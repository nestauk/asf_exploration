"""
Script to process RECC complaints data. 
"""

# package imports
import config
import getters
import pandas as pd
import os
import re
from datetime import datetime
from nltk import word_tokenize
from text_analysis_utils import stemming, lemmatising


# paths and file names
processed_recc_data_filename = config.processed_recc_data_filename
outputs_local_path = config.outputs_local_path
outputs_local_path_data = config.outputs_local_path_data
variants_same_expression = config.variants_same_expression
categories_short_names = config.categories_short_names


def camel_case_columns(df: pd.DataFrame):
    """
    Transforms column names in pandas dataframe into lower and camel case.
    """
    cols = df.columns
    cols = [c.lower() for c in cols]
    cols = [c.replace(" ", "_") for c in cols]
    df.columns = cols


def deal_with_fit(text: str) -> str:
    """
    Replaces 'FiT' by "feed in tariff.
    We do this separately from merges_expression_variations() as we do not
    want to replace the word 'fit' by 'feed in tariff'. 
    """
    return text.replace("FiT", "feed in tariff")


def merges_expression_variations(text: str) -> str:
    """
    Merges together different variations of the same expression.
    E.g.: Replaces "air source heat pump" by "ashp" in text.
    """
    for expression in variants_same_expression.keys():
        text = text.replace(expression, variants_same_expression[expression])
    return text


def process_complaint_summary(data: pd.DataFrame) -> pd.DataFrame:
    """
    Processes complaint summary variable by:
    - Dealing with "FiT" expression;
    - Creating new variable with lower case complaint text;
    - Merging together different air source heat pump expressions;
    - Creating a new variable with number of characters in complaint;
    - Creating a variable with the complaint summary tokens.

    Args:
        data: dataframe with RECC data
    Returns:
        The processed dataframe.
    """

    data["processed_complaint_summary"] = data["complaint_summary"].apply(deal_with_fit)

    data["processed_complaint_summary"] = data[
        "processed_complaint_summary"
    ].str.lower()

    data["processed_complaint_summary"] = data["processed_complaint_summary"].apply(
        merges_expression_variations
    )

    data["complaint_length"] = data["processed_complaint_summary"].str.len()

    data["tokens"] = data["processed_complaint_summary"].apply(
        lambda x: re.sub("[^A-Za-z0-9]+", " ", x)
    )

    data["tokens"] = data["tokens"].apply(lambda x: word_tokenize(x))

    data["stems"] = data["tokens"].apply(stemming)

    data["lemmas"] = data["tokens"].apply(lemmatising)

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
    Processes the categories column by filling NAs with "No category specified; "
    and adding "; " at the end of each categories' instance to make it easier to split by category in the future.
    Also creates an additional variable with a short version of each category.

    Args:
        data: dataframe with RECC data
    Returns:
        Processed dataframe.
    """
    data["categories"].fillna("No category specified; ", inplace=True)
    data["categories"] = data["categories"].apply(
        lambda x: x + "; " if not x.endswith("; ") else x
    )
    data["short_categories"] = data["categories"].copy()
    for cat in categories_short_names.keys():
        data["short_categories"] = data["short_categories"].apply(
            lambda x: x.replace(cat, categories_short_names[cat])
        )
    return data


def process_recc_data(data: pd.DataFrame):
    """
    Processes raw RECC data and saves it to a csv in the ouputs folder.
    Args:
        data: dataframe with RECC data
    """

    print("We're processing RECC data for you...\n")

    camel_case_columns(data)

    data = extract_info_from_date(data)

    data = process_complaint_summary(data)

    data = create_dummy_variables_and_total(data, "technologies", "tech")

    data = changes_to_categories(data)

    data = create_dummy_variables_and_total(data, "short_categories", "category")

    if not os.path.exists(outputs_local_path_data):
        os.makedirs(outputs_local_path_data)

    data.to_csv(outputs_local_path_data + processed_recc_data_filename)

    print("RECC data is processed and can be found under '/outputs/data/'.\n")


if __name__ == "__main__":
    # Download raw RECC complaints data from S3
    getters.download_recc_data_from_s3()

    # Save raw RECC complaints data as one sheet csv
    getters.raw_recc_data_to_one_sheet()

    # Get raw RECC complaints data and process it
    raw_recc_data = getters.get_raw_recc_data()
    process_recc_data(raw_recc_data)
