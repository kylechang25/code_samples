"""
This file attempts to predict player salaries based on various statistics from NHL.com using linear regression.

To summarize the methodology: this script will take the statistics of every skater's *signing* year and then
statsmodels will perform a linear regression to predict salary.

To simplify the model and improve accuracy, we will take the statistics from the most recent 82 game
season. This means if a player was signed in 2013 (lockout shortened year), we will use their 2011-12 totals.
For the 2019-20 and 2020-21 seasons, we will use the player's 2018-19 data.
"""

# Imports
import logging as LOGGER
import requests
import pandas as pd
import itertools

from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from statsmodels.tools.eval_measures import meanabs
from functions import create_summary_df

# Setup
pd.options.display.max_rows = 500
pd.options.display.max_columns = 500
LOGGER.getLogger().setLevel(LOGGER.INFO)

# Configurations
SALARY_URL = 'https://www.spotrac.com/nhl/contracts/sort-value/limit-1690/'
STATS_YEAR_DICT = {2013: 2012, 2020: 2019, 2021: 2019, 2022: 2019}

"""
PART 1: Data Prep ######################################################################################################
"""

# Scrape the contents of the website
html = requests.get(SALARY_URL).content
salaries_list = pd.read_html(html)
salaries_df = salaries_list[-1]
LOGGER.info("Successfully pulled salary information from online")

"""
First, we identify the player's signing year given the website's data.

Note that the "Player" column in salaries_df has the following format:
"FIRSTNAME LASTNAME POSITION | SIGNINGYEAR-YYYY (FA: YYYY)"
We want to grab SIGNINGYEAR for every player.

To do this, we use the following methodology:
1) Split the string by '-', which produces a list. Note this list does not necessarily have a length of 2 because there
can be dashes in the player's name (ie. Oliver Ekman-Larsson)
2) Take the second last element in the list because it will contain the signing year. We do this by slicing [-2:-1]
This step returns a single element list. To only grab the string within the list, we write [0]
3) Take the last 4 characters of the list with [-4:0] and this will return the year.
"""

salaries_df['Signing Year'] = salaries_df['Player'].apply(lambda info: (((info.split('-'))[-2:-1])[0])[-4:]).astype(int)
LOGGER.info("Finished creating a column for signing year")

# Stats year will be the column that indicates what season we should take stats from (to account for shortened seasons)
salaries_df['Stats Year'] = salaries_df['Signing Year'].map(STATS_YEAR_DICT).fillna(salaries_df['Signing Year'])
LOGGER.info("Finished creating a column for stats year")

# Replace the player column with only the player's first and last name - we will use this column as a merge key.
salaries_df['Player'] = salaries_df['Player'].apply(lambda info: (info.split(" "))[0] + " " + (info.split(" "))[1])
LOGGER.info("Finished creating a column for player names")

# NHL stats for 2008-2019
# We don't need all of the 08-11 data because the players in salaries_df with a signing year in 08-11 are included
# in the first few pages.
stats_08_df = pd.read_excel("Data/08Summary.xlsx")
stats_08_df['Year'] = 2008
stats_09_df = pd.read_excel("Data/09Summary.xlsx")
stats_09_df['Year'] = 2009
stats_10_df = pd.read_excel("Data/10Summary.xlsx")
stats_10_df['Year'] = 2010
stats_11_df = pd.read_excel("Data/11Summary.xlsx")
stats_11_df['Year'] = 2011
stats_12_df = create_summary_df('12')  # create_summary_df is defined in functions.py
stats_14_df = create_summary_df('14')
stats_15_df = create_summary_df('15')
stats_16_df = create_summary_df('16')
stats_17_df = create_summary_df('17')
stats_18_df = create_summary_df('18')
stats_19_df = create_summary_df('19')

all_stats_df = pd.concat([stats_08_df, stats_09_df, stats_10_df, stats_11_df, stats_12_df, stats_14_df, stats_15_df,
                          stats_16_df, stats_17_df, stats_18_df, stats_19_df])
LOGGER.info("Finished merging NHL statistics from 2008-2019")

# Merge salaries_df and all_stats_df
reg_data_df = salaries_df[['Player', 'Stats Year', 'Signed Age', 'AAV']].merge(all_stats_df, how='inner',
                                                                               left_on=['Player', 'Stats Year'],
                                                                               right_on=['Player', 'Year'])
LOGGER.info("Finished merging salaries and statistics")

