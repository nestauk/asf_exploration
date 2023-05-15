# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: imd_for_gb
#     language: python
#     name: imd_for_gb
# ---

# %% [markdown]
# # Organising IMD Data
#
# ----
#
#
# ## Wales IMD

# %%
import pandas as pd
import numpy as np
from ipywidgets import interact

# %%
wales_postcode = pd.read_csv("inputs/wales/Postcode to WIMD Lookup - Welsh_Postcodes.csv")
wales_deciles = pd.read_csv("inputs/wales/welsh-index-multiple-deprivation-2019-index-and-domain-ranks-by-small-area - Deciles_quintiles_quartiles.csv")
wales_ranks = pd.read_csv("inputs/wales/welsh-index-multiple-deprivation-2019-index-and-domain-ranks-by-small-area - WIMD_2019_ranks.csv", skiprows=[0,1])
wales_scores = pd.read_csv("inputs/wales/wimd-2019-index-and-domain-scores-by-small-area_0 - Data.csv", skiprows=[0,1])

# %%
print(wales_postcode.columns)
print()
print(wales_deciles.columns)
print()
print(wales_ranks.columns)
print()
print(wales_scores.columns)
print()
print(wales_postcode.shape)
print(wales_deciles.shape)
print(wales_ranks.shape)
print(wales_scores.shape)

# %%
wales_postcode.columns = ["Postcode", "LSOA Code", "LSOA Name", "LSOA Name Cymraeg", "IMD Rank", "IMD Decile", "IMD Quintile", "IMD Quartile"]
wales_postcode.head()

# %%
del wales_ranks['LSOA Name (Eng)']
del wales_ranks['Local Authority Name (Eng)']
del wales_ranks['WIMD 2019 ']
del wales_ranks[' ']

wales_ranks.columns = ['LSOA Code', "Income Rank", 'Employment Rank', 'Health Rank', 'Education Rank', 'Access to Services Rank', 'Housing Rank', 'Community Safety Rank', 'Physical Environment Rank']
wales_ranks.head()

# %%
del wales_scores['LSOA Name']
del wales_scores['Local Authority Name ']

wales_scores.columns = ['LSOA Code', "IMD Score", "Income Score", 'Employment Score', 'Health Score', 'Education Score', 'Access to Services Score', 'Housing Score', 'Community Safety Score', 'Physical Environment Score']
wales_scores.head()

# %%
merged_wales = pd.merge(wales_postcode, wales_ranks, on=["LSOA Code"])
merged_wales.shape

merged_wales = pd.merge(merged_wales, wales_scores, on=["LSOA Code"])
merged_wales.head()

# %%
merged_wales['Country'] = 'Wales'
merged_wales.to_csv('outputs/wales_imd.csv')

# %% [markdown]
# ## Scotland IMD

# %%
scotland_ranks = pd.read_csv("inputs/scotland/SIMD 2020v2 DZ lookup data-Table 1.csv")

scotland_ranks = scotland_ranks[['DZ', 'DZname', 'SIMD2020v2_Rank', 'SIMD2020v2_Vigintile',
       'SIMD2020v2_Decile', 'SIMD2020v2_Quintile',
       'SIMD2020v2_Income_Domain_Rank', 'SIMD2020_Employment_Domain_Rank',
       'SIMD2020_Education_Domain_Rank', 'SIMD2020_Health_Domain_Rank',
       'SIMD2020_Access_Domain_Rank', 'SIMD2020_Crime_Domain_Rank',
       'SIMD2020_Housing_Domain_Rank']]

scotland_ranks.columns = ['DZ', 'DZname', 'IMD Rank', 'IMD Vigintile', 'IMD Decile', 'IMD Quintile', 'Income Rank', 'Employment Rank', 'Education Rank', 'Health Rank', 'Access to Services Rank', 'Community Safety Rank', 'Housing Rank']
scotland_ranks = scotland_ranks.astype({k:'int' for k in scotland_ranks.columns[2:]})

print(scotland_ranks.shape)
scotland_ranks.head()

# %%
scotland_postcodes = pd.read_csv("inputs/scotland/All postcodes-Table 1.csv")[["Postcode", "DZ"]]
scotland_postcodes.head()

# %%
scotland_scores = pd.read_csv("inputs/scotland/postcode_2020_1_all_simd_carstairs.csv", 
                              usecols=['pc8','simd2020v2_emp_rate', 'simd2020v2_inc_rate'])

scotland_scores.columns = [#'DZ',
    'Postcode', 'Employment Score', 'Income Score']

scotland_scores['Employment Score'].replace(r'\s+', np.nan, regex=True, inplace=True)
scotland_scores['Income Score'].replace(r'\s+', np.nan, regex=True, inplace=True)
scotland_scores['Employment Score'] = round(scotland_scores['Employment Score'].astype(float) *100,2)#* 100
scotland_scores['Income Score'] = round(scotland_scores['Income Score'].astype(float) *100,2)

print(scotland_scores.shape)
scotland_scores.head()

# %%
# Example
scotland_scores.loc[scotland_scores['Postcode'] == 'G22 6AB'].head()

# %%
print(scotland_ranks.shape)
print(scotland_postcodes.shape)
print(scotland_scores.shape)

