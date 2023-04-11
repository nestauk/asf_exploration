# Index for Multiple Deprivation

This repo contains rudimentary code for loading relevant information from various Index of Multiple Deprivation (IMD) data sources for the three nations England, Wales and Scotland. It generates one IMD output file for each nation: `england_imd.csv`, `wales_imd.csv` and `scotland_imd.csv`.

Note that the code merely loads, filters and concatenates datasets, while also renaming some columns for consistency. It is **not a complete processing** pipeline for IMD data. 

**Note that the scores/ranks are not always comparable across nations since they are based on slightly different factors** [[see also this paper](https://www.researchgate.net/profile/Gary-Abel/publication/221696538_UK_indices_of_multiple_deprivation_-_A_way_to_make_comparisons_across_constituent_countries_easier/links/00b7d52c552a036655000000/UK-indices-of-multiple-deprivation-A-way-to-make-comparisons-across-constituent-countries-easier.pdf)]. Even if they show the same column name, they may not represent exactly the same. However, we have found that Income and Employment are computed very similary for England, Wales and Scotland, so we have used these measures for example in predictive models.  

You can find more information and notes on IMD for GB in this inofficial [document](https://docs.google.com/document/d/1juwDmIBhXCrml6-C1yF8qd2vyRXeaE93lJPwO_IxjX0/edit#heading=h.csycwr7foff0).

## To Do's

This code should not be considered polished or in any way complete. There are many things one could tackle when there is time for it:

- Update with the most recent IMD data sources for all nations (currently 2019 and 2020)
- Refactoring
- Develop a proper processing pipeline
- Analyse further which ranks and scores are comparable across nations
- Integrate the code and/or its outputs into asf-core-data or asf-daps


## How to get started

Clone or update repo

- ```git clone https://github.com/nestauk/asf_exploration.git``` OR
- ```cd asf_exploration``` and ```git pull``` 

```
git checkout 12_imd_for_gb
cd imd_for_gb
```

Create and activate conda enviroment

```
conda create --name imd_for_gb --file requirements.txt
conda activate imd_for_gb
```

Prepare ipykernel

```
conda install -c anaconda ipykernel
python -m ipykernel install --user --name=imd_for_gb
```

Download inputs data 

```
aws s3 sync s3://asf-exploration/imd_for_gb/inputs ./inputs
```