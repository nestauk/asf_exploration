"""
Script to process RECC complaints data. 
"""

# package imports
import config
import getters
import pandas as pd
import os
import re
import nltk
from datetime import datetime


# paths and file names
raw_recc_data_filename_xlsx = config.raw_recc_data_filename_xlsx
raw_recc_data_filename_csv = config.raw_recc_data_filename_csv
outputs_local_path = config.outputs_local_path
processed_recc_data_filename = config.processed_recc_data_filename


def camel_case_columns(df: pd.DataFrame):
    """
    Transforms column names in pandas dataframe into lower and camel case.
    """
    cols = df.columns
    cols = [c.lower() for c in cols]
    cols = [c.replace(" ", "_") for c in cols]
    df.columns = cols


def unify_ashp_expressions(text: str) -> str:
    """
    Replaces "air source heat pump" by "ashp" in text.
    """
    text = text.replace("air source heat pump (ashp)", "ashp")
    text = text.replace("air source heat pump", "ashp")
    return text


def process_complaint_summary(data: pd.DataFrame) -> pd.DataFrame:
    """
    Processes complaint summary variable by:
    - Creating new variable with lower case complaint text;
    - Unifying air source heat pump expressions;
    - Creating a new variable with number of characters in complaint;
    - Creating a variable with the complaint summary tokens.

    Args:
        data: dataframe with RECC data
    Returns:
        The processed dataframe.
    """
    raw_recc_data["processed_complaint_summary"] = raw_recc_data[
        "complaint_summary"
    ].str.lower()

    raw_recc_data["processed_complaint_summary"] = raw_recc_data[
        "processed_complaint_summary"
    ].apply(unify_ashp_expressions)

    raw_recc_data["complaint_length"] = raw_recc_data[
        "processed_complaint_summary"
    ].str.len()

    raw_recc_data["tokens"] = raw_recc_data["processed_complaint_summary"].apply(
        lambda x: re.sub("[^A-Za-z0-9]+", " ", x)
    )

    raw_recc_data["tokens"] = raw_recc_data["tokens"].apply(
        lambda x: nltk.word_tokenize(x)
    )

    return data


def create_dummy_variables_and_total(
    data: pd.DataFrame, variable: str, prefix: str
) -> pd.DataFrame:
    """
    Creates dummy variables based on an existing variable in the data frame.
    Also creates a variable with the totals (number of dummy variables with 1 for each instance).

    Args:
        data: dataframe with RECC data
        variable: variable to split into dummy variables
        prefix: prefix to add to each dummy variable
    Returns:
        The processed dataframe.

    """

    unique_values = list(set(data[variable].unique().sum().split("; ")[:-1]))

    dummy_variable_names = [prefix + ":" + c for c in unique_values]

    for c in range(len(unique_values)):
        data[dummy_variable_names[c]] = data[variable].apply(
            lambda x: 1 if unique_values[c] in x else 0
        )

    data["number_of_" + variable] = data[dummy_variable_names].sum(axis=1)

    return data


def extract_info_from_date(data: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts info such as year and month from the date variable.

    Args:
        data: dataframe with RECC data
    Returns:
        The processed dataframe.
    """
    data["year_month"] = data["date_received"].apply(lambda x: x[:7])
    data["date_received"] = data["date_received"].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d")
    )
    data["year"] = data["date_received"].dt.year
    data["month"] = data["date_received"].dt.month

    return data


def changes_to_categories(data: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the categories column by filling NAs with "No category specified;"
    and adding "; " at the end of each categories' instance to make it easier to split by category in the future.

    Args:
        data: dataframe with RECC data
    Returns:
        Processed dataframe.
    """
    data["categories"].fillna("No category specified; ", inplace=True)
    data["categories"] = data["categories"].apply(
        lambda x: x + "; " if not x.endswith("; ") else x
    )

    return data


def process_recc_data(raw_recc_data: pd.DataFrame):
    """
    Processes raw RECC data and saves it to a csv in the ouputs folder.
    Args:
        data: dataframe with RECC data
    """

    camel_case_columns(raw_recc_data)

    raw_recc_data = extract_info_from_date(raw_recc_data)

    raw_recc_data = process_complaint_summary(raw_recc_data)

    raw_recc_data = create_dummy_variables_and_total(
        raw_recc_data, "technologies", "tech"
    )

    raw_recc_data = changes_to_categories(raw_recc_data)

    raw_recc_data = create_dummy_variables_and_total(
        raw_recc_data, "categories", "category"
    )

    if not os.path.exists(outputs_local_path):
        os.mkdir(outputs_local_path)

    raw_recc_data.to_csv(outputs_local_path + processed_recc_data_filename)


if __name__ == "__main__":
    # Download raw RECC complaints data from S3
    getters.download_recc_data_from_s3()

    # Save raw RECC complaints data as one sheet csv
    getters.raw_recc_data_to_one_sheet()

    # Get raw RECC complaints data and process it
    raw_recc_data = getters.get_raw_recc_data()
    process_recc_data(raw_recc_data)
