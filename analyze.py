import numpy
import pandas
import matplotlib
import sqlalchemy as sqlalc

engine = sqlalc.create_engine('mysql://ght:@127.0.0.1/ghtorrent')

def get_user_id(user_name):
    global engine
    query = "SELECT p.owner_id FROM projects p JOIN users u ON u.id=p.owner_id WHERE u.login=%s LIMIT 1 ;"
    data = pandas.read_sql(query, engine, params = [user_name])
    return data.owner_id[0]

users_data = {}

def load_user(user_name):
    global engine
    query = "SELECT id,login,company,location,created_at,type,fake,deleted,country_code,state,city FROM users WHERE login=%s LIMIT 1 ;"
    data = pandas.read_sql(query, engine, params = [user_name])
    users_data[user_name] = data

def load_projects_by(user_name):
    global engine
    query = "SELECT p.*, u.login FROM projects p JOIN users u ON u.id=p.owner_id WHERE u.login=%s ;"
    print(query % user_name)
    data = pandas.read_sql(query, engine, params = [user_name])
    print(data)

#get_user_id("Vany")

#query = "DESCRIBE users ;"
#data = pandas.read_sql(query, engine)
#print(data)

load_user("Vany")
load_projects_by("Vany")

#data = pandas.read_sql('SELECT * FROM `projects` LIMIT 100;', engine)
#query = 'SELECT * FROM projects WHERE url LIKE "https://github.com/' + "Vany" + '/%" ;'
#print(query)
#print(data)