# Clean the AAV column by removing dollar signs and commas. Divide by 1 million to simplify values.
reg_data_df['AAV'] = reg_data_df['AAV'].apply(lambda aav: (int("".join(aav.strip("$").split(","))) / 1000000))

# Convert TOI/GP to an integer value
reg_data_df['TOI/GP'] = reg_data_df['TOI/GP'].apply(
    lambda time: int(time.split(":")[0]) + (int(time.split(":")[1]) / 60))

# Replace invalid shooting percentage
reg_data_df['S%'].replace({'--': 0}, inplace=True)

# Replace invalid faceoff percentage
reg_data_df['FOW%'].replace({'--': 0}, inplace=True)

# Drop index column
reg_data_df.drop(columns=['index'], inplace=True)

# Convert signed age to integer
reg_data_df['Signed Age'] = reg_data_df['Signed Age'].astype(int)
LOGGER.info("Finished cleaning columns for modelling")

"""
PART 2: Linear Regression Modeling #####################################################################################

We have the following options as potential model features from our dataset:

['Signed Age', 'GP', 'G', 'A', 'P', '+/-', 'PIM', 'P/GP', 'EVG', 'EVP', 'PPG', 'PPP', 'SHG', 'SHP', 'OTG', 'GWG', 
'S', 'S%', 'TOI/GP', 'FOW%']

I understand that the code for the lin regression can be condensed into a function - but I wanted to maintain visibility
for the readers.
"""

salary_values = reg_data_df['AAV'].values  # target for model

# INITIAL MODEL ########################################################################################################
# Note that the initial model only used stats from the 2018-2019 season.
# To replicate results as discussed in the analysis, set reg_data_df['Stats Year'] = 2019.

features = ['G', 'A', 'TOI/GP', '+/-', 'PPP', 'GP']

var_train, var_test, sal_train, sal_test = train_test_split(reg_data_df[features].values, salary_values,
                                                            test_size=0.2, random_state=20)  # split data for test/train
lin_model = sm.OLS(sal_train, var_train)
result = lin_model.fit()  # create a model with training set
sal_pred = result.predict(var_test)  # test the model

print(result.summary())
print("Mean Absolute Error: " + str(meanabs(sal_test, sal_pred, axis=0)))

# SECOND MODEL #########################################################################################################
features = ['G', 'A', 'TOI/GP', '+/-', 'PPP', 'GP', 'Signed Age']

var_train, var_test, sal_train, sal_test = train_test_split(reg_data_df[features].values, salary_values,
                                                            test_size=0.2, random_state=20)
lin_model = sm.OLS(sal_train, var_train)
result = lin_model.fit()
sal_pred = result.predict(var_test)

print(result.summary())
print("Mean Absolute Error: " + str(meanabs(sal_test, sal_pred, axis=0)))

# BEST POSSIBLE MODEL ##################################################################################################

# List of possible features - removed SHG, SHP, OTG, GWG because they are too rare to be considered as features and
# it will reduce code run time
possible_features = ['Signed Age', 'GP', 'G', 'A', 'P', '+/-', 'PIM', 'P/GP', 'EVG', 'EVP', 'PPG', 'PPP', 'S', 'S%',
                     'TOI/GP', 'FOW%']
feature_mae_dict = {}

# Loop through all possible features to identify the combination that results in the smallest MAE.
for i in range(1, len(possible_features) + 1):
    for subset in itertools.combinations(possible_features, i):
        features = reg_data_df[list(subset)].values
        var_train, var_test, sal_train, sal_test = train_test_split(features, salary_values, test_size=0.2,
                                                                    random_state=5)

        lin_model = sm.OLS(sal_train, var_train)
        result = lin_model.fit()
        sal_pred = result.predict(var_test)
        mae = meanabs(sal_test, sal_pred, axis=0)
        feature_mae_dict[subset] = mae
    LOGGER.info(f"Finished models for combinations of length {i}")

best_features = list(min(feature_mae_dict, key=feature_mae_dict.get))

var_train, var_test, sal_train, sal_test = train_test_split(reg_data_df[best_features].values, salary_values,
                                                            test_size=0.2, random_state=20)

lin_model = sm.OLS(sal_train, var_train)
result = lin_model.fit()
sal_pred = result.predict(var_test)

print(result.summary())
print("Mean Absolute Error: " + str(meanabs(sal_test, sal_pred, axis=0)))
