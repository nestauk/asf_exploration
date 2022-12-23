"""
Utility functions to visualise data.
"""

#package imports
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import pandas as pd
import dataframe_image as dfi
import math
import config

def set_spines():
    """
    Function to add or remove spines from plots.
    """
    mpl.rcParams['axes.spines.left'] = config.left_spine
    mpl.rcParams['axes.spines.right'] = config.right_spine
    mpl.rcParams['axes.spines.top'] = config.top_spine
    mpl.rcParams['axes.spines.bottom'] = config.bottom_spine


def set_plotting_styles():
    """
    Function that sets plotting styles.
    """

    sns.set_context("talk")

    set_spines()

    font_files = font_manager.findSystemFonts(fontpaths=["/Users/anasofiapinto/Library/Fonts/"])

    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    mpl.rcParams['font.family'] = config.font
    mpl.rcParams['xtick.labelsize'] = config.fontsize_normal
    mpl.rcParams['ytick.labelsize'] = config.fontsize_normal
    mpl.rcParams['axes.titlesize'] = config.fontsize_title
    mpl.rcParams['axes.labelsize'] = config.fontsize_normal
    mpl.rcParams["legend.fontsize"] = config.fontsize_normal
    mpl.rcParams["figure.titlesize"] = config.fontsize_title

def pandas_df_to_figure(df:pd.DataFrame, folder:str, figure_name:str):
    """
    Saves pandas DataFrame as a figure.

    Args:
        df: any pandas DataFrame
        folder: folder where the figure is going to be stored
        figure_name: figure name
    """
    dfi.export(df, folder+figure_name)

def max_value_to_show(values:pd.Series) -> list[int]:
    """
    Computes max value to show on plot based on max value found in data
    and order of magnitude.

    Examples:
    1) If max in values is 71, it outputs: 80, 10
    2) If max in values is 4987, it outputs: 5000, 1000
    3) If max in values is 43.2, it outputs: 50, 10
    4) If max in values is 200, it outpus: 200, 100

    Args:
        values: pandas Series with all possible values
    Returns:
        A tuple with max value to show and its order of magnitude
    """
    max_value = int(values.max())
    max_as_string = str(max_value)
    order_magnitude = 10**(len(max_as_string)-1)

    if max_value%10==0:
        max_to_show = max_value
    else:
        max_to_show = (int(max_as_string[0])+1)*order_magnitude

    return [max_to_show, order_magnitude]

def compute_bins(values:pd.Series)->range:
    """
    Automatically computes bins for an histogram given a pandas series with all possible values.

    Args:
        values: pandas Serxxies with all possible values
    Returns:
        The bins as a range.
    """
    bins_max, order_magnitude = max_value_to_show(values)
    bins_increment = math.ceil(order_magnitude/10)

    return range(0, bins_max, bins_increment)

def add_bar_values(bar_values:pd.Series):
    """
    Adds bar values to horizontal bar plots.

    Args:
        bar_values: pandas Series with bar plot values
    """
    max_x = max_value_to_show(bar_values)[0]
    for i, v in enumerate(bar_values):
        round_value = round(v)
        if v==max_x:
            pos_x = v - 0.08*v
        else:
            pos_x = v + 0.05*v
        if round_value<1:
            plt.text(pos_x, i-0.25, "<1%", fontsize=config.fontsize_small)
        else:
            plt.text(pos_x, i-0.25, str(round_value)+"%", fontsize=config.fontsize_small)


def horizontal_bar_plot(data:pd.DataFrame, y_var:str, x_var:str):
    """
    Creates a horizontal bar plot.

    Args:
        data: dataframe containing data to create the bar plot
        y_var: variable in the y axis
        x_var: variable in the x axis/width of the bar plot
    """
    plt.figure(figsize=(config.figure_size_x_big,config.figure_size_y))
    plt.barh(y = data[y_var], width = data[x_var], color = config.default_colour)
    max_x = max_value_to_show(data[x_var])[0]
    plt.xlim(0, max_x)

    if config.display_bar_values:
        add_bar_values(data[x_var])