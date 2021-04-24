"""
This file creates the dataframes containing player stats needed for salary_prediction.py

All Excel sheets are downloaded from NHL.com

Apologies for the repetition in code - I could put this in a function but feeling lazy for now :P
"""

# Imports
import pandas as pd

stats_08_df = pd.read_excel("Data/08Summary.xlsx")
stats_10_df = pd.read_excel("Data/10Summary.xlsx")
stats_11_df = pd.read_excel("Data/11Summary.xlsx")



summary12_1 = pd.read_excel("Data/12Summary1.xlsx")
summary12_2 = pd.read_excel("Data/12Summary2.xlsx")
summary12_3 = pd.read_excel("Data/12Summary3.xlsx")
summary12_4 = pd.read_excel("Data/12Summary4.xlsx")
summary12_5 = pd.read_excel("Data/12Summary5.xlsx")
summary12_6 = pd.read_excel("Data/12Summary6.xlsx")
summary12_7 = pd.read_excel("Data/12Summary7.xlsx")
summary12_8 = pd.read_excel("Data/12Summary8.xlsx")
summary12_9 = pd.read_excel("Data/12Summary9.xlsx")

stats_12_df = pd.concat([summary12_1, summary12_2, summary12_3, summary12_4,
                         summary12_5, summary12_6, summary12_7, summary12_8,
                         summary12_9])
stats_12_df.drop_duplicates(subset='Player', keep='first', inplace=True)
stats_12_df = stats_12_df.reset_index()

summary14_1 = pd.read_excel("Data/14Summary1.xlsx")
summary14_2 = pd.read_excel("Data/14Summary2.xlsx")
summary14_3 = pd.read_excel("Data/14Summary3.xlsx")
summary14_4 = pd.read_excel("Data/14Summary4.xlsx")
summary14_5 = pd.read_excel("Data/14Summary5.xlsx")
summary14_6 = pd.read_excel("Data/14Summary6.xlsx")
summary14_7 = pd.read_excel("Data/14Summary7.xlsx")
summary14_8 = pd.read_excel("Data/14Summary8.xlsx")
summary14_9 = pd.read_excel("Data/Data/14Summary9.xlsx")

nhl_summary14 = pd.concat([summary14_1, summary14_2, summary14_3, summary14_4,
                           summary14_5, summary14_6, summary14_7, summary14_8,
                           summary14_9])
nhl_summary14.drop_duplicates(subset='Player', keep='first', inplace=True)
nhl_summary14 = nhl_summary14.reset_index()

summary15_1 = pd.read_excel("15Summary1.xlsx")
summary15_2 = pd.read_excel("15Summary2.xlsx")
summary15_3 = pd.read_excel("15Summary3.xlsx")
summary15_4 = pd.read_excel("15Summary4.xlsx")
summary15_5 = pd.read_excel("15Summary5.xlsx")
summary15_6 = pd.read_excel("15Summary6.xlsx")
summary15_7 = pd.read_excel("15Summary7.xlsx")
summary15_8 = pd.read_excel("15Summary8.xlsx")
summary15_9 = pd.read_excel("15Summary9.xlsx")

nhl_summary15 = pd.concat([summary15_1, summary15_2, summary15_3, summary15_4,
                           summary15_5, summary15_6, summary15_7, summary15_8,
                           summary15_9])
nhl_summary15 = nhl_summary15.drop_duplicates(subset='Player', keep='first',
                                              inplace=False)
nhl_summary15 = nhl_summary15.reset_index()

summary16_1 = pd.read_excel("16Summary1.xlsx")
summary16_2 = pd.read_excel("16Summary2.xlsx")
summary16_3 = pd.read_excel("16Summary3.xlsx")
summary16_4 = pd.read_excel("16Summary4.xlsx")
summary16_5 = pd.read_excel("16Summary5.xlsx")
summary16_6 = pd.read_excel("16Summary6.xlsx")
summary16_7 = pd.read_excel("16Summary7.xlsx")
summary16_8 = pd.read_excel("16Summary8.xlsx")
summary16_9 = pd.read_excel("16Summary9.xlsx")

nhl_summary16 = pd.concat([summary16_1, summary16_2, summary16_3, summary16_4,
                           summary16_5, summary16_6, summary16_7, summary16_8,
                           summary16_9])
nhl_summary16 = nhl_summary16.drop_duplicates(subset='Player', keep='first',
                                              inplace=False)
nhl_summary16 = nhl_summary16.reset_index()

summary17_1 = pd.read_excel("17Summary1.xlsx")
summary17_2 = pd.read_excel("17Summary2.xlsx")
summary17_3 = pd.read_excel("17Summary3.xlsx")
summary17_4 = pd.read_excel("17Summary4.xlsx")
summary17_5 = pd.read_excel("17Summary5.xlsx")
summary17_6 = pd.read_excel("17Summary6.xlsx")
summary17_7 = pd.read_excel("17Summary7.xlsx")
summary17_8 = pd.read_excel("17Summary8.xlsx")
summary17_9 = pd.read_excel("17Summary9.xlsx")

nhl_summary17 = pd.concat([summary17_1, summary17_2, summary17_3, summary17_4,
                           summary17_5, summary17_6, summary17_7, summary17_8,
                           summary17_9])
nhl_summary17 = nhl_summary17.drop_duplicates(subset='Player', keep='first',
                                              inplace=False)
nhl_summary17 = nhl_summary17.reset_index()

summary18_1 = pd.read_excel("17Summary1.xlsx")
summary18_2 = pd.read_excel("17Summary2.xlsx")
summary18_3 = pd.read_excel("17Summary3.xlsx")
summary18_4 = pd.read_excel("17Summary4.xlsx")
summary18_5 = pd.read_excel("17Summary5.xlsx")
summary18_6 = pd.read_excel("17Summary6.xlsx")
summary18_7 = pd.read_excel("17Summary7.xlsx")
summary18_8 = pd.read_excel("17Summary8.xlsx")
summary18_9 = pd.read_excel("17Summary9.xlsx")

nhl_summary18 = pd.concat([summary18_1, summary18_2, summary18_3, summary18_4,
                           summary18_5, summary18_6, summary18_7, summary18_8,
                           summary18_9])
nhl_summary18 = nhl_summary18.drop_duplicates(subset='Player', keep='first',
                                              inplace=False)
nhl_summary18 = nhl_summary18.reset_index()

summary19_1 = pd.read_excel("19Summary1.xlsx")
summary19_2 = pd.read_excel("19Summary2.xlsx")
summary19_3 = pd.read_excel("19Summary3.xlsx")
summary19_4 = pd.read_excel("19Summary4.xlsx")
summary19_5 = pd.read_excel("19Summary5.xlsx")
summary19_6 = pd.read_excel("19Summary6.xlsx")
summary19_7 = pd.read_excel("19Summary7.xlsx")
summary19_8 = pd.read_excel("19Summary8.xlsx")
summary19_9 = pd.read_excel("19Summary9.xlsx")

nhl_summary19 = pd.concat([summary19_1, summary19_2, summary19_3, summary19_4,
                           summary19_5, summary19_6, summary19_7, summary19_8,
                           summary19_9])
nhl_summary19 = nhl_summary19.drop_duplicates(subset='Player', keep='first',
                                              inplace=False)
nhl_summary19 = nhl_summary19.reset_index()


