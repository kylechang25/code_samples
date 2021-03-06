"""
DO NOT RUN. IT WON'T COMPILE.

This code is the old version of salary_prediction.py.
Its purpose is to solely illustrate the progress I've made as a coder in the past year.
"""

import warnings
import requests
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import statsmodels.api as sm
from statsmodels.tools.eval_measures import meanabs

warnings.simplefilter(action='ignore', category=FutureWarning)

# Create a handle, page, to handle the contents of the website
url = 'https://www.spotrac.com/nhl/contracts/sort-value/limit-1690/'
html = requests.get(url).content
df_list = pd.read_html(html)
nhl_salaries = df_list[-1]

# Calculate signing year
signing_years = []
i = 0

while i < nhl_salaries['Yrs'].size:
    fa_date = nhl_salaries['Player'][i].split("(")[1][4:8]
    if "0)" in fa_date:
        fa_date = 2020
    fa_date = int(fa_date)
    signing_year = fa_date - nhl_salaries['Yrs'][i]
    signing_years.append(signing_year)
    i = i + 1

signing_years_array = np.array(signing_years)
nhl_salaries['Year Signed'] = pd.Series(signing_years_array)

# Clean age column
players = []
i = 0

while i < nhl_salaries['Yrs'].size:
    first_name = nhl_salaries['Player'][i].split(" ")[0]
    last_name = nhl_salaries['Player'][i].split(" ")[1]
    name = first_name + " " + last_name
    players.append(name)
    i = i + 1

players_array = np.array(players)
nhl_salaries['Player'] = pd.Series(players_array)

sum0 = pd.read_excel("Sum0 19-20.xlsx")
sum1 = pd.read_excel("Sum1 19-20.xlsx")
sum2 = pd.read_excel("Sum2 19-20.xlsx")
sum3 = pd.read_excel("Sum3 19-20.xlsx")
sum4 = pd.read_excel("Sum4 19-20.xlsx")
sum5 = pd.read_excel("Sum5 19-20.xlsx")
sum6 = pd.read_excel("Sum6 19-20.xlsx")
sum7 = pd.read_excel("Sum7 19-20.xlsx")
sum8 = pd.read_excel("Sum8 19-20.xlsx")

nhl_summary = pd.concat([sum0, sum1, sum2, sum3, sum4, sum5, sum6,
                         sum7, sum8])

nhl_data = pd.merge(nhl_salaries, nhl_summary, on='Player')
nhl_data = nhl_data.drop_duplicates(subset='Player', keep='first',
                                    inplace=False)
nhl_data = nhl_data.reset_index()

nhl_summary08 = pd.read_excel("08Summary.xlsx")
nhl_summary10 = pd.read_excel("10Summary.xlsx")
nhl_summary11 = pd.read_excel("11Summary.xlsx")

summary12_1 = pd.read_excel("12Summary1.xlsx")
summary12_2 = pd.read_excel("12Summary2.xlsx")
summary12_3 = pd.read_excel("12Summary3.xlsx")
summary12_4 = pd.read_excel("12Summary4.xlsx")
summary12_5 = pd.read_excel("12Summary5.xlsx")
summary12_6 = pd.read_excel("12Summary6.xlsx")
summary12_7 = pd.read_excel("12Summary7.xlsx")
summary12_8 = pd.read_excel("12Summary8.xlsx")
summary12_9 = pd.read_excel("12Summary9.xlsx")

nhl_summary12 = pd.concat([summary12_1, summary12_2, summary12_3, summary12_4,
                           summary12_5, summary12_6, summary12_7, summary12_8,
                           summary12_9])
nhl_summary12 = nhl_summary12.drop_duplicates(subset='Player', keep='first',
                                              inplace=False)
nhl_summary12 = nhl_summary12.reset_index()

