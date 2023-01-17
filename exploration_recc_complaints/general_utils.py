"""
Script with general utility functions.
"""


import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import config


def complaints_by(
    df: pd.DataFrame,
    by: list[str],
    dummy_vars: bool = False,
    percent: bool = False,
    sort: bool = False,
) -> pd.DataFrame:
    """
    Computes number of complaints by a set of variables.

    Arg:
        df: complaints data frame
        by: list of variables by which we want to aggregate the number of complaints
        dummy_vars: True if "by" are dummy variables, False otherwise
        percent: True to compute percentage of complaints, False otherwise
        sort: True if we want to sort variables by number of complaints

    Returns:
        gb: a pandas dataframe with aggregated number of complaints.
    """
    if dummy_vars:
        gb = pd.DataFrame(df.sum()[by], columns=["n_complaints"])
        gb.reset_index(drop=False, inplace=True)
    else:
        gb = df.groupby(by, as_index=False)[["complaints_reference"]].nunique()
        gb.rename(columns={"complaints_reference": "n_complaints"}, inplace=True)

    if sort:
        gb.sort_values("n_complaints", ascending=False, inplace=True)
        gb.reset_index(drop=True, inplace=True)

    if percent:
        gb["percent_complaints"] = gb["n_complaints"] / len(df) * 100

    return gb


def stemming(tokens: list[str]) -> str:
    """
    Applies porter stemming to tokens for tokens not in acronyms list.
    If token is an acronym, it stays the same.

    Args:
        tokens: list of strings representing words/tokens
    Returns:
        A string with stemmed tokens in order.
    """
    porter = PorterStemmer()
    return " ".join(
        [
            porter.stem(word) if word not in config.domain_acronyms_list else word
            for word in tokens
        ]
    )


def lemmatising(tokens: list[str]) -> str:
    """
    Applies lemmatisation to tokens for tokens not in acronyms list.
    If token is an acronym, it stays the same.

    Args:
        tokens: list of strings representing words/tokens
    Returns:
        A string with lemmatised tokens in order.
    """
    lemmatizer = WordNetLemmatizer()
    return " ".join(
        [
            lemmatizer.lemmatize(word)
            if word not in config.domain_acronyms_list
            else word
            for word in tokens
        ]
    )
