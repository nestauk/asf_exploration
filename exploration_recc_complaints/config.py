"""
Configuration variables.
"""

# Paths and file names
s3_bucket = "asf-exploration"
s3_path = "exploration_recc_complaints/inputs/"
inputs_local_path = "./inputs/"
raw_recc_data_filename_xlsx = (
    "RECC_Consumer_Complaints_Data_Air_Source_Heat_Pumps_2019-2021.xlsx"
)
raw_recc_data_filename_csv = "recc_consumer_ashp_complaints_2019_2021.csv"
outputs_local_path = "./outputs/"
outputs_local_path_data = outputs_local_path + "data/"
processed_recc_data_filename = "recc_processed_data_2019_2021.csv"
outputs_local_path_figures = outputs_local_path + "figures/"

# Plotting styles, fonts and colours
figure_size_x = 6
figure_size_x_big = 10
figure_size_y = 4
left_spine = True
right_spine = False
top_spine = False
bottom_spine = True
font = "Averta"
title_font = "Averta"
fontsize_title = 16
fontsize_subtitle = 13
fontsize_normal = 13
fontsize_small = 10
nesta_colours = [
    "#0000FF",
    "#FDB633",
    "#18A48C",
    "#9A1BBE",
    "#EB003B",
    "#FF6E47",
    "#646363",
    "#0F294A",
    "#97D9E3",
    "#A59BEE",
    "#F6A4B7",
    "#D2C9C0",
    "#FFFFFF",
    "#000000",
]
default_colour = nesta_colours[2]
display_bar_values = True