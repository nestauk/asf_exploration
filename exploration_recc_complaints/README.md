# Exploration of RECC complaints data

The **Renewable Energy Consumer Code (RECC)** shared complaints data on **Air Source Heat Pumps (ASHP)** with the [sustainable future mission](https://www.nesta.org.uk/sustainable-future/#:~:text=Our%20goal%20is%20to%20reduce,comes%20from%20low%2Dcarbon%20sources.) team at Nesta, covering 3 years, from 2019 to 2021. We had a couple of days to look at this data to see if we could extract any insights to inform the **Heat Pump Lifestyle Guides** project. A [summary of results and next steps can be is in this google docs](https://docs.google.com/document/d/1zfvDfTmx2PlMW8N5y6ori_JAMXN3I60IlZOq_4diisU/edit#) (only accessible by Nesta employees).

## The work we did 📝

- **Processed RECC data**

Run `python3 /exploration_recc_complaints/processing_recc_data.py` to process the data. Processed data is stored under `/asf_exploration/exploration_recc_complaints/outputs/data`

- **Basic descriptive analysis**

Run `python3 /exploration_recc_complaints/descriptive_analysis.py` to do descriptive analysis. Outputs can be seen under `/asf_exploration/exploration_recc_complaints/outputs/figures`

- **Looking at specific keywords and expressions of interest**

Run `python3 /exploration_recc_complaints/keyword.py` to do keyword and expressions analysis. Outputs can be seen under `/asf_exploration/exploration_recc_complaints/outputs/figures`

- **Analysing top n-grams in complaints text**

Run `python3 /exploration_recc_complaints/top_ngrams_analysis.py` to analyse top tokens and n-grams in complaints data. Outputs can be seen under `/asf_exploration/exploration_recc_complaints/outputs/figures`

- **RECC complaints data**

Jupyter notebook `RECC complaints data` allows you to take a look a the raw and processed datasets.

## Set up 🛠️
Open your terminal and follow the instructions:
1. **Clone this repo:** `git clone git@github.com:nestauk/asf_exploration.git`

2. **Navigate to this exploration's folder:** `cd asf_exploration/exploration_recc_complaints`

3. **Create your conda environment:** `conda create --name exploration_recc_complaints python=3.9`

4. **Activate your conda environment:** `conda activate exploration_recc_complaints`

5. **Install package dependencies:** `pip3 install -r requirements.txt`

6. **Add your conda environment to the notebooks:** `python3 -m ipykernel install --user --name=exploration_recc_complaints`