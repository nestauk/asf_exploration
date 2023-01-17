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
from sklearn.feature_extraction.text import TfidfVectorizer
from general_utils import stemming, lemmatising

outputs_local_path_figures_ngram_analysis = (
    config.outputs_local_path_figures_ngram_analysis
)
domain_stopwords = config.domain_stopwords
top_ngrams_variants = config.top_ngrams_variants


def stopwords_definition(text_process: str = "normal") -> list:
    """
    Function to define stopwords, by putting together NLTK, gensim,
    as well as domain stopwords. Defaults to "normal".
    If text_process different from "normal", it applies stemming or lemmatising (accordingly).

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


def compute_tf_idf_dataframe(data, text_process, filter_var=None) -> pd.DataFrame:
    """
    Computes tf-idf values.

    Args:
        data: dataframe with data
        text_process: either "normal", "stemming" or "lemmatising". Defaults to "normal".
        filter_var: variable to filter data by

    """
    # checks how text data should be processed
    if text_process == "normal":
        corpus = list(data["processed_complaint_summary"])
    elif text_process == "stemming":
        corpus = list(data["stems"])
    elif text_process == "lemmatising":
        corpus = list(data["lemmas"])
    else:
        raise ValueError(
            "text_process should take one of the values: 'normal','stemming', 'lemmatising'."
        )

    # creates tf-idf dataframe
    vectorizer = TfidfVectorizer(
        norm=None, ngram_range=(config.ngram_min, config.ngram_max), use_idf=False
    )
    x = vectorizer.fit_transform(corpus)
    x_features = vectorizer.get_feature_names_out()
    df_tfidfvect = pd.DataFrame(
        data=x.toarray(), index=data["complaints_reference"], columns=x_features
    )

    # filters tf-idf dataframe when a specific filter_var has value 1
    if filter_var is not None:
        data.set_index("complaints_reference", inplace=True)
        df_tfidfvect[filter_var] = data[filter_var]
        data.reset_index(inplace=True)

        df_tfidfvect = df_tfidfvect[df_tfidfvect[filter_var] == 1]
        df_tfidfvect.drop(filter_var, axis=1)

    # averages tf-idf values so that we have 1 tf-idf value per n-gram
    df_tfidfvect = pd.DataFrame(df_tfidfvect.mean(axis=0))
    df_tfidfvect.columns = ["tf_idf"]

    return df_tfidfvect


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


def generate_wordcloud(data: pd.DataFrame, variant_params: dict):
    """
    Generates wordcloud from data and variant parameters and stores figure.

    Args:
        data: data to generate wordcloud from
        variant_params: parameters
    """
    generate_from_text = variant_params["generate_from_text"]
    text_process = variant_params["text_process"]
    max_words = variant_params["max_words"]
    stopwords_list = stopwords_definition(text_process)

    if "filter" in variant_params:
        filter = variant_params["filter"]
        data_ready_for_wordcloud = prepare_data_for_wordcloud(
            data, generate_from_text, text_process, filter_var=filter
        )
    else:
        data_ready_for_wordcloud = prepare_data_for_wordcloud(
            data, generate_from_text, text_process
        )

    visualisation_utils.wordcloud(
        data_ready_for_wordcloud,
        stopwords=stopwords_list,
        variant_name=variant,
        path=outputs_local_path_figures_ngram_analysis,
        generate_from_text=generate_from_text,
        max_words=max_words,
    )


if __name__ == "__main__":
    # Get processed RECC data
    recc_data = getters.get_processed_recc_data()

    # creating local path to store figures if it does not exist
    if not os.path.exists(outputs_local_path_figures_ngram_analysis):
        os.makedirs(outputs_local_path_figures_ngram_analysis)

    # Setting plotting style
    visualisation_utils.set_plotting_styles()

    # Top tokens and n-grams analysis
    print("N-grams analysis ongoing...\n")
    for variant in top_ngrams_variants.keys():
        variant_params = top_ngrams_variants[variant]
        generate_wordcloud(recc_data, variant_params)
    print(
        "N-grams analysis finished! Results can be seen under {}".format(
            outputs_local_path_figures_ngram_analysis
        )
    )
