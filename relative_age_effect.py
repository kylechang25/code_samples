"""
The Relative Age Effect (RAE) describes the “the phenomenon by which children born early in their year of birth perform
more highly than children born later in the same cohort”.

This file creates multiple histograms to determine if RAE impacts the number of players in the NHL and their PPG.
"""

# Imports
import logging as LOGGER
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
import matplotlib.pyplot as plt4
from functions import calculate_quarter, calculate_ppg_by_qtr_yr

# Setup
pd.options.display.max_rows = 500
pd.options.display.max_columns = 500
LOGGER.getLogger().setLevel(LOGGER.INFO)

# Configurations
FILE_NAME = "Data/Bio Info.xlsx"  # all data as of May 4, 2020
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUNE", "JULY", "AUG", "SEPT", "OCT", "NOV", "DEC"]
BIRTH_YEARS = [1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989,
               1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001]
QUARTERS_DICT = {1: "Q1 = Jan-Mar", 2: "Q1 = Jan-Mar", 3: "Q1 = Jan-Mar",
                 4: "Q2 = Apr-Jun", 5: "Q2 = Apr-Jun", 6: "Q2 = Apr-Jun",
                 7: "Q3 = Jul-Sep", 8: "Q3 = Jul-Sep", 9: "Q3 = Jul-Sep",
                 10: "Q4 = Oct-Dec", 11: "Q4 = Oct-Dec", 12: "Q4 = Oct-Dec"}

# Read data
bio_info = pd.read_excel(FILE_NAME)
LOGGER.info(f"Shape of data: {bio_info.shape}")

"""
PART 1: Determine the number of active NHL players born in each month.##################################################
"""

# Create a column in df for birth months and count frequency
bio_info['Birth Months'] = bio_info['DOB'].apply(lambda birthday: birthday.split('-')[1]).astype(int)
month_freq = bio_info['Birth Months'].value_counts().sort_index().tolist()
LOGGER.info("Calculated birth month frequencies")

# Create bar graph
x_index = np.arange(len(MONTHS))
fig, ax = plt.subplots()
frequency_bars = ax.bar(x_index, month_freq, align="center", alpha=0.9)
ax.set_ylim(top=100)
ax.set_xticks(x_index)
ax.set_xticklabels(MONTHS, fontsize=9)
ax.set_ylabel("Number of Active NHL Players")
ax.set_xlabel("Birth Month")
ax.set_title("Plot 1: Birth Months of Active NHL Players")

# Add labels
for i in x_index:
    ax.annotate(str(month_freq[i]),
                xy=(frequency_bars[i].get_x() + 0.4,
                    month_freq[i]),
                xytext=(0, 0),
                textcoords='offset points',
                ha='center',
                va='bottom')
plt.show()
LOGGER.info("Created first bar graph with labels")

"""
PART 2: Points per game by birth month.#################################################################################
"""

# Calculate points per game by birth month
bio_info['Birth Months'] = bio_info['DOB'].apply(lambda birthday: birthday.split('-')[1]).astype(int)
ppg_df = bio_info.groupby('Birth Months').agg({'P': sum, 'GP': sum})
ppg_df['Points per Game'] = ppg_df['P'] / ppg_df['GP']
ppg_month = ppg_df['Points per Game'].tolist()
LOGGER.info("Calculated birth month points per game")

# Create bar graph
x_index2 = np.arange(len(MONTHS))
fig2, ax2 = plt2.subplots()
ppg_bars = ax2.bar(x_index2, ppg_month, align="center", alpha=0.9)
ax2.set_xticks(x_index2)
ax2.set_xticklabels(MONTHS, fontsize=9)
ax2.set_ylabel("Average Points Per Game")
ax2.set_xlabel("Birth Month")
ax2.set_title("Plot 2: Average PPG for Active NHL Players Born in Each Month")

# Add labels
for i in x_index2:
    ax2.annotate(round(ppg_month[i], 2),
                 xy=(ppg_bars[i].get_x() + 0.4,
                     ppg_month[i]),
                 xytext=(0, 0),
                 textcoords='offset points',
                 ha='center',
                 va='bottom')
