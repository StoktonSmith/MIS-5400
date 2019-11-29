# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:46:26 2019

@author: stokt
"""
import pyodbc
from flask import Flask, g, render_template, abort, request
import json

CONNECTION_STRING = 'Driver={ODBC Driver 17 for SQL Server};Server=nba-data.cewblrob7gqp.us-west-1.rds.amazonaws.com,1433;Database=nba-data;Uid=admin;Pwd=Edgehill3;'

# Setup Flask
app = Flask(__name__)
app.config.from_object(__name__)

#Before / Teardown
@app.before_request
def before_request():
    try:
        g.sql_conn =  pyodbc.connect(CONNECTION_STRING, autocommit=True)
    except Exception:
        abort(500, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.sql_conn.close()
    except AttributeError:
        pass

@app.route('/', methods=['GET'])
def root_page():
    return render_template('home.html')
    

@app.route('/NHL_data', methods=['GET'])
def get_team_and_player_data():
    curs = g.sql_conn.cursor()
    query = '''SELECT * FROM [nba-data].[dbo].[Teams_NHL] tm 
                JOIN [nba-data].[dbo].[PLAYERS_NHL] pl 
                on tm.Team_ID = pl.Team_ID'''
    curs.execute(query)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)

#Get All Teams
@app.route('/NHL_teams', methods=['GET'])
def get_team_data():
    curs = g.sql_conn.cursor()
    query = 'SELECT * FROM [nba-data].[dbo].[Teams_NHL]'
    curs.execute(query)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)

#Get All Players
@app.route('/NHL_players', methods=['GET'])
def get_player_data():
    curs = g.sql_conn.cursor()
    query = 'SELECT * FROM [nba-data].[dbo].[PLAYERS_NHL]'
    curs.execute(query)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)

# GET Single team
@app.route('/NHL_teams/<string:id>', methods=['GET'])
def get_single_nhl_team(id):
    curs = g.sql_conn.cursor()
    curs.execute("SELECT * FROM [nba-data].[dbo].[Teams_NHL] where Team_ID = ?", id)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)

# GET Players From a Single Team
@app.route('/NHL_teams/<string:id>/players', methods=['GET'])
def get_single_nhl_team_players(id):
    curs = g.sql_conn.cursor()
    curs.execute("SELECT * FROM [nba-data].[dbo].[PLAYERS_NHL] where Team_ID = ?", id)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)

#Get a Single Player
@app.route('/NHL_players/<string:id>', methods=['GET'])
def get_single_player(id):
    curs = g.sql_conn.cursor()
    curs.execute("SELECT * FROM [nba-data].[dbo].[PLAYERS_NHL] where Player_ID = ?", id)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)

#POST API (Add)
@app.route('/NHL_teams', methods=['POST'])
def insert_new_team():
    data = request.get_json()

    curs = g.sql_conn.cursor()

    query = '''INSERT INTO [nba-data].[dbo].[Teams_NHL] (Team_ID, Team_Name, Venue, City, Short_Name, State, Start_Year, Division, Conference, Website_URL)
                VALUES(?,?,?,?,?,?,?,?,?,?)'''

    if isinstance(data, dict):
        curs.execute(query, data["Team_ID"], data["Team_Name"], data["Venue"], data["City"], data["Short_Name"], data["State"], data["Start_Year"], data["Division"], data["Conference"], data["Website_URL"])
        curs.commit()

    if isinstance(data, list):
        for row in data:
            curs.execute(query, row["Team_ID"], row["Team_Name"], row["Venue"], row["City"], row["Short_Name"], row["State"], row["Start_Year"], row["Division"], row["Conference"], row["Website_URL"])
            curs.commit()

    return 'success', 200

#POST API (Add)
@app.route('/NHL_players', methods=['POST'])
def insert_new_player():
    data = request.get_json()

    curs = g.sql_conn.cursor()

    query = '''INSERT INTO [nba-data].[dbo].[PLAYERS_NHL] (Team_ID, Player_ID, Player_Name, Jersey_Number, Position_Name, Position_Type)
               VALUES (?,?,?,?,?,?)'''

    if isinstance(data, dict):
        curs.execute(query, data["Team_ID"], data["Player_ID"], data["Player_Name"], data["Jersey_Number"], data["Position_Name"], data["Position_Type"])
        curs.commit()

    if isinstance(data, list):
        for row in data:
            curs.execute(query, row["Team_ID"], row["Player_ID"], row["Player_Name"], row["Jersey_Number"], row["Position_Name"], row["Position_Type"])
            curs.commit()

    return 'success', 200

#DELETE Team (DELETE)
@app.route('/NHL_teams/<string:id>', methods=['DELETE'])
def delete_single_team(id):
    curs = g.sql_conn.cursor()
    curs.execute("DELETE FROM [nba-data].[dbo].[Teams_NHL] WHERE Team_ID = ?", id)

    return 'success', 200

#DELETE Player
@app.route('/NHL_players/<string:id>', methods=['DELETE'])
def delete_single_player(id):
    curs = g.sql_conn.cursor()
    curs.execute("DELETE FROM [nba-data].[dbo].[PLAYERS_NHL] WHERE Player_ID = ?", id)

    return 'success', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0")
