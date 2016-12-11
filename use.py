import numpy as np
import pandas as pd
import sqlalchemy as sqlalc
from functools import *

def get_user_id(engine, user_name):
    query = "SELECT p.owner_id FROM projects p JOIN users u ON u.id=p.owner_id WHERE u.login=%s LIMIT 1 ;"
    data = pd.read_sql(query, engine, params = [user_name])
    if len(data) == 0:
        return "-1"
    return data.owner_id[0]

def get_user_matches(user_name, language):
    engine = sqlalc.create_engine('mysql://ght:@127.0.0.1/ghtorrent')

    user_average_commits = pd.read_csv("data/user_average_commits.csv")
    user_languages = pd.read_csv("data/user_languages.csv")
    user_last_activities = pd.read_csv("data/user_last_activities.csv")
    users = pd.read_csv("data/users.csv")
    
    data = pd.merge(left=user_average_commits, right=pd.merge(left=user_languages, right=pd.merge(left=user_last_activities, right=users)))
    
    my_user_id = get_user_id(engine, user_name)
    
    query_commits = "SELECT c.author_id AS id, c.project_id, c.created_at, SUM(1) AS commit_num FROM commits c WHERE id=%s GROUP BY c.author_id, c.project_id ;"
    data_commits = pd.read_sql(query_commits, engine, params = [my_user_id])
    commit_groups = data_commits.groupby('id')
    
    my_average_commits = commit_groups.commit_num.mean()
    
    my_last_activities = commit_groups.created_at.max()
    
    query_users = "SELECT u.id AS id, u.location, u.state, u.city FROM users u WHERE id=%s"
    
    my_user = pd.read_sql(query_users, engine, params = [my_user_id])
    
    k = 0.1
    
    my_average_commits = float(my_average_commits)
    print(data.commit_num - my_average_commits)
    data['sort_data'] = (user_average_commits.commit_num - my_average_commits).abs()
    my_matches = data[data.language.str.contains(language) & (data.login != user_name)]
    my_matches = my_matches.sort_values('sort_data')
    if len(my_matches) == 0:
        return None
    return my_matches.login.iloc[0]

name = input()
lang = input()
print(get_user_matches(name, lang))
