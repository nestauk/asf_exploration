"""
Script with processing utility functions.
"""


import pandas as pd
import math
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import config


def complaints_by(df:pd.DataFrame, by:list[str], dummy_vars:bool = False, percent:bool = False, sort:bool = False) -> pd.DataFrame:
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
        gb.rename(columns = {"complaints_reference": "n_complaints"}, inplace=True)

    if sort:
        gb.sort_values("n_complaints", ascending=False, inplace=True)
        gb.reset_index(drop = True, inplace=True)

    if percent:
        gb["percent_complaints"] = gb["n_complaints"]/len(df)*100

    return gb

def stemming(tokens:list[str]) -> str:
    """
    Applies porter stemming to tokens for tokens not in acronyms list.
    If token is an acronym, it stays the same.

    Args:
        tokens: list of strings representing words/tokens
    Returns:
        A string with stemmed tokens in order.
    """
    porter = PorterStemmer()
    return " ".join([porter.stem(word) if word not in config.domain_acronyms_list else word for word in tokens])

def lemmatising(tokens:list[str]) -> str:
    """
    Applies lemmatisation to tokens for tokens not in acronyms list.
    If token is an acronym, it stays the same.

    Args:
        tokens: list of strings representing words/tokens
    Returns:
        A string with lemmatised tokens in order.
    """
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(word) if word not in config.domain_acronyms_list else word for word in tokens])

def compute_tf_idf_dataframe(data, text_process, filter_var=None) -> pd.DataFrame:
    """
    Computes tf-idf dataframe.

    Args:
        data: dataframe with data
        text_process: either "normal", "stemming" or "lemmatising". Defaults to "normal".
        filter_var: variable to filter data by

    """
    if text_process=="normal":
        corpus = list(data["processed_complaint_summary"])
    elif text_process == "stemming":
        corpus = list(data["stems"])
    elif text_process == "lemmatising":
        corpus = list(data["lemmas"])
    else:
        raise ValueError("text_process should take one of the values: 'normal','stemming', 'lemmatising'.")

    vectorizer = TfidfVectorizer(norm=None, ngram_range = (config.ngram_min, config.ngram_max), use_idf=False)
    x = vectorizer.fit_transform(corpus)
    x_features = vectorizer.get_feature_names_out()
    df_tfidfvect = pd.DataFrame(data = x.toarray(),
                            index = data["complaints_reference"],
                            columns = x_features)

    if filter_var is not None:
        data.set_index("complaints_reference", inplace=True)
        df_tfidfvect[filter_var] = data[filter_var]
        data.reset_index(inplace=True)

        
        df_tfidfvect = df_tfidfvect[df_tfidfvect[filter_var]==1]
        df_tfidfvect.drop(filter_var, axis=1)
    
    df_tfidfvect = pd.DataFrame(df_tfidfvect.mean(axis=0))
    df_tfidfvect.columns = ["tf_idf"]

    return df_tfidfvect