summary14_1 = pd.read_excel("14Summary1.xlsx")
summary14_2 = pd.read_excel("14Summary2.xlsx")
summary14_3 = pd.read_excel("14Summary3.xlsx")
summary14_4 = pd.read_excel("14Summary4.xlsx")
summary14_5 = pd.read_excel("14Summary5.xlsx")
summary14_6 = pd.read_excel("14Summary6.xlsx")
summary14_7 = pd.read_excel("14Summary7.xlsx")
summary14_8 = pd.read_excel("14Summary8.xlsx")
summary14_9 = pd.read_excel("14Summary9.xlsx")

nhl_summary14 = pd.concat([summary14_1, summary14_2, summary14_3, summary14_4,
                           summary14_5, summary14_6, summary14_7, summary14_8,
                           summary14_9])
nhl_summary14 = nhl_summary14.drop_duplicates(subset='Player', keep='first',
                                              inplace=False)
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

regression_data = pd.DataFrame(columns=['Player', 'Pos', 'GP', 'G', 'A', 'S%',
                                        '+/-', 'TOI/GP', 'AAV', 'PPP', 'S'])

reg_players = []
reg_gp = []
reg_g = []
reg_a = []
reg_s = []
reg_plusmin = []
reg_toi = []
reg_aav = []
reg_pos = []
reg_shots = []
reg_ppp = []

i = 0

