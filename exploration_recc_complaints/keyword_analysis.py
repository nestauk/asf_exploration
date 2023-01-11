"""
Script with keyword and expression analysis.
"""

import config
import getters
import pandas as pd
import os
import visualisation_utils
import matplotlib.pyplot as plt
import text_analysis_utils

keywords_expressions = config.keywords_expressions
outputs_local_path_figures = config.outputs_local_path


def keyword_expression_dummies(data: pd.DataFrame):
    for g in keywords_expressions.keys():
        for ke in keywords_expressions[g]:
            if " " in ke:
                data["EXP:" + ke] = data["processed_complaint_summary"].apply(
                    lambda x: 1 if ke in x else 0
                )
            else:
                data["KEYW:" + ke] = data["tokens"].apply(lambda x: 1 if ke in x else 0)


def group_keyword_expression_dummies(data):
    for g in keywords_expressions.keys():
        columns = ["KEYW:" + col for col in keywords_expressions[g] if " " not in col]
        columns = columns + [
            "EXP:" + col for col in keywords_expressions[g] if " " in col
        ]
        data["G:" + g] = data[columns].sum(axis=1)

    group_columns = [col for col in data.columns if col.startswith("G:")]
    for col in group_columns:
        data[col] = data[col].apply(lambda x: 1 if x > 1 else x)


if __name__ == "__main__":
    # Get processed RECC data
    recc_data = getters.get_processed_recc_data()

    # creating local path to store figures if it does not exist
    if not os.path.exists(outputs_local_path_figures):
        os.makedirs(outputs_local_path_figures)

    # Setting plotting syle
    visualisation_utils.set_plotting_styles()

    # Keywords and expressions in complaints text (top 10)
    keyword_expression_dummies(recc_data)
    dummies_keywords_expressions = [
        col
        for col in recc_data.columns
        if (col.startswith("KEYW:") or col.startswith("EXP:"))
    ]
    stats_keywords_expressions = text_analysis_utils.complaints_by(
        df=recc_data,
        by=dummies_keywords_expressions,
        dummy_vars=True,
        percent=True,
        sort=True,
    )
    stats_keywords_expressions = stats_keywords_expressions.loc[:10]
    visualisation_utils.plotting_complaints_by_dummies(
        stats_keywords_expressions, "keywords and expressions (top 10)"
    )

    # Amount of complaints by keyword group
    group_keyword_expression_dummies(recc_data)
    dummies_groups = [col for col in recc_data.columns if col.startswith("G:")]
    stats_groups = text_analysis_utils.complaints_by(
        df=recc_data, by=dummies_groups, dummy_vars=True, percent=True, sort=True
    )
    visualisation_utils.plotting_complaints_by_dummies(stats_groups, "keywords group")
