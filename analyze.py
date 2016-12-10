import numpy as np
import pandas as pd
import matplotlib
import sqlalchemy as sqlalc
from functools import *

engine = sqlalc.create_engine('mysql://ght:@127.0.0.1/ghtorrent')

users_data = {}
users_languages = {}
projects_datas = []
projects_users = []

#from http://stackoverflow.com/questions/34411495/pandas-merge-several-dataframes
def my_merge(dfs):
    cols, rows = [], []
    for df_i in dfs:
        cols = cols + df_i.columns.tolist()
        rows = rows + df_i.index.tolist()
    cols = np.unique(cols)
    rows = np.unique(rows)       
    df = pd.DataFrame(data=np.NaN, columns=cols, index=rows) 

    for df_i in dfs:
        df.loc[df_i.index, df_i.columns] = df_i.values
    return df

def get_user_name(user_id):
    global engine
    query = "SELECT login FROM users WHERE id=%s LIMIT 1 ;"
    data = pd.read_sql(query, engine, params = [user_id])
    if len(data) == 0:
        return "~INVALID_USER"
    return data.login[0]

def get_user_id(user_name):
    global engine
    query = "SELECT p.owner_id FROM projects p JOIN users u ON u.id=p.owner_id WHERE u.login=%s LIMIT 1 ;"
    data = pd.read_sql(query, engine, params = [user_name])
    if len(data) == 0:
        return "-1"
    return data.owner_id[0]

def load_user(user_name):
    global engine
    global users_data
    
    if user_name in users_data:
        return
    query = "SELECT id,login,company,location,created_at,type,fake,deleted,country_code,state,city FROM users WHERE login=%s LIMIT 1 ;"
    data = pd.read_sql(query, engine, params = [user_name])
    
    if len(data) == 0:
        return
    
    users_data[user_name] = data
    users_languages[user_name] = set()

def load_projects_by(user_name):
    global engine
    global projects_datas
    global users_data
    global users_languages
    
    if not user_name in users_data:
        load_user(user_name)
    
    query = "SELECT p.*, u.login FROM projects p JOIN users u ON u.id=p.owner_id WHERE u.login=%s ;"
    data = pd.read_sql(query, engine, params = [user_name])
    
    if len(data) == 0:
        return
    
    for idx, row in data.iterrows():
        users_languages[user_name].add(row.language)
    
    projects_datas += [data]

#get_user_id("Vany")

user_id_start = get_user_id("Vany")
for user_id in range(user_id_start, user_id_start + 10):
    user_name = get_user_name(user_id)
    if user_name == "~INVALID_USER":
        continue
    load_user(user_name)
    load_projects_by(user_name)

projects_data = my_merge(projects_datas)

print("!")
print(projects_datas)
print("!")
print(projects_data)
print("!")
print(users_languages)
