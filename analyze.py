import numpy as np
import pandas as pd
import sqlalchemy as sqlalc
from functools import *
import time

engine = sqlalc.create_engine('mysql://ght:@127.0.0.1/ghtorrent')

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

user_id_start = get_user_id("Vany")
user_num = 100
#user_num = 8

user_average_commits = None
user_languages = None
user_last_activities = None
users = None

def load_data(user_id_start, user_num):
    global engine
    global user_average_commits
    global user_languages
    global user_last_activities
    global users
    
    query_commits = "SELECT c.author_id AS id, c.project_id, c.created_at, SUM(1) AS commit_num FROM commits c WHERE c.author_id>=%s AND c.author_id<%s GROUP BY c.author_id, c.project_id ;"
    data_commits = pd.read_sql(query_commits, engine, params = [user_id_start, user_id_start + user_num])
    commit_groups = data_commits.groupby('author_id')
    
    user_average_commits = commit_groups.commit_num.mean()
    
    user_last_activities = commit_groups.created_at.max()
    
    query_projects = "SELECT pm.user_id, pr.language FROM project_members pm JOIN projects pr WHERE pm.user_id>=%s AND pm.user_id<%s AND pm.repo_id=pr.id ;"
    data_projects = pd.read_sql(query_projects, engine, params = [user_id_start, user_id_start + user_num])
    
    user_languages = data_projects.groupby('user_id').language.unique()
    
    query_users = "SELECT u.id, u.location, u.state, u.city FROM users u WHERE u.id>=%s AND u.id<%s"
    users = pd.read_sql(query_users, engine, params = [user_id_start, user_id_start + user_num])

time1 = time.perf_counter()

load_data(user_id_start, user_num)

time2 = time.perf_counter()

#user_data = pd.concat([user_average_commits, user_languages, user_last_activities, users])
#user_data.to_csv("data/user_data.csv", header=True)
user_average_commits.to_csv("data/user_average_commits.csv", header=True)
user_languages.to_csv("data/user_languages.csv", header=True)
user_last_activities.to_csv("data/user_last_activities.csv", header=True)
users.to_csv("data/users.csv", header=True)

time3 = time.perf_counter()

engine.dispose()

print("Loaded")
print("Stage 1: %s sec, %s sec per user" % (str(time2 - time1), str((time2 - time1) / user_num)))
print("Stage 2: %s sec" % (str(time3 - time2)))
