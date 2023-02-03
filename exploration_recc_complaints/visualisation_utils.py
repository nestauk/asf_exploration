"""
Utility functions to visualise data.
"""

# package imports
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import pandas as pd
import dataframe_image as dfi
import math
import config
from wordcloud import WordCloud
import warnings


def set_spines():
    """
    Function to add or remove spines from plots.
    """
    mpl.rcParams["axes.spines.left"] = config.left_spine
    mpl.rcParams["axes.spines.right"] = config.right_spine
    mpl.rcParams["axes.spines.top"] = config.top_spine
    mpl.rcParams["axes.spines.bottom"] = config.bottom_spine


def set_plotting_styles():
    """
    Function that sets plotting styles.
    """

    sns.set_context("talk")

    set_spines()

    # Had trouble making it find the font I set so this was the only way to do it
    # without specifying the local filepath
    all_font_files = font_manager.findSystemFonts()

    try:
        mpl.rcParams["font.family"] = "sans-serif"
        font_files = [f for f in all_font_files if config.font_type in f]
        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)
        mpl.rcParams["font.sans-serif"] = config.font
    except:
        print(config.font + " font could not be located. Using 'DejaVu Sans' instead")
        font_files = [f for f in all_font_files if "DejaVuSans.ttf" in f][0]
        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)
        mpl.rcParams["font.family"] = "sans-serif"
        mpl.rcParams["font.sans-serif"] = "DejaVu Sans"

    mpl.rcParams["xtick.labelsize"] = config.fontsize_normal
    mpl.rcParams["ytick.labelsize"] = config.fontsize_normal
    mpl.rcParams["axes.titlesize"] = config.fontsize_title
    mpl.rcParams["axes.labelsize"] = config.fontsize_normal
    mpl.rcParams["legend.fontsize"] = config.fontsize_normal
    mpl.rcParams["figure.titlesize"] = config.fontsize_title


def finding_path_to_font(font_name: str):
    """
    Finds path to specific font.
    Args:
        font_name: name of font
    """

    all_font_files = font_manager.findSystemFonts()
    font_files = [f for f in all_font_files if font_name in f]
    if len(font_files) == 0:
        font_files = [f for f in all_font_files if "DejaVuSans.ttf" in f]
    return font_files[0]


def pandas_df_to_figure(df: pd.DataFrame, folder: str, figure_name: str):
    """
    Saves pandas DataFrame as a figure.

    Args:
        df: any pandas DataFrame
        folder: folder where the figure is going to be stored
        figure_name: figure name
    """
    dfi.export(df, folder + figure_name)


def max_value_to_show(values: pd.Series) -> list[int]:
    """
    Computes max value to show on plot based on max value found in data
    and order of magnitude.

    Examples:
    1) If max in values is 71, it outputs: [80, 10]
    2) If max in values is 4987, it outputs: [5000, 1000]
    3) If max in values is 43.2, it outputs: [50, 10]
    4) If max in values is 200, it outpus: [200, 100]

    Args:
        values: pandas Series with all possible values
    Returns:
        A tuple with max value to show and its order of magnitude
    """
    max_value = int(values.max())
    max_as_string = str(max_value)
    order_magnitude = 10 ** (len(max_as_string) - 1)

    if max_value % 10 == 0 and max_value == values.max():
        max_to_show = max_value
    else:
        max_to_show = (int(max_as_string[0]) + 1) * order_magnitude

    return [max_to_show, order_magnitude]


def compute_bins(values: pd.Series) -> range:
    """
    Automatically computes bins for an histogram given a pandas series with all possible values.

    Args:
        values: pandas Series with all possible values
    Returns:
        The bins as a range.
    """
    bins_max, order_magnitude = max_value_to_show(values)
    bins_increment = math.ceil(order_magnitude / 10)

    return range(0, bins_max, bins_increment)


def add_bar_values(bar_values: pd.Series):
    """
    Adds bar values to horizontal bar plots.

    Args:
        bar_values: pandas Series with bar plot values
    """
    max_x = max_value_to_show(bar_values)[0]
    for i, v in enumerate(bar_values):
        round_value = round(v)
        if v == max_x:
            pos_x = v - 0.05 * v
        else:
            pos_x = v + 0.01 * v
        if round_value < 1:
            plt.text(pos_x, i - 0.25, "<1%", fontsize=config.fontsize_small)
        else:
            plt.text(
                pos_x, i - 0.25, str(round_value) + "%", fontsize=config.fontsize_small
            )


def horizontal_bar_plot(data: pd.DataFrame, y_var: str, x_var: str):
    """
    Creates a horizontal bar plot.

    Args:
        data: dataframe containing data to create the bar plot
        y_var: variable in the y axis
        x_var: variable in the x axis/width of the bar plot
    """
    plt.figure(figsize=(config.figure_size_x_big, config.figure_size_y))
    plt.barh(y=data[y_var], width=data[x_var], color=config.default_colour)
    max_x = max_value_to_show(data[x_var])[0]
    plt.xlim(0, max_x)

    if config.display_bar_values:
        add_bar_values(data[x_var])


def plotting_complaints_by_dummies(data: pd.DataFrame, by: str, path: str):
    """
    Plots the number of complaints by a set of dummy variables

    Args:
        data: data frame with number and percentage of of complaints by a set of dummy variables
        by: variables by which we are calculating the percentage of complaints
        path: path to folder where the figure is going to be stored
    """

    data["short_index"] = data["index"].str.split(":").str[1]

    horizontal_bar_plot(data, "short_index", "percent_complaints")
    plt.title("Percentage of complaints by " + by)

    plt.tight_layout()
    plt.savefig(
        path + "complaints_by_" + by.replace(" ", "_") + ".png", dpi=config.dpi,
    )


def wordcloud(
    data: str | pd.DataFrame,
    stopwords: list,
    variant_name: str,
    path: str,
    generate_from_text: bool = True,
    max_words: int = 25,
):
    """
    Generates a wordcloud image and displays generated image.

    Args:
        data: data containing the information to create the wordcloud
        stopwords: list of stopwords
        variant_name: variant name to appear in figure name
        path: path to folder where the figure is going to be stored
        generated_from_text: wether wordcloud will be generated from a string containing all text (True)
           or from a tf-idf matrix (False). Defaults to True.
        max_words: max number of tokens/n-grams to add to the wordcloud
    """
    font_path_ttf = finding_path_to_font(config.font_type)

    wordcloud = WordCloud(
        font_path=font_path_ttf,
        width=config.wordcloud_width,
        height=config.wordcloud_height,
        margin=0,
        collocations=True,
        stopwords=stopwords,
        background_color="white",
        max_words=max_words,
    )
    if generate_from_text:
        wordcloud = wordcloud.generate(data)
    else:
        wordcloud = wordcloud.generate_from_frequencies(
            frequencies=dict(data["tf_idf"])
        )

    # plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(
        path + "wordcloud_" + variant_name + ".png", dpi=config.dpi,
    )
