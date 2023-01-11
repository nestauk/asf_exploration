"""
Analysis of top tokens and n-grams.
"""

import config
import getters
import os
import visualisation_utils
import pandas as pd
import nltk

nltk.download("punkt")
from nltk.corpus import stopwords

nltk.download("stopwords")
from gensim.parsing.preprocessing import STOPWORDS
from text_analysis_utils import stemming, lemmatising, compute_tf_idf_dataframe

keywords = config.keywords_expressions
expressions = config.keywords_expressions
outputs_local_path_figures = config.outputs_local_path
domain_stopwords = config.domain_stopwords
top_ngrams_variants = config.top_ngrams_variants


def stopwords_definition(text_process: str = "normal") -> list:
    """
    Function to define stopwords, by putting together NLTK, gensim,
    as well as domain stopwords. Defaults to "normal".
    If text_process different from "normal", it applies stemming/lemmatising.

    Args:
        text_process: either "normal", "stemming" or "lemmatising"

    Returns:
        A list of stopwords.
    """
    sw_nltk = stopwords.words("english")
    sw_gensim = [s for s in STOPWORDS if s not in sw_nltk]
    for w in ["bill", "full", "several", "last", "always", "kg", "serious", "fire"]:
        sw_gensim.remove(w)

    stopwords_list = sw_nltk + sw_gensim

    stopwords_list = stopwords_list + domain_stopwords

    if text_process != "normal":
        if text_process == "stemming":
            stopwords_list = stemming(stopwords_list)
            stopwords_list = stopwords_list.split(" ")
        elif text_process == "lemmatising":
            stopwords_list = lemmatising(stopwords_list)
            stopwords_list = stopwords_list.split(" ")
        else:
            raise ValueError(
                "text_process should take one of the values: 'normal','stemming', 'lemmatising'."
            )

    return stopwords_list


def str_with_prepared_text(
    data: pd.DataFrame, text_process: str = "normal", filter_var: str = None
) -> str:
    """
    Prepares data for wordcloud creation in the case of not using tf-idf.

    Args:
        data: dataframe with text variable
        text_process: either "normal", "stemming" or "lemmatising". Defaults to "normal".
        filter_var: variable to filter data by

    Returns:
        Data ready for wordcloud.
    """
    if filter_var is not None:
        data_ready_for_wordcloud = data[data[filter_var] == 1]
    else:
        data_ready_for_wordcloud = data.copy()

    if text_process == "normal":
        data_ready_for_wordcloud = data["processed_complaint_summary"]
    elif text_process == "stemming":
        data_ready_for_wordcloud = data["stems"]
    elif text_process == "lemmatising":
        data_ready_for_wordcloud = data["lemmas"]
    else:
        raise ValueError(
            "text_process should take one of the values: 'normal','stemming', 'lemmatising'."
        )

    data_ready_for_wordcloud = " ".join(t for t in data_ready_for_wordcloud)

    return data_ready_for_wordcloud


def prepare_data_for_wordcloud(
    data: pd.DataFrame,
    generate_from_text: bool = True,
    text_process: str = "normal",
    filter_var: str = None,
) -> str | pd.DataFrame:
    """
    Prepares data for wordcloud.

    Args:
        data: dataframe with text variable
        generate_from_text: wether wordcloud will be generated from a string containing all text (True)
           or from a tf-idf matrix (False). Defaults to True.
        text_process: either "normal", "stemming" or "lemmatising". Defaults to "normal".
        filter_var: variable to filter data by

    Returns:
        Data ready for wordcloud (either a string or a pandas dataframe, depending on the value of generated_from_text)
    """
    if generate_from_text:
        data_ready_for_wordcloud = str_with_prepared_text(
            data, text_process, filter_var
        )
    else:
        data_ready_for_wordcloud = compute_tf_idf_dataframe(
            data, text_process, filter_var
        )

    return data_ready_for_wordcloud


if __name__ == "__main__":
    # Get processed RECC data
    recc_data = getters.get_processed_recc_data()

    # creating local path to store figures if it does not exist
    if not os.path.exists(outputs_local_path_figures):
        os.makedirs(outputs_local_path_figures)

    # Setting plotting style
    visualisation_utils.set_plotting_styles()

    # Top tokens and n-grams analysis
    for variant in top_ngrams_variants.keys():
        variant_params = top_ngrams_variants[variant]

        generate_from_text = variant_params["generate_from_text"]
        text_process = variant_params["text_process"]
        max_words = variant_params["max_words"]
        stopwords_list = stopwords_definition(text_process)
        if "filter" in variant_params:
            filter = variant_params["filter"]
            data_ready_for_wordcloud = prepare_data_for_wordcloud(
                recc_data, generate_from_text, text_process, filter_var=filter
            )
        else:
            data_ready_for_wordcloud = prepare_data_for_wordcloud(
                recc_data, generate_from_text, text_process
            )

        visualisation_utils.wordcloud(
            data_ready_for_wordcloud,
            stopwords=stopwords_list,
            variant_name=variant,
            generate_from_text=generate_from_text,
            max_words=max_words,
        )