plt2.show()
LOGGER.info("Created second bar graph with labels")

"""
PART 3: Active players born in each quarter by year.####################################################################
"""

# Create 4 lists showing frequencies of birth quarters per year
q1, q2, q3, q4 = [0] * 25, [0] * 25, [0] * 25, [0] * 25

for birthday in bio_info['DOB'].tolist():
    year = int(birthday[:4])
    month = int(birthday[5:7])
    if month <= 3:
        q1[year - 1977] += 1
    elif month <= 6:
        q2[year - 1977] += 1
    elif month <= 9:
        q3[year - 1977] += 1
    else:
        q4[year - 1977] += 1
LOGGER.info("Calculated frequency of birth quarters per year")

# Create the histogram
x_index3 = np.arange(len(BIRTH_YEARS))
width = 0.15
fig3, ax3 = plt.subplots()
rects1 = ax3.bar(x_index3 - 1.5 * width, q1, width, label="Q1 = Jan-Mar")
rects2 = ax3.bar(x_index3 - width / 2, q2, width, label="Q2 = Apr-Jun")
rects3 = ax3.bar(x_index3 + width / 2, q3, width, label="Q3 = Jul-Sep")
rects4 = ax3.bar(x_index3 + 1.5 * width, q4, width, label="Q4 = Oct-Dec")

ax3.set_xticks(x_index3)
ax3.set_xticklabels(BIRTH_YEARS, fontsize=11)
ax3.set_ylabel("Number of Birthdays")
ax3.set_yticks(np.arange(0, 45, 5))
ax3.set_xlabel("Birth Year")
ax3.set_title("Plot 3: Active NHL Players Born in Each Quarter by Year")
ax3.legend(prop={'size': 15})
fig3.set_size_inches(18, 10)
plt3.show()
LOGGER.info("Created third bar graph with labels")

"""
PART 4: Points per game of active players born in each quarter by year.#################################################
"""

# Calculate a player's birth quarter and year. calculate_quarter is defined in functions.py
bio_info['Birth Quarter'] = bio_info['DOB'].apply(lambda dob: calculate_quarter(dob))
bio_info['Birth Year'] = bio_info['DOB'].apply(lambda dob: int(dob[0:4]))

# Calculate the points per game for every quarter split by year. calculate_ppg_by_qtr_yr is defined in function.py
q1_ppg = calculate_ppg_by_qtr_yr(bio_info, [1977, 2001], "Q1 = Jan-Mar")
q2_ppg = calculate_ppg_by_qtr_yr(bio_info, [1977, 2001], "Q2 = Apr-Jun")
q3_ppg = calculate_ppg_by_qtr_yr(bio_info, [1977, 2001], "Q3 = Jul-Sep")
q4_ppg = calculate_ppg_by_qtr_yr(bio_info, [1977, 2001], "Q4 = Oct-Dec")

# Create the histogram
x_index4 = np.arange(len(BIRTH_YEARS))
width = 0.15
fig4, ax4 = plt.subplots()
rects1 = ax4.bar(x_index4 - 1.5 * width, q1_ppg, width, label="Q1 = Jan-Mar")
rects2 = ax4.bar(x_index4 - width / 2, q2_ppg, width, label="Q2 = Apr-Jun")
rects3 = ax4.bar(x_index4 + width / 2, q3_ppg, width, label="Q3 = Jul-Sep")
rects4 = ax4.bar(x_index4 + 1.5 * width, q4_ppg, width, label="Q4 = Oct-Dec")

ax4.set_xticks(x_index4)
ax4.set_xticklabels(BIRTH_YEARS, fontsize=11)
ax4.set_ylabel("Points per Game")
ax4.set_xlabel("Birth Year")
ax4.set_title("Plot 4: Points Per Game of Active NHL Players Born in Each Quarter by Year")
ax4.legend(prop={'size': 15})
fig4.set_size_inches(18, 10)
plt4.show()
LOGGER.info("Created fourth bar graph with labels")
