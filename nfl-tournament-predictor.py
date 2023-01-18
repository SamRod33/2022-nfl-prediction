#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import time


# In[2]:


t0 = time.time_ns()
data_name = '2022-nfl-game-by-game-summary'
data_pth = os.path.join('.', f"{data_name}.csv")
data = pd.read_csv(data_pth)
print(f"{(time.time_ns() - t0) * 10**-6 : .2f} ms to load")
data


# In[3]:


# teams that played in NFL 2022 season
assert (np.sort(data['visitor'].unique()) == np.sort(data['home'].unique())).all()
teams = np.sort(data['visitor'].unique())
teams


# In[4]:


# table of N x N representing for each team row, win-likelihood against all other teams
wins_df = pd.DataFrame(0, index=teams, columns= teams)

def inc(visitor, home, visitor_pt, home_pt):
    if np.max([visitor_pt, home_pt]) == 0:
        wins_df.at[visitor, home] += 0
        wins_df.at[home, visitor] += 0
    else:  
        wins_df.at[visitor, home] += visitor_pt / np.max([visitor_pt, home_pt])
        wins_df.at[home, visitor] += home_pt / np.max([visitor_pt, home_pt])

data.apply(lambda row: inc(row['visitor'], row['home'], row['visitor-pts'], row['home-pts']), axis=1)
print()


# In[5]:


playoff_teams = np.sort(np.array(['Los Angeles Chargers', 'Jacksonville Jaguars', 'Miami Dolphins', 
                    'Buffalo Bills', 'Baltimore Ravens', 'Cincinnati Bengals', 
                    'Dallas Cowboys', 'Tampa Bay Buccaneers', 'Seattle Seahawks', 
                    'San Francisco 49ers', 'New York Giants', 'Minnesota Vikings', 
                    'Kansas City Chiefs', 'Philadelphia Eagles']))


# In[6]:


# filter to teams that made the playoffs
wins_df.loc[playoff_teams, playoff_teams]


# In[9]:


# write table out
t0 = time.time_ns()
out_path = os.path.join('.', '2022-playoff-teams-versus-stats.csv')
wins_df.loc[playoff_teams, playoff_teams].to_csv(out_path)
print(f"{(time.time_ns() - t0) * 10**-6 : .2f} ms to write")