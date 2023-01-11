"""
Script with descriptive analysis
"""

import pandas as pd
import math
import os
import matplotlib.pyplot as plt
import getters
import visualisation_utils
import config
from text_analysis_utils import complaints_by

outputs_local_path_figures = config.outputs_local_path_figures

def plotting_complaints_per_month(complaints_per_month:pd.DataFrame):
    """
    Plots number of complaints per month.

    Args:
        complaints_per_month: data frame with counts of complaints per month
    """
    months = list(complaints_per_month["year_month"])
    x_ticks = [months[i] for i in range(len(months)) if i%6==0] + [months[-1]]

    plt.figure(figsize=(config.figure_size_x,config.figure_size_y))
    plt.plot(complaints_per_month["year_month"],
            complaints_per_month["n_complaints"], "-o", markersize=5, color = config.default_colour)

    max_y = visualisation_utils.max_value_to_show(complaints_per_month["n_complaints"])[0]
    plt.ylim(0,max_y)
    plt.xticks(x_ticks, rotation = 20)
    plt.title("Number of monthly complaints")

    plt.tight_layout()
    plt.savefig(outputs_local_path_figures+"complaints_per_month.png", dpi=300)

def plotting_complaints_per_year(complaints_per_year:pd.DataFrame):
    """
    Plots number of complaints per year.

    Args:
        complaints_per_year: data frame with counts of complaints per year
    """
    plt.figure(figsize=(config.figure_size_x,config.figure_size_y))
    plt.bar(x = complaints_per_year["year"],
            height = complaints_per_year["n_complaints"], color = config.default_colour)

    max_y = visualisation_utils.max_value_to_show(complaints_per_year["n_complaints"])[0]
    plt.ylim(0,max_y)
    plt.xticks(complaints_per_year["year"])
    plt.title("Number of yearly complaints")

    plt.tight_layout()
    plt.savefig(outputs_local_path_figures+"complaints_per_year.png", dpi=300)
    

def plotting_length_complaints(distribution_length_complaints:pd.DataFrame):
    """
    Plots the distribution of complaints by their length, i.e. how many complaints have a certain length.

    Args:
        distribution_length_complaints: data frame with number of complaints with a given length.
    """
    bins = visualisation_utils.compute_bins(distribution_length_complaints["complaint_length"])

    plt.figure(figsize=(config.figure_size_x,config.figure_size_y))
    plt.hist(x = distribution_length_complaints["complaint_length"], bins = bins, color = config.default_colour)

    plt.xlabel("Number of characters")
    plt.ylabel("Number of complaints")
    plt.title("Distribution of complaints by length")

    plt.tight_layout()
    plt.savefig(outputs_local_path_figures+"distribution_length_complaints.png", dpi=300)

def plotting_length_complaints_per_year(distribution_length_complaints:pd.DataFrame):
    """
    Plots the distribution of complaints by their length for each year, i.e. how many complaints have a certain length each year.

    Args:
        distribution_length_complaints: data frame with number of complaints with a given length in a certain year.
    """
    bins = visualisation_utils.compute_bins(distribution_length_complaints["complaint_length"])

    years = distribution_length_complaints["year"].unique()
    years.sort()

    colors = config.nesta_colours[:len(years)]

    fig, ax = plt.subplots(len(years), 1, figsize=(config.figure_size_x,config.figure_size_y*len(years)*2/3))
    for i in range(len(years)):
        ax[i].hist(distribution_length_complaints[distribution_length_complaints["year"]==years[i]]["complaint_length"],
                bins = bins, color = colors[i], density = True)
    ax[i].set_xlabel("Complaint length")
    fig.suptitle("Density of complaints yearly")
    fig.legend(years)

    plt.tight_layout()
    plt.savefig(outputs_local_path_figures+"distribution_length_complaints_yearly.png", dpi=300)



if __name__ == "__main__":
    print("Descriptive analysis ongoing...\n")
    # Get processed RECC data
    recc_data = getters.get_processed_recc_data()

    # creating local path to store figures if it does not exist
    if not os.path.exists(outputs_local_path_figures):
        os.mkdir(outputs_local_path_figures)

    # Setting plotting syle
    visualisation_utils.set_plotting_styles()

    # Complaints per month
    complaints_per_month = complaints_by(recc_data, ["year_month", "year", "month"])
    plotting_complaints_per_month(complaints_per_month)

    # Complaints per year
    complaints_per_year = complaints_by(recc_data, "year")
    plotting_complaints_per_year(complaints_per_year)
    visualisation_utils.pandas_df_to_figure(complaints_per_year, outputs_local_path_figures, "complaints_per_year_table.png")

    # Length of complaints
    distribution_length_complaints = complaints_by(recc_data, ["complaint_length", "year"])
    plotting_length_complaints(distribution_length_complaints)

    # Length of complaints per year
    plotting_length_complaints_per_year(distribution_length_complaints)

    # Number and percentage of complaints per tech type
    technology_columns = [col for col in recc_data.columns if col.startswith("tech:")]
    complaints_by_tech = complaints_by(df = recc_data, by = technology_columns, percent = True, dummy_vars = True, sort=True)
    visualisation_utils.plotting_complaints_by_dummies(complaints_by_tech, by="technology")
    visualisation_utils.pandas_df_to_figure(complaints_by_tech, outputs_local_path_figures, "complaints_by_tech_table.png")

    # Number and percentage of complaints per category
    categories_columns = [col for col in recc_data.columns if col.startswith("category:")]
    complaints_by_category = complaints_by(df = recc_data, by = categories_columns, percent = True, dummy_vars = True, sort=True)
    visualisation_utils.plotting_complaints_by_dummies(complaints_by_category, by="category")
    visualisation_utils.pandas_df_to_figure(complaints_by_category, outputs_local_path_figures, "complaints_by_category_table.png")

    print("Descriptive analysis complete! Plots can be found under '/outputs/figures/'.\n")