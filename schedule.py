"""
This file outputs an Excel file listing the number of games that every pair of NHL teams have on separate days.

The purpose is to identify the teams that play on the same day the least so I don't pick goalies that always play on
the same day for the KR fantasy league.
"""

# Imports and setup
import logging as LOGGER
import pandas as pd
import requests

LOGGER.getLogger().setLevel(LOGGER.INFO)

# Configurations
teams_info = [["ANA", 'https://www.espn.com/nhl/team/schedule/_/name/ana'],
              ["ARI", 'https://www.espn.com/nhl/team/schedule/_/name/ari'],
              ["BOS", 'https://www.espn.com/nhl/team/schedule/_/name/bos'],
              ["BUF", 'https://www.espn.com/nhl/team/schedule/_/name/buf'],
              ["CAR", 'https://www.espn.com/nhl/team/schedule/_/name/car'],
              ["CGY", 'https://www.espn.com/nhl/team/schedule/_/name/cgy'],
              ["CHI", 'https://www.espn.com/nhl/team/schedule/_/name/chi'],
              ["CBJ", 'https://www.espn.com/nhl/team/schedule/_/name/cbj'],
              ["COL", 'https://www.espn.com/nhl/team/schedule/_/name/col'],
              ["DAL", 'https://www.espn.com/nhl/team/schedule/_/name/dal'],
              ["DET", 'https://www.espn.com/nhl/team/schedule/_/name/det'],
              ["EDM", 'https://www.espn.com/nhl/team/schedule/_/name/edm'],
              ["FLA", 'https://www.espn.com/nhl/team/schedule/_/name/fla'],
              ["LAK", 'https://www.espn.com/nhl/team/schedule/_/name/la'],
              ["MIN", 'https://www.espn.com/nhl/team/schedule/_/name/min'],
              ["MTL", 'https://www.espn.com/nhl/team/schedule/_/name/mtl'],
              ["NSH", 'https://www.espn.com/nhl/team/schedule/_/name/nsh'],
              ["NJD", 'https://www.espn.com/nhl/team/schedule/_/name/njd'],
              ["NYI", 'https://www.espn.com/nhl/team/schedule/_/name/nyi'],
              ["NYR", 'https://www.espn.com/nhl/team/schedule/_/name/nyr'],
              ["OTT", 'https://www.espn.com/nhl/team/schedule/_/name/ott'],
              ["PHI", 'https://www.espn.com/nhl/team/schedule/_/name/phi'],
              ["PIT", 'https://www.espn.com/nhl/team/schedule/_/name/pit'],
              ["SJS", 'https://www.espn.com/nhl/team/schedule/_/name/sj'],
              ["STL", 'https://www.espn.com/nhl/team/schedule/_/name/stl'],
              ["TBL", 'https://www.espn.com/nhl/team/schedule/_/name/tb'],
              ["TOR", 'https://www.espn.com/nhl/team/schedule/_/name/tor'],
              ["VAN", 'https://www.espn.com/nhl/team/schedule/_/name/van'],
              ["VGK", 'https://www.espn.com/nhl/team/schedule/_/name/vgs'],
              ["WPG", 'https://www.espn.com/nhl/team/schedule/_/name/wpg'],
              ["WSH", 'https://www.espn.com/nhl/team/schedule/_/name/wsh']]


def non_overlapping_games(T1, T2, url1, url2):
    '''
    Calculates the number of non overlapping games between two teams
    :param T1 (str): 3 letter abbreviation of first team
    :param T2 (str): 3 letter abbreviation of second team
    :param url1 (str): url for the first team's schedule
    :param url2 (str): url for the second team's schedule
    :return: integer representing the number of non overlapping games
    '''
    # grab the schedules from the two teams
    T1url = url1
    T2url = url2
    html1 = requests.get(T1url).content
    html2 = requests.get(T2url).content
    df1_list = pd.read_html(html1)
    df2_list = pd.read_html(html2)
    df1 = df1_list[-1]
    df2 = df2_list[-1]

    new_header = df1.iloc[0]  # grab the first row for the header
    df1 = df1[1:]  # take the data less the header row
    df1.columns = new_header  # set the header row as the df header

    new_header = df2.iloc[0]
    df2 = df2[1:]
    df2.columns = new_header

    dates1 = list(df1["DATE"])
    dates2 = list(df2["DATE"])

    overlapping_games = 0

    # Loop through the first team's schedule to count number of overlapping games
    for date in dates1:
        if date in dates2:
            overlapping_games = overlapping_games + 1

    return 112 - overlapping_games  # since the season is 56 games long, 112 is the max number of non overlapping games


columns = ["Teams", "# Non-Overlapping Games"]
final_df = pd.DataFrame(columns=columns)

# Loop through every combination of teams and store the number of non overlapping games in final_df
for team1_info in teams_info:
    i1 = teams_info.index(team1_info)
    subteams = teams_info[i1 + 1:]
    for team2_info in subteams:
        i2 = subteams.index(team2_info)
        df_col1 = teams_info[i1][0] + " & " + subteams[i2][0]
        df_col2 = non_overlapping_games(teams_info[i1][0], subteams[i2][0], teams_info[i1][1], subteams[i2][1])
        final_df = final_df.append({'Teams': df_col1, '# Non-Overlapping Games': df_col2}, ignore_index=True)
    LOGGER.info(f"Finished {team1_info}")

# Save to excel
final_df.to_excel('Non Overlapping Games for 2 NHL Teams (2020-2021).xlsx')
LOGGER.info(f"Finished writing dataframe to excel")