merged_scotland = pd.merge(scotland_ranks, scotland_postcodes, on=["DZ"])
print(merged_scotland.shape)

merged_scotland = pd.merge(merged_scotland, scotland_scores, on=["Postcode"])
print(merged_scotland.shape)
merged_scotland.head()

merged_scotland['Country'] = 'Scotland'
merged_scotland.to_csv('outputs/scotland_imd.csv')
merged_scotland.head(100)

# %% [markdown]
# ## England IMD

# %%
england_all = pd.read_csv("inputs/england/File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv")

england_all = england_all[['LSOA code (2011)', 'LSOA name (2011)', 
                                 'Index of Multiple Deprivation (IMD) Score', 'Index of Multiple Deprivation (IMD) Rank (where 1 is most deprived)', 'Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)', 
                                 'Income Score (rate)', 'Income Rank (where 1 is most deprived)', 'Income Decile (where 1 is most deprived 10% of LSOAs)', 'Employment Score (rate)', 'Employment Rank (where 1 is most deprived)', 
                                 'Employment Decile (where 1 is most deprived 10% of LSOAs)', 'Education, Skills and Training Score', 'Education, Skills and Training Rank (where 1 is most deprived)', 'Education, Skills and Training Decile (where 1 is most deprived 10% of LSOAs)', 
                                 'Health Deprivation and Disability Score', 'Health Deprivation and Disability Rank (where 1 is most deprived)', 'Health Deprivation and Disability Decile (where 1 is most deprived 10% of LSOAs)', 
                                 'Crime Score', 'Crime Rank (where 1 is most deprived)', 'Crime Decile (where 1 is most deprived 10% of LSOAs)', 
                                 'Barriers to Housing and Services Score', 'Barriers to Housing and Services Rank (where 1 is most deprived)', 'Barriers to Housing and Services Decile (where 1 is most deprived 10% of LSOAs)', 
                                 'Living Environment Score', 'Living Environment Rank (where 1 is most deprived)', 'Living Environment Decile (where 1 is most deprived 10% of LSOAs)']]

england_all.columns = ["LSOA Code", "LSOA Name", "IMD Score", "IMD Rank", "IMD Decile", 
                          "Income Score", "Income Rank", "Income Decile", 
                          "Employment Score", "Employment Rank", "Employment Decile", 
                          "Education Score", "Education Rank", "Education Decile", 
                          "Health Score", "Health Rank", "Health Decile", 
                          "Community Safety Score", "Community Safety Rank", "Community Safety Decile", 
                          "Access to Services  Score", "Access to Services  Rank", "Access to Services  Decile", 
                          "Housing and Physical Environment Score", "Housing and Physical Environment Rank", "Housing and Physical Environment Decile"]


england_all['Employment Score'] = england_all['Employment Score'] * 100
england_all['Income Score'] = england_all['Income Score'] * 100


england_all.head()

# %%
postcode_lsoa = pd.read_csv("inputs/england/PCD_OA_LSOA_MSOA_LAD_AUG19_UK_LU.csv", encoding='ISO-8859-1')[["pcds", "lsoa11cd"]]
postcode_lsoa.columns = ['Postcode', 'LSOA Code']
postcode_lsoa.head()

# %%
merged_england = pd.merge(england_all, postcode_lsoa, on=["LSOA Code"])
merged_england.head()

# %%
merged_england['Country'] = 'England'
merged_england.to_csv('outputs/england_imd.csv')

# %% [markdown]
# ## Inspect the IMD for England, Wales and Scotland
#
# Note that the available features for the different nations are different. The min and max values are not suitable for all features. 

# %%
country_df_dict = {'England': merged_england, 'Wales': merged_wales, 'Scotland': merged_scotland}

england_imd = country_df_dict['England']

@interact(feature=england_imd.columns)
def england_imd_inspection(feature):

    print('Feature:', feature)

    if len(england_imd[feature].unique()) <= 10:
        print('Unique values:', england_imd[feature].unique())
        print()
        print('Value counts:')
        print(england_imd[feature].value_counts(dropna=False))
        print()
    
    print('Max:', england_imd[feature].max())
    print('Min:', england_imd[feature].min())


# %%
wales_imd = country_df_dict['Wales']

@interact(feature=merged_wales.columns)
def wales_imd_inspection(feature):

    print('Feature:', feature)

    if len(wales_imd[feature].unique()) <= 10:
        print('Unique values:', wales_imd[feature].unique())
        print()
        print('Value counts:')
        print(wales_imd[feature].value_counts(dropna=False))
        print()
    
    print('Max:', wales_imd[feature].max())
    print('Min:', wales_imd[feature].min())


# %%
scotland_imd = country_df_dict['Scotland']

@interact(feature=scotland_imd.columns)
def scotland_imd_inspection(feature):

    print('Feature:', feature)
    
    if len(scotland_imd[feature].unique()) <= 10:
        print('Unique values:', scotland_imd[feature].unique())
        print()
        print('Value counts:')
        print(scotland_imd[feature].value_counts(dropna=False))
        print()
    
    print('Max:', scotland_imd[feature].max())
    print('Min:', scotland_imd[feature].min())

# %%
