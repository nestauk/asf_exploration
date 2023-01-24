"""
Script to do keyword and expression analysis.
Given a set of keywords and expressions of interest for the mission,
we identify the proportion of complaints mentioning those.
"""

import config
import getters
import pandas as pd
import os
import visualisation_utils
import general_utils

keywords_expressions = config.keywords_expressions
outputs_local_path_figures_keyword_analysis = (
    config.outputs_local_path_figures_keyword_analysis
)


def keyword_expression_dummies(data: pd.DataFrame):
    """
    Adds keyword and expression dummies to the dataset.
    Keyword example: "installer"
    Expression example: "district network"

    Args:
        data: a dataframe with data
    """
    for g in keywords_expressions.keys():
        for ke in keywords_expressions[g]:
            if " " in ke:
                data["EXP:" + ke] = data["processed_complaint_summary"].apply(
                    lambda x: 1 if ke in x else 0
                )
            else:
                data["KEYW:" + ke] = data["tokens"].apply(lambda x: 1 if ke in x else 0)


def group_keyword_expression_dummies(data):
    """
    Creates and adds keyword and expression dummy groups to the dataset.

    Args:
        data: a dataframe with data
    """
    for g in keywords_expressions.keys():
        columns = ["KEYW:" + col for col in keywords_expressions[g] if " " not in col]
        columns = columns + [
            "EXP:" + col for col in keywords_expressions[g] if " " in col
        ]
        data["G:" + g] = data[columns].any(axis=1).astype(int)


def perform_keyword_expression_analysis(data):
    """
    Performs keyword and expression analysis:
    - Creates keywords and expression dummy variables as well as groups of these;
    - Creates stats for the above;
    - Plots and saves these stats.

    Args:
        data: a dataframe with data
    """

    print(
        "We're analysing the presence of specific keywords and expressions in text...\n"
    )

    # keyword and epxression analysis
    keyword_expression_dummies(data)

    dummies_keywords_expressions = [
        col
        for col in data.columns
        if (col.startswith("KEYW:") or col.startswith("EXP:"))
    ]

    stats_keywords_expressions = general_utils.complaints_by(
        df=data,
        by=dummies_keywords_expressions,
        dummy_vars=True,
        percent=True,
        sort=True,
    )
    # only plot for the top keywords and expressions
    stats_keywords_expressions = stats_keywords_expressions.loc[
        : config.number_keyword_expressions_to_show
    ]

    visualisation_utils.plotting_complaints_by_dummies(
        stats_keywords_expressions,
        "keywords and expressions (top {})".format(
            config.number_keyword_expressions_to_show
        ),
        path=outputs_local_path_figures_keyword_analysis,
    )

    # Groups of keywords and expressions analysis
    group_keyword_expression_dummies(data)

    dummies_groups = [col for col in data.columns if col.startswith("G:")]

    stats_groups = general_utils.complaints_by(
        df=data, by=dummies_groups, dummy_vars=True, percent=True, sort=True
    )

    visualisation_utils.plotting_complaints_by_dummies(
        stats_groups, "keywords group", path=outputs_local_path_figures_keyword_analysis
    )

    print(
        "Keyword and expression analysis done! See results under {}.\n".format(
            outputs_local_path_figures_keyword_analysis
        )
    )


if __name__ == "__main__":
    # Get processed RECC data
    recc_data = getters.get_processed_recc_data()

    # creating local path to store figures if it does not exist
    if not os.path.exists(outputs_local_path_figures_keyword_analysis):
        os.makedirs(outputs_local_path_figures_keyword_analysis)

    # Setting plotting syle
    visualisation_utils.set_plotting_styles()

    # Keywords and expressions analysis
    perform_keyword_expression_analysis(recc_data)
