# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: mcs_new_builds
#     language: python
#     name: mcs_new_builds
# ---

# %%
from asf_core_data import get_mcs_installations, load_preprocessed_epc_data

import pandas as pd
import numpy as np

# %%
mcs = get_mcs_installations("full")

# %%
mcs["commission_date"] = pd.to_datetime(mcs["commission_date"])
mcs["INSPECTION_DATE"] = pd.to_datetime(mcs["INSPECTION_DATE"])

# %%
mcs["installation_type"] = mcs["installation_type"].fillna(
    mcs["end_user_installation_type"]
)
mcs = mcs.loc[mcs.installation_type == "Domestic"].reset_index(
    drop=True
)

# %% [markdown]
# ### What proportion of records in the MCS database relate to new-build installations?

# %%
first_records = mcs.sort_values("INSPECTION_DATE").groupby("original_mcs_index").head(1).sort_values("original_mcs_index")

# %%
first_records["diff_epc_to_mcs"] = (
    first_records["commission_date"] - first_records["INSPECTION_DATE"]
).dt.days

# Assume dwelling was built with HP if:
# - first EPC shows it as a new dwelling
# - time difference between EPC inspection when dwelling was built and HP installation is less than 1 year
first_records["assumed_hp_when_built"] = (
    first_records["TRANSACTION_TYPE"] == "new dwelling"
) & (first_records["diff_epc_to_mcs"] < 365)

# %%
first_records.assumed_hp_when_built.value_counts(normalize=True)

# %%
first_records.loc[first_records["assumed_hp_when_built"]]["installer_name"].value_counts().head()

# %%
first_records.groupby("assumed_hp_when_built").cost.mean()

# %% [markdown]
# ### What proportion of properties in the EPC database that were built with a HP appear in the MCS database?

# %%
epc = load_preprocessed_epc_data("/Users/chris.williamson/Documents/ASF_data", version="preprocessed")

# %%
new_hp = epc.loc[(epc["TRANSACTION_TYPE"] == "new dwelling") & (epc["HP_INSTALLED"])]

# %%
new_hp["UPRN"] = new_hp["UPRN"].replace("unknown", np.nan).fillna(0).astype("float").astype("int")
mcs["UPRN"] = mcs["UPRN"].replace("unknown", np.nan).fillna(-1).astype("float").astype("int")

# %%
new_hp["in_mcs"] = new_hp["UPRN"].isin(mcs["UPRN"])

# %%
new_hp["in_mcs"].value_counts(normalize=True)

# %%
mcs.commission_date.max()

# %%
epc.INSPECTION_DATE.max()

# %%
