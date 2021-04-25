"""
This file stores all functions used in relative_age_effect.py, salary_prediction.py, fantasy_goalies.py
Test
"""

import logging as LOGGER
import pandas as pd

LOGGER.getLogger().setLevel(LOGGER.INFO)


def calculate_quarter(birthday=""):
    '''
    Determines the quarter in which a player was born in given their birthday.
    :param birthday (str): a player's birthday in the form YYYY-MM-DD
    :return: a string describing the quarter the player was born in

    Example:
    calculate_quarter(2021-04-18) -> "Q2 = Apr-Jun"
    '''
    month = int(birthday[5:7])
    if month <= 3:
        return "Q1 = Jan-Mar"
    elif month <= 6:
        return "Q2 = Apr-Jun"
    elif month <= 9:
        return "Q3 = Jul-Sep"
    else:
        return "Q4 = Oct-Dec"


def calculate_ppg_by_qtr_yr(bio_info, year_range, qtr):
    '''
    Creates a list of points per game for every birth year of all players born in a particular quarter.
    :param bio_info (pd.Dataframe): provides the data for games played, points, and birth quarter
    :param year_range [int, int]: the oldest and youngest years of birth, to create the length of the list
    :param qtr (str): the desired quarter, such as "Q1 = Jan-Mar" (must be in this format)
    :return: a list with the points per game
    '''
    # Create dictionaries where the keys are the birth years and values are all 0.
    qtr_total_pts_dict = dict(
        zip(range(year_range[0], year_range[1] + 1), [0] * (year_range[1] - year_range[0] + 1)))
    qtr_total_gp_dict = dict(zip(range(year_range[0], year_range[1] + 1), [0] * (year_range[1] - year_range[0] + 1)))
    qtr_info = bio_info[bio_info['Birth Quarter'] == qtr]

    # Create a list of total points
    pts_df = qtr_info.groupby('Birth Year').agg({'P': sum})

    LOGGER.info(f"Points by year for {qtr}: {pts_df}")

    temp_dict = dict(zip(list(pts_df.index), list(pts_df['P'])))
    for key in list(temp_dict.keys()):
        qtr_total_pts_dict[key] = temp_dict[key]
    qtr_total_pts_list = list(qtr_total_pts_dict.values())

    # Create a list of total games
    gp_df = qtr_info.groupby('Birth Year').agg({'GP': sum})
    LOGGER.info(f"Games by year for {qtr}: {gp_df}")

    temp_dict = dict(zip(list(gp_df.index), list(gp_df['GP'])))
    for key in list(temp_dict.keys()):
        qtr_total_gp_dict[key] = temp_dict[key]
    qtr_total_gp_list = list(qtr_total_gp_dict.values())

    # Calculate PPG given the two lists
    qtr_ppg_list = []
    for i in range(len(qtr_total_gp_list)):
        if qtr_total_gp_list[i] != 0:  # avoid dividing by 0 games played
            qtr_ppg_list.append(qtr_total_pts_list[i] / qtr_total_gp_list[i])
        else:
            qtr_ppg_list.append(0)

    LOGGER.info(f"List of points per game for {qtr}: {qtr_ppg_list}")
    return qtr_ppg_list


def create_summary_df(year):
    '''
    Produces a single dataframe from 9 different Excel files that contain player statistics for the same season
    :param year (str): a two digit string in the form 'YY' indicating the corresponding NHL season for the stats
    :return: a dataframe with all stats in year
    '''
    summary1 = pd.read_excel(f"Data/{year}Summary1.xlsx")
    summary2 = pd.read_excel(f"Data/{year}Summary2.xlsx")
    summary3 = pd.read_excel(f"Data/{year}Summary3.xlsx")
    summary4 = pd.read_excel(f"Data/{year}Summary4.xlsx")
    summary5 = pd.read_excel(f"Data/{year}Summary5.xlsx")
    summary6 = pd.read_excel(f"Data/{year}Summary6.xlsx")
    summary7 = pd.read_excel(f"Data/{year}Summary7.xlsx")
    summary8 = pd.read_excel(f"Data/{year}Summary8.xlsx")
    summary9 = pd.read_excel(f"Data/{year}Summary9.xlsx")

    output_df = pd.concat([summary1, summary2, summary3, summary4, summary5, summary6, summary7, summary8, summary9])
    output_df.drop_duplicates(subset='Player', keep='first', inplace=True)
    output_df.reset_index(inplace=True)
    output_df['Year'] = int(f"20{year}")
    return output_df

def clean_aav(aav_str):
    '''

    :param aav_str:
    :return:
    '''
    AAV = int("".join(aav_str.strip("$").split(",")))
    AAV = int("".join(AAV))