while i < nhl_data['Player'].size:
    signing_year = nhl_data['Year Signed'][i]
    player = nhl_data['Player'][i]
    if signing_year == 2008:
        if nhl_summary08.isin([player]).any().any():
            index = int((np.where(nhl_summary08['Player'] == player))[0])
            reg_players.append(nhl_summary08['Player'][index])
            reg_gp.append(nhl_summary08['GP'][index])
            reg_g.append(nhl_summary08['G'][index])
            reg_a.append(nhl_summary08['A'][index])
            reg_s.append(nhl_summary08['S%'][index])
            reg_plusmin.append(nhl_summary08['+/-'][index])
            reg_toi.append(nhl_summary08['TOI/GP'][index])
            reg_pos.append(nhl_summary08['Pos'][index])
            reg_shots.append(nhl_summary08['S'][index])
            reg_ppp.append(nhl_summary08['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2010:
        if nhl_summary10.isin([player]).any().any():
            index = int((np.where(nhl_summary10['Player'] == player))[0])
            reg_players.append(nhl_summary10['Player'][index])
            reg_gp.append(nhl_summary10['GP'][index])
            reg_g.append(nhl_summary10['G'][index])
            reg_a.append(nhl_summary10['A'][index])
            reg_s.append(nhl_summary10['S%'][index])
            reg_plusmin.append(nhl_summary10['+/-'][index])
            reg_toi.append(nhl_summary10['TOI/GP'][index])
            reg_pos.append(nhl_summary10['Pos'][index])
            reg_shots.append(nhl_summary10['S'][index])
            reg_ppp.append(nhl_summary10['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2011:
        if nhl_summary11.isin([player]).any().any():
            index = int((np.where(nhl_summary11['Player'] == player))[0])
            reg_players.append(nhl_summary11['Player'][index])
            reg_gp.append(nhl_summary11['GP'][index])
            reg_g.append(nhl_summary11['G'][index])
            reg_a.append(nhl_summary11['A'][index])
            reg_s.append(nhl_summary11['S%'][index])
            reg_plusmin.append(nhl_summary11['+/-'][index])
            reg_toi.append(nhl_summary11['TOI/GP'][index])
            reg_pos.append(nhl_summary11['Pos'][index])
            reg_shots.append(nhl_summary11['S'][index])
            reg_ppp.append(nhl_summary11['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2012 or signing_year == 2013:
        if nhl_summary12.isin([player]).any().any():
            index = int((np.where(nhl_summary12['Player'] == player))[0])
            reg_players.append(nhl_summary12['Player'][index])
            reg_gp.append(nhl_summary12['GP'][index])
            reg_g.append(nhl_summary12['G'][index])
            reg_a.append(nhl_summary12['A'][index])
            reg_s.append(nhl_summary12['S%'][index])
            reg_plusmin.append(nhl_summary12['+/-'][index])
            reg_toi.append(nhl_summary12['TOI/GP'][index])
            reg_pos.append(nhl_summary12['Pos'][index])
            reg_shots.append(nhl_summary12['S'][index])
            reg_ppp.append(nhl_summary12['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2014:
        if nhl_summary14.isin([player]).any().any():
            index = int((np.where(nhl_summary14['Player'] == player))[0])
            reg_players.append(nhl_summary14['Player'][index])
            reg_gp.append(nhl_summary14['GP'][index])
            reg_g.append(nhl_summary14['G'][index])
            reg_a.append(nhl_summary14['A'][index])
            reg_s.append(nhl_summary14['S%'][index])
            reg_plusmin.append(nhl_summary14['+/-'][index])
            reg_toi.append(nhl_summary14['TOI/GP'][index])
            reg_pos.append(nhl_summary14['Pos'][index])
            reg_shots.append(nhl_summary14['S'][index])
            reg_ppp.append(nhl_summary14['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2015:
        if nhl_summary15.isin([player]).any().any():
            index = int((np.where(nhl_summary15['Player'] == player))[0])
            reg_players.append(nhl_summary15['Player'][index])
            reg_gp.append(nhl_summary15['GP'][index])
            reg_g.append(nhl_summary15['G'][index])
            reg_a.append(nhl_summary15['A'][index])
            reg_s.append(nhl_summary15['S%'][index])
            reg_plusmin.append(nhl_summary15['+/-'][index])
            reg_toi.append(nhl_summary15['TOI/GP'][index])
            reg_pos.append(nhl_summary15['Pos'][index])
            reg_shots.append(nhl_summary15['S'][index])
            reg_ppp.append(nhl_summary15['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2016:
        if nhl_summary16.isin([player]).any().any():
            index = int((np.where(nhl_summary16['Player'] == player))[0])
            reg_players.append(nhl_summary16['Player'][index])
            reg_gp.append(nhl_summary16['GP'][index])
            reg_g.append(nhl_summary16['G'][index])
            reg_a.append(nhl_summary16['A'][index])
            reg_s.append(nhl_summary16['S%'][index])
            reg_plusmin.append(nhl_summary16['+/-'][index])
            reg_toi.append(nhl_summary16['TOI/GP'][index])
            reg_pos.append(nhl_summary16['Pos'][index])
            reg_shots.append(nhl_summary16['S'][index])
            reg_ppp.append(nhl_summary16['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2017:
        if nhl_summary17.isin([player]).any().any():
            index = int((np.where(nhl_summary17['Player'] == player))[0])
            reg_players.append(nhl_summary17['Player'][index])
            reg_gp.append(nhl_summary17['GP'][index])
            reg_g.append(nhl_summary17['G'][index])
            reg_a.append(nhl_summary17['A'][index])
            reg_s.append(nhl_summary17['S%'][index])
            reg_plusmin.append(nhl_summary17['+/-'][index])
            reg_toi.append(nhl_summary17['TOI/GP'][index])
            reg_pos.append(nhl_summary17['Pos'][index])
            reg_shots.append(nhl_summary17['S'][index])
            reg_ppp.append(nhl_summary17['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2018:
        if nhl_summary18.isin([player]).any().any():
            index = int((np.where(nhl_summary18['Player'] == player))[0])
            reg_players.append(nhl_summary18['Player'][index])
            reg_gp.append(nhl_summary18['GP'][index])
            reg_g.append(nhl_summary18['G'][index])
            reg_a.append(nhl_summary18['A'][index])
            reg_s.append(nhl_summary18['S%'][index])
            reg_plusmin.append(nhl_summary18['+/-'][index])
            reg_toi.append(nhl_summary18['TOI/GP'][index])
            reg_pos.append(nhl_summary18['Pos'][index])
            reg_shots.append(nhl_summary18['S'][index])
            reg_ppp.append(nhl_summary18['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    if signing_year == 2019 or signing_year == 2020:
        if nhl_summary19.isin([player]).any().any():
            index = int((np.where(nhl_summary19['Player'] == player))[0])
            reg_players.append(nhl_summary19['Player'][index])
            reg_gp.append(nhl_summary19['GP'][index])
            reg_g.append(nhl_summary19['G'][index])
            reg_a.append(nhl_summary19['A'][index])
            reg_s.append(nhl_summary19['S%'][index])
            reg_plusmin.append(nhl_summary19['+/-'][index])
            reg_toi.append(nhl_summary19['TOI/GP'][index])
            reg_pos.append(nhl_summary19['Pos'][index])
            reg_shots.append(nhl_summary19['S'][index])
            reg_ppp.append(nhl_summary19['PPP'][index])

            index_sal = int((np.where(nhl_data['Player'] == player))[0])
            reg_aav.append(nhl_data['AAV'][index_sal])
        else:
            i = i + 1
    i = i + 1

# Build regression data from lists
players_arr = np.array(reg_players)
regression_data['Player'] = pd.Series(players_arr)
gp_arr = np.array(reg_gp)
regression_data['GP'] = pd.Series(gp_arr)
g_arr = np.array(reg_g)
regression_data['G'] = pd.Series(g_arr)
a_arr = np.array(reg_a)
regression_data['A'] = pd.Series(a_arr)
s_arr = np.array(reg_s)
regression_data['S%'] = pd.Series(s_arr)
plusmin_arr = np.array(reg_plusmin)
regression_data['+/-'] = pd.Series(plusmin_arr)
toi_arr = np.array(reg_toi)
regression_data['TOI/GP'] = pd.Series(toi_arr)
aav_arr = np.array(reg_aav)
regression_data['AAV'] = pd.Series(aav_arr)
pos_arr = np.array(reg_pos)
regression_data['Pos'] = pd.Series(pos_arr)
shots_arr = np.array(reg_shots)
regression_data['S'] = pd.Series(shots_arr)
ppp_arr = np.array(reg_ppp)
regression_data['PPP'] = pd.Series(ppp_arr)

# Clean AAV column
AAVs = []
i = 0

while i < regression_data['AAV'].size:
    AAV = regression_data['AAV'][i].strip("$").split(",")
    AAV = int("".join(AAV))
    AAVs.append(AAV)
    i = i + 1

AAV_array = np.array(AAVs)
regression_data['AAV'] = pd.Series(AAV_array)

regression_data['AAV'] = regression_data['AAV'].divide(other=1000000)

ice_time = []
i = 0

# Fix TOI/GP issue with strings
while i < regression_data['TOI/GP'].size:
    mins = regression_data['TOI/GP'][i].split(":")
    player_time = int(mins[0]) + int(mins[1]) / 60
    ice_time.append(player_time)
    i = i + 1

ice_time_array = np.array(ice_time)
regression_data['TOI/GP'] = pd.Series(ice_time_array)

shootingp = []
i = 0

# Fix S% issue with "--" and multiply S% by 2 if d-man
while i < regression_data['TOI/GP'].size:
    if regression_data['S%'][i] == "--":
        shootingp.append(0)
    else:
        shotp = float(regression_data['S%'][i])
        shootingp.append(shotp)
    if regression_data['Pos'][i] == "D" and regression_data['S%'][i] != "--":
        shootingp.append(float(regression_data['S%'][i]) * 2)
    i = i + 1

shootingp_array = np.array(shootingp)
regression_data['S%'] = pd.Series(shootingp_array)

variables = regression_data[['G', 'A', 'TOI/GP', 'PPP']].values

salary = regression_data['AAV'].values

var_train, var_test, sal_train, sal_test = train_test_split(variables,
                                                            salary,
                                                            test_size=0.2,
                                                            random_state=5)

lin_model = sm.OLS(sal_train, var_train)
result = lin_model.fit()
sal_pred = result.predict(var_test)

print(result.summary())

print("Mean Absolute Error: " + str(meanabs(sal_test, sal_pred, axis=0)))
