"""
This file attempts to predict player salaries based on various statistics from NHL.com using linear regression.

To summarize the methodology: this script will take the statistics of every skater's *signing* year and then
stats models will perform a linear regression to predict salary.

We are taking the signing year statistics rather than current year statistics because the player's season immediately
before signing has a greater impact on salary (sure, there are exceptions due to injury, etc.)

In particular, to simplify the model and improve accuracy, we will take the statistics from the most recent 82 game
season. This means if a player was signed in 2013 (lockout), we will use their 2011-12 totals.
For the 2019-20 and 2020-21 seasons, we will use the 2018-19 data.

Resources:
https://stackoverflow.com/questions/10556048/how-to-extract-tables-from-websites-in-python
https://www.khanacademy.org/math/ap-statistics/inference-slope-linear-regression/inference-slope/v/t-statistic-slope
"""

# Imports
import logging as LOGGER
import requests
import numpy as np
import pandas as pd

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

# Create a handle, page, to handle the contents of the website
html = requests.get(SALARY_URL).content
salaries_list = pd.read_html(html)
salaries_df = salaries_list[-1]

"""
First we identify the player's signing year.

Note that the "Player" column in salaries_df has the following format:
"FIRSTNAME LASTNAME POSITION | SIGNINGYEAR-YYYY (FA: YYYY)"
We want to grab SIGNINGYEAR for every player.

To do this, we use the following methodology:
1) Split the string by '-', which produces a list. Note this list does not necessarily have a length of 2 because there
can be dashes in the player's name (ie. Oliver Ekman-Larsson)
2) Take the second last element in the list because it will contain the signing year. We do this by slicing [-2,:-1]
This step returns a single element list. To only grab the string within the list, we write [0]
3) Take the last 4 characters of the list with [-4:0] and this will return the year.
"""

salaries_df['Signing Year'] = salaries_df['Player'].apply(lambda info: (((info.split('-'))[-2:-1])[0])[-4:]).astype(int)

# Stats year will be the column that indicates what season we should take stats from (to account for shortened seasons)
salaries_df['Stats Year'] = salaries_df['Signing Year'].map(STATS_YEAR_DICT).fillna(salaries_df['Signing Year'])

# Replace the player column with only the player's first and last name.
salaries_df['Player'] = salaries_df['Player'].apply(lambda info: (info.split(" "))[0] + " " + (info.split(" "))[1])

# NHL stats for 2008-2019
# We don't need all of the 08-11 data because the palyers in salaries_df with a signing year in 08-11 are included in
# the top 100 points list so we only need the first spreadsheet.
stats_08_df = pd.read_excel("Data/08Summary.xlsx")
stats_08_df['Year'] = 2008
stats_09_df = pd.read_excel("Data/09Summary.xlsx")
stats_09_df['Year'] = 2009
stats_10_df = pd.read_excel("Data/10Summary.xlsx")
stats_10_df['Year'] = 2010
stats_11_df = pd.read_excel("Data/11Summary.xlsx")
stats_11_df['Year'] = 2011
stats_12_df = create_summary_df('12')
stats_14_df = create_summary_df('14')
stats_15_df = create_summary_df('15')
stats_16_df = create_summary_df('16')
stats_17_df = create_summary_df('17')
stats_18_df = create_summary_df('18')
stats_19_df = create_summary_df('19')

all_stats_df = pd.concat([stats_08_df, stats_09_df, stats_10_df, stats_11_df, stats_12_df, stats_14_df, stats_15_df,
                          stats_16_df, stats_17_df, stats_18_df, stats_19_df])

# Merge salaries_df and all_stats_df
reg_data_df = salaries_df[['Player', 'Stats Year', 'Signed Age', 'AAV']].merge(all_stats_df, how='inner',
                                                                               left_on=['Player', 'Stats Year'],
                                                                               right_on=['Player', 'Year'])

# Clean the AAV column by removing dollar signs and commas. Divide by 1 million to simplify values.
reg_data_df['AAV'] = reg_data_df['AAV'].apply(lambda aav: (int("".join(aav.strip("$").split(",")))/1000000))

# Convert TOI/GP to an integer value
reg_data_df['TOI/GP'] = reg_data_df['TOI/GP'].apply(lambda time: int(time.split(":")[0]) + (int(time.split(":")[1])/60))

# Replace invalid shooting percentage
reg_data_df['S%'].replace({'--':0}, inplace=True)

# Replace invalid faceoff percentage
reg_data_df['FOW%'].replace({'--':0}, inplace=True)

# Convert signed age to integer
reg_data_df['Signed Age'] = reg_data_df['Signed Age'].astype(int)

'''
Select features to include in the model out of the following options:

['Signed Age', 'GP', 'G', 'A', 'P', '+/-', 'PIM', 'P/GP', 'EVG', 'EVP', 'PPG', 'PPP', 'SHG', 'SHP', 'OTG', 'GWG', 
'S', 'S%', 'TOI/GP', 'FOW%']
'''

features = reg_data_df[['G', 'A', 'TOI/GP', '+/-', 'PPP', 'GP', 'Signed Age']].values
salary = reg_data_df['AAV'].values

var_train, var_test, sal_train, sal_test = train_test_split(features,
                                                            salary,
                                                            test_size=0.2,
                                                            random_state=20)

lin_model = sm.OLS(sal_train, var_train)
result = lin_model.fit()
sal_pred = result.predict(var_test)

print(result.summary())
print("Mean Absolute Error: " + str(meanabs(sal_test, sal_pred, axis=0)))
