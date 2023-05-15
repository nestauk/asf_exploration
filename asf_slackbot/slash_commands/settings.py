# ==== IMPORTS ====

from pathlib import Path

# ================

asana_reminder_text = f"Hello! :wave:\nThis a gentle reminder to complete your project status update on asana for this sprint by COP tomorrow. Here is a <https://docs.google.com/document/d/1cFgVR9Rb24VncTe9ekj6IagusZp-xGSyKW8gN_ss3aE/edit|link> on how to prepare the project status update if needed. :blush:"

asana_preview_text = "Hello! This is a gentle reminder to complete your project status update on Asana..."

asana_reminder_day = "Thursday"
asana_reminder_time = "11:00"

default_members = ["U0155LT0YJF",   # Davinia
                   "U01VB0LVBRB",   # Julia 
                   "URF8X7JM6",     # Olly
                   "U042TCF9PT7",   # Oli B
                   "U0224M68QCS",   # Chris
                   "U02Q4LDST0T",   # Shaan
                   "UCESYHK9V",     # Codrina
                   "U02BPEVD0DQ",   # Andrew Sissons
                   "U02K3PS1FBN",   # Andy R
                   "U02EHE0U81G",   # Alasdair
                   "UGWAF7C7P",     # Genna Barnett
                   "U04UW4AEB7X"    # Sarah Davies 
]

joke_default_topic = "work"
fun_emoji = " :rolling_on_the_floor_laughing:"

hp_data_file = Path('asf_slackbot/epc_mcs_hp_only.csv')
hp_data_columns = ['POSTCODE','BUILT_FORM', 'PROPERTY_TYPE',
       'HP_INSTALLED', 'LATITUDE','LONGITUDE']