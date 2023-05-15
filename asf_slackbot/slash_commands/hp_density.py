# ==== IMPORTS ====

import numpy as np
import pandas as pd
import re
from scipy import spatial

from asf_core_data.getters.supplementary_data.geospatial import coordinates

# ================


def to_Cartesian(lat, lng):
    """Convert latitude/longitude coordinates to Cartesian coordinate system.

    Args:
        lat (float): Latitude.
        lng (float): Longitude.

    Returns:
        np.array: Converted cartesian coordinates (x,y,z).
    """

    R = 6367  # radius of the Earth in kilometers

    x = R * np.cos(lat) * np.cos(lng)
    y = R * np.cos(lat) * np.sin(lng)
    z = R * np.sin(lat)
    return np.array((x, y, z)).T


def extract_Cartesian_coords(df):
    """Get latitude and longitude from df and convert to Cartesian coordinates.

    Args:
        df (pd.DataFrame): Dataframe including LATITUDE and LONGITUDE column.

    Returns:
        coords (numpy.ndarray): Cartesian coordinates.
    """

    coords = df[["LATITUDE", "LONGITUDE"]].to_numpy()

    coords = np.deg2rad(coords)
    coords = to_Cartesian(coords[:, 0], coords[:, 1])

    return coords


def create_query(lat, lng):
    """Create a query df with given latitude and longitude.

    Args:
        lat (float): Latitude.
        lng (float): Longitude.

    Returns:
        coords (numpy.ndarray): Cartesian coordinates.
    """

    non_hp_df = pd.DataFrame({"LATITUDE": [lat], "LONGITUDE": [lng]})
    non_hp_coords = extract_Cartesian_coords(non_hp_df)

    return non_hp_coords


def get_n_hp_closeby(df, postcode, property_type=None, max_dist=10):
    """Get the number of closeby heat pumps given the postcode, property type and radius.

    Args:
        df (pd.DataFrame): Dataframe including information about heat pumps and postcode.
        postcode (str): Postcode to search for.
        property_type (str, optional): Property type to filter by. Defaults to None.
        max_dist (int, optional): Maximum distance in km to postcode / search radius. Defaults to 10.

    Returns:
        int: Number of closeby heat pumps given filter and radius.
    """

    postcode = postcode.upper()
    postcode = re.sub(" ", "", postcode)
    df = df[~df["LATITUDE"].isna()]

    coord = coordinates.get_postcode_coordinates(data_path="S3")

    coord["POSTCODE"] = coord["POSTCODE"].str.replace(" ", "")
    df["POSTCODE"] = df["POSTCODE"].str.replace(" ", "")

    try:
        lat, long = (
            coord.loc[coord["POSTCODE"] == postcode]["LATITUDE"].values[0],
            coord.loc[coord["POSTCODE"] == postcode]["LONGITUDE"].values[0],
        )
    except IndexError:
        return None

    # Filter conditions
    no_cond = ~df["LATITUDE"].isna()  # will always be true
    flat = df["PROPERTY_TYPE"] == "Flat"

    terraced = [
        "Enclosed Mid-Terrace",
        "Enclosed End-Terrace",
        "End-Terrace",
        "Mid-Terrace",
    ]

    terraced_house = (df["PROPERTY_TYPE"] == "House") & (
        df["BUILT_FORM"].isin(terraced)
    )

    detached_house = (df["PROPERTY_TYPE"] == "House") & (df["BUILT_FORM"] == "Detached")

    semi_house = (df["PROPERTY_TYPE"] == "House") & (
        df["BUILT_FORM"] == "Semi-Detached"
    )

    cond_dict = {
        "Flats": flat,
        "Semi-detached Houses": semi_house,
        "Detached Houses": detached_house,
        "Terraced Houses": terraced_house,
        "Any": no_cond,
        None: no_cond,
    }

    # Filter by property type
    conds = cond_dict[property_type]
    hp_samples = df.loc[df["HP_INSTALLED"] & conds]

    # Convert to Cartesian
    hp_coords = extract_Cartesian_coords(hp_samples)
    query_coords = create_query(lat, long)

    # Build search trees
    hp_tree = spatial.KDTree(hp_coords)
    query_tree = spatial.KDTree(query_coords)

    # Extract matches
    match_indices = hp_tree.query_ball_tree(query_tree, r=max_dist)

    # Count matches
    return np.array([[len(x) for x in match_indices if len(x) > 0]])[0].sum()
