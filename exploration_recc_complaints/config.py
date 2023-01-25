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
outputs_local_path_data = "./outputs/data/"
processed_recc_data_filename = "recc_processed_data_2019_2021.csv"
outputs_local_path_figures_descriptive_analysis = (
    "./outputs/figures/descriptive_analysis/"
)
outputs_local_path_figures_keyword_analysis = "./outputs/figures/keyword_analysis/"
outputs_local_path_figures_ngram_analysis = "./outputs/figures/ngram_analysis/"

# Plotting styles, fonts and colours
figure_size_x = 6
figure_size_x_big = 10
figure_size_y = 4
wordcloud_width = 800
wordcloud_height = 800
dpi = 300

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

# Categories short name
categories_short_names = {
    "After-sales (guarantees, workmanship warranties and warranty protection, after-sales support: customer service)": "After sales",
    "Awareness of RECC / Consumer Protection (including staff training)": "Awareness of RECC and consumer protection",
    "Complaints (numbers, handling, procedures)": "Complaints",
    "Completing the installation": "Completing the installation",
    "Contracts and cancellation rights": "Contracts and cancellation rights",
    "Estimates / quotes, including performance estimates and financial incentives": "Estimates and quotes",
    "Finance agreements": "Finance agreements",
    "Marketing and selling": "Marketing and selling",
    "Microgeneration Certification Scheme": "MCS",
    "No category specified": "No category specified",
    "Taking and protection of deposits and advanced payments": "Taking and protection of deposits and advanced payments",
}

# Variantes of expressions in complaints data
variants_same_expression = {
    "air source heat pump (ashp)": "ashp",
    "air source heat pump": "ashp",
    "office of gas and electricity markets": "ofgem",
    "feed-in tariff": "feed in tariff",
    "feed-in tariff (fit)": "feed in tariff",
    "feed in tariff (fit)": "feed in tariff",
    "feed-in tariff (feed in tariff)": "feed in tariff",
    "feed in tariff (feed in tariff)": "feed in tariff",
    "microgeneration certification scheme": "mcs",
    "green homes grant": "ghg",
    "domestic renewable heat incentive": "rhi",
    "renewable heat incentive": "rhi",
    "boiler upgrade scheme": "bus",
    "district network operator": "dno",
}

domain_acronyms_list = ["ashp", "ofgem", "mcs", "ghg", "rhi", "bus", "dno", "recc"]

# Keywords and expressions organised in groups
keywords_expressions = {
    "Issues": [
        "noise",
        "noises",
        "noisy",
        "damage",
        "damages",
        "damp",
        "mold",
        "moldy",
        "leak",
        "fan",
        "complain",
        "complaint",
        "complaints",
        "complained",
        "issue",
        "issues",
    ],
    "Performance": [
        "condensation",
        "heating",
        "hot water",
        "performance",
        "temperature",
        "cold",
        "weather",
        "weather compensation",
    ],
    "Industry/Schemes": [
        "ofgem",
        "feed in tariff",
        "manufacturer",
        "mcs",
        "ghg",
        "rhi",
        "code",
        "bus",
        "dno",
        "disctrict network",
    ],
    "Advice": ["information", "advice", "advise", "understand"],
    "Finances": [
        "cost",
        "estimate",
        "installation cost",
        "quote",
        "deposit",
        "running costs",
        "bills",
    ],
    "Installation": ["installer", "installation", "installed", "installations"],
}

number_keyword_expressions_to_show = 10

# Domain stopwords
domain_stopwords = [
    "consumer",
    "company",
    "ashp",
    "installation",
    "states",
    "signed",
    "advised",
    "contract",
    "reports",
    "installed",
    "installer",
    "recc",
]
# domain_stopwords = ["consumer", "company", "installation", "states", "contract", "reports", "installed", "installer"]

# Variants for computing and plotting top tokens and n-grams
wordcloud_max_words = 25
ngram_min = 1
ngram_max = 4
top_ngrams_variants = {
    "top_tokens_bigrams": {
        "generate_from_text": True,
        "text_process": "normal",
        "max_words": wordcloud_max_words,
    },
    "top_tokens_bigrams_stems": {
        "generate_from_text": True,
        "text_process": "stemming",
        "max_words": wordcloud_max_words,
    },
    "top_tokens_bigrams_lemmas": {
        "generate_from_text": True,
        "text_process": "lemmatising",
        "max_words": wordcloud_max_words,
    },
    "top_tokens_bigrams_category_estimates": {
        "generate_from_text": True,
        "text_process": "normal",
        "max_words": wordcloud_max_words,
        "filter": "category:Estimates and quotes",
    },
    "top_tokens_bigrams_category_complete_installation": {
        "generate_from_text": True,
        "text_process": "normal",
        "max_words": wordcloud_max_words,
        "filter": "category:Completing the installation",
    },
    "tf_idf_category_estimates": {
        "generate_from_text": False,
        "text_process": "normal",
        "max_words": wordcloud_max_words,
        "filter": "category:Estimates and quotes",
    },
    "tf_idf_category_complete_installation": {
        "generate_from_text": False,
        "text_process": "normal",
        "max_words": wordcloud_max_words,
        "filter": "category:Completing the installation",
    },
}
