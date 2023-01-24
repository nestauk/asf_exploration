"""
Script with descriptive analysis
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import getters
import visualisation_utils
import config
from general_utils import complaints_by

outputs_local_path_figures_descriptive_analysis = (
    config.outputs_local_path_figures_descriptive_analysis
)


def plotting_complaints_per_month(complaints_per_month: pd.DataFrame):
    """
    Plots number of complaints per month.

    Args:
        complaints_per_month: data frame with counts of complaints per month
    """
    months = list(complaints_per_month["year_month"])
    x_ticks = [months[i] for i in range(len(months)) if i % 6 == 0] + [months[-1]]

    plt.figure(figsize=(config.figure_size_x, config.figure_size_y))
    plt.plot(
        complaints_per_month["year_month"],
        complaints_per_month["n_complaints"],
        "-o",
        markersize=5,
        color=config.default_colour,
    )

    max_y = visualisation_utils.max_value_to_show(complaints_per_month["n_complaints"])[
        0
    ]
    plt.ylim(0, max_y)
    plt.xticks(x_ticks, rotation=20)
    plt.title("Number of monthly complaints")

    plt.tight_layout()
    plt.savefig(
        outputs_local_path_figures_descriptive_analysis + "complaints_per_month.png",
        dpi=300,
    )


def plotting_complaints_per_year(complaints_per_year: pd.DataFrame):
    """
    Plots number of complaints per year.

    Args:
        complaints_per_year: data frame with counts of complaints per year
    """
    plt.figure(figsize=(config.figure_size_x, config.figure_size_y))
    plt.bar(
        x=complaints_per_year["year"],
        height=complaints_per_year["n_complaints"],
        color=config.default_colour,
    )

    max_y = visualisation_utils.max_value_to_show(complaints_per_year["n_complaints"])[
        0
    ]
    plt.ylim(0, max_y)
    plt.xticks(complaints_per_year["year"])
    plt.title("Number of yearly complaints")

    plt.tight_layout()
    plt.savefig(
        outputs_local_path_figures_descriptive_analysis + "complaints_per_year.png",
        dpi=300,
    )


def plotting_length_complaints(distribution_length_complaints: pd.DataFrame):
    """
    Plots the distribution of complaints by their length, i.e. how many complaints have a certain length.

    Args:
        distribution_length_complaints: data frame with number of complaints with a given length.
    """
    bins = visualisation_utils.compute_bins(
        distribution_length_complaints["complaint_length"]
    )

    plt.figure(figsize=(config.figure_size_x, config.figure_size_y))
    plt.hist(
        x=distribution_length_complaints["complaint_length"],
        bins=bins,
        color=config.default_colour,
    )

    plt.xlabel("Number of characters in complaint text")
    plt.ylabel("Number of complaints")
    plt.title("Distribution of complaints by length")

    plt.tight_layout()
    plt.savefig(
        outputs_local_path_figures_descriptive_analysis
        + "distribution_length_complaints.png",
        dpi=300,
    )


def plotting_length_complaints_per_year(distribution_length_complaints: pd.DataFrame):
    """
    Plots the distribution of complaints by their length for each year, i.e. how many complaints have a certain length each year.

    Args:
        distribution_length_complaints: data frame with number of complaints with a given length in a certain year.
    """
    bins = visualisation_utils.compute_bins(
        distribution_length_complaints["complaint_length"]
    )

    years = distribution_length_complaints["year"].unique()
    years.sort()

    colors = config.nesta_colours[: len(years)]

    fig, ax = plt.subplots(
        len(years),
        1,
        figsize=(config.figure_size_x, config.figure_size_y * len(years) * 2 / 3),
    )
    for i in range(len(years)):
        ax[i].hist(
            distribution_length_complaints[
                distribution_length_complaints["year"] == years[i]
            ]["complaint_length"],
            bins=bins,
            color=colors[i],
            density=True,
        )
    ax[i].set_xlabel("Number of characters in complaint text")
    fig.suptitle("Density of complaints yearly")
    fig.legend(years)

    plt.tight_layout()
    plt.savefig(
        outputs_local_path_figures_descriptive_analysis
        + "distribution_length_complaints_yearly.png",
        dpi=300,
    )


def plotting_distribution_complaints_by_number_cat_or_tech(
    data: pd.DataFrame, by: str = "categories"
):
    """
    Plots percentage of complaints that have a certain number of categories/technologies.

    data: data frame with counts data
    by: 'categories' or 'technologies. Defaults to 'categories'.
    """

    if by not in ["categories", "technologies"]:
        raise ValueError("'by' should be either 'categories' or 'technologies'.")

    if by == "categories":
        y_var = "number_of_short_categories"
    else:
        y_var = "number_of_technologies"

    data[y_var] = data[y_var].astype(str)

    visualisation_utils.horizontal_bar_plot(data, y_var, "percent_complaints")
    plt.title("Percentage of complaints by number of " + by)

    plt.tight_layout()

    plt.xlabel("Percentage of complaints")
    plt.ylabel("Number of " + by)

    plt.savefig(
        outputs_local_path_figures_descriptive_analysis
        + "percentage_complaints_by_number_of_"
        + by
        + ".png",
        dpi=300,
    )


def descriptive_analysis(data: pd.DataFrame):
    """
    Produces descriptive analysis:
    - complaints per month;
    - complaints per year;
    - length of complaints;
    - length of complaints per year;
    - number and percentage of complaints per tech type;
    - number and percentage of complaints per category.

    Args:
        data: data to do descriptive analysis with.

    """
    print("Descriptive analysis ongoing...\n")
    # Complaints per month
    complaints_per_month = complaints_by(data, ["year_month", "year", "month"])
    plotting_complaints_per_month(complaints_per_month)

    # Complaints per year
    complaints_per_year = complaints_by(data, "year")
    plotting_complaints_per_year(complaints_per_year)
    visualisation_utils.pandas_df_to_figure(
        complaints_per_year,
        outputs_local_path_figures_descriptive_analysis,
        "complaints_per_year_table.png",
    )

    # Length of complaints
    distribution_length_complaints = complaints_by(data, ["complaint_length", "year"])
    plotting_length_complaints(distribution_length_complaints)

    # Length of complaints per year
    plotting_length_complaints_per_year(distribution_length_complaints)

    # Number and percentage of complaints per tech type
    technology_columns = [col for col in data.columns if col.startswith("tech:")]
    complaints_by_tech = complaints_by(
        df=data, by=technology_columns, percent=True, dummy_vars=True, sort=True
    )
    visualisation_utils.plotting_complaints_by_dummies(
        complaints_by_tech,
        by="technology",
        path=outputs_local_path_figures_descriptive_analysis,
    )
    visualisation_utils.pandas_df_to_figure(
        complaints_by_tech,
        outputs_local_path_figures_descriptive_analysis,
        "complaints_by_tech_table.png",
    )

    # Number and percentage of complaints per category
    categories_columns = [col for col in data.columns if col.startswith("category:")]
    complaints_by_category = complaints_by(
        df=data, by=categories_columns, percent=True, dummy_vars=True, sort=True
    )
    visualisation_utils.plotting_complaints_by_dummies(
        complaints_by_category,
        by="category",
        path=outputs_local_path_figures_descriptive_analysis,
    )
    visualisation_utils.pandas_df_to_figure(
        complaints_by_category,
        outputs_local_path_figures_descriptive_analysis,
        "complaints_by_category_table.png",
    )

    # Percentage of complaints with a given number of categories
    n_complaints_n_categories = complaints_by(
        df=data,
        by=["number_of_short_categories"],
        percent=True,
        dummy_vars=False,
        sort=False,
    )
    plotting_distribution_complaints_by_number_cat_or_tech(
        n_complaints_n_categories, by="categories"
    )

    # Percentage of complaints with a given number of technologies
    n_complaints_n_tech = complaints_by(
        df=data,
        by=["number_of_technologies"],
        percent=True,
        dummy_vars=False,
        sort=False,
    )
    plotting_distribution_complaints_by_number_cat_or_tech(
        n_complaints_n_tech, by="technologies"
    )

    print(
        "Descriptive analysis complete! Plots can be found under {}.\n".format(
            outputs_local_path_figures_descriptive_analysis
        )
    )


if __name__ == "__main__":
    # Get processed RECC data
    recc_data = getters.get_processed_recc_data()

    # creating local path to store figures if it does not exist
    if not os.path.exists(outputs_local_path_figures_descriptive_analysis):
        os.makedirs(outputs_local_path_figures_descriptive_analysis)

    # Setting plotting syle
    visualisation_utils.set_plotting_styles()

    # Descriptive analysis
    descriptive_analysis(recc_data)
