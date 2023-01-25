# Exploration of RECC complaints data

The **Renewable Energy Consumer Code (RECC)** shared complaints data on **Air Source Heat Pumps (ASHP)** with the [sustainable future mission](https://www.nesta.org.uk/sustainable-future/#:~:text=Our%20goal%20is%20to%20reduce,comes%20from%20low%2Dcarbon%20sources.) team at Nesta, covering 3 years, from 2019 to 2021. We had a couple of days to look at the data to see if we could extract any insights to inform the **Heat Pump Lifestyle Guides** project. A [summary of results and next steps is in this google docs](https://docs.google.com/document/d/1zfvDfTmx2PlMW8N5y6ori_JAMXN3I60IlZOq_4diisU/edit#) (only accessible by Nesta employees).

## The work we did 📝

The following sections summarise the work done in this exploration.

### RECC complaints data notebook

Jupyter notebook `RECC complaints data` allows you to take a look a the raw and processed datasets.

### Processed RECC data

Run `python3 /exploration_recc_complaints/processing_recc_data.py` to process the data. Processed data is stored under `/asf_exploration/exploration_recc_complaints/outputs/data`.

The script is responsible for **processing data** by performing the following tasks:

- Renaming columns to snake case;
- Extracting month and year from date;
- Processing complaint summary by:
    - Creating new variable with lower case complaint text;
    - Merging together variations of the same expression (e.g. "ASHP" and a"ir source heat pump");
    - Creating a new variable with number of characters in complaint;
    - Creating a variable with the complaint summary tokens.
    - Creating new variables by applying stemming and lemmatising to the complaint summary.
- Creating dummy variables to represent different a complaint belonging to a given category or technology type;
- Creating variables representing the number of categories/technologies.


### Basic descriptive analysis

Run `python3 /exploration_recc_complaints/descriptive_analysis.py` to perform descriptive analysis.

The script is responsible for **descriptive analysis**, with the following plots as outputs:
- Number of complaints per month/year;
- Distribution of complaint lengths;
- Distribution of complaint lengths per year;
- Percentage of complaints per tech type/category;
- Percentage of complaints with a given number of categories/technologies.

Outputs can be seen under `/asf_exploration/exploration_recc_complaints/outputs/figures/descriptive_analysis`.

### Looking at specific keywords and expressions of interest

Run `python3 /exploration_recc_complaints/keyword_analysis.py` to do keyword and expressions analysis. 

The script is responsible for **analysing the presence of specific keywords and expressions of interest to the ASF team** (pre-defined by the team):

- Creates dummy variables representing the keywords and expression defined, as well as groups of these (groups are also pre-defined);
- Creates stats for the above (number and percentage of complaints containing a given keyword or expression/groups of keywords expressions);
- Plots and saves these stats.

Outputs can be seen under `/asf_exploration/exploration_recc_complaints/outputs/figures/keyword_analysis`. The list of keywords and expressions are defined in the `keywords_expressions` dictionary under the `config.py` file.

### Analysing top n-grams in complaints text

Run `python3 /exploration_recc_complaints/top_ngrams_analysis.py` to analyse top tokens and n-grams in complaints data.

The script is responsible for **identifying top n-grams in complaints text**, by performing the following tasks:

- Generates wordclouds of top words and n-grams according to different variants defined in `config.py`, with the possible configurations:
    - Tokens, stemmed tokens or lemmatised tokens;
    - All complaints or a subset of complaints (e.g. top n-grams in a specific category);
    - Frequency (combined with specifying common English stopwords as well as domain stopwords) or using TF-IDF values (combined with specifying common English stopwords).

Outputs can be seen under `/asf_exploration/exploration_recc_complaints/outputs/figures/ngram_analysis`.

Note that we're using NLTK's package to stem/lemmatise tokens and we noticed some problems with NLTK identifying the correct POS tag before stemming/lemmatising (e.g. "has" transformed into "ha" instead of "have"). If taking this work forward, this needs to be improved.

## Set up 🛠️
Open your terminal and follow the instructions:
1. **Clone this repo:** `git clone git@github.com:nestauk/asf_exploration.git`

2. **Navigate to this exploration's folder:** `cd asf_exploration/exploration_recc_complaints`

3. **Create your conda environment:** `conda create --name exploration_recc_complaints python=3.10`

4. **Activate your conda environment:** `conda activate exploration_recc_complaints`

5. **Install package dependencies:** `pip3 install -r requirements.txt`

6. **Add your conda environment to the notebooks:** `python3 -m ipykernel install --user --name=exploration_recc_complaints`