import requests as re
import pyodbc


#Questions 1-3
#1) Which database will you be using for you final project? (e.g. SQL Server, MongoDB, Other...)
#2) Where will the database you are using be hosted? (e.g. Azure, Locally, Shared MIS Dept.)
#3) Why did you choose the database and hosting option you did?
#
#1) We are using SQL Server Express Edition.
#2) It is being hosted through Amazon Web Services' RDS System.
#3) It's fairly user-friendly and Stokton is already familiar with the system.
# =============================================================================
# For Schema Description See Table Creation Queries below
# =============================================================================


# url is what gives us the JSON file. header is what makes it so we're not flagged as a bot
#Establish connection to Database and MS SQL
header = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
server = 'nba-data.cewblrob7gqp.us-west-1.rds.amazonaws.com,1433'
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=nba-data.cewblrob7gqp.us-west-1.rds.amazonaws.com,1433;Database=nba-data;Uid=admin;Pwd=Edgehill3;'
conn = pyodbc.connect(connection_string,autocommit=True)
curs = conn.cursor()

# =============================================================================
# Inserting data into 'Teams_NHL'
# We are operating under the following assumptions
# 1. Table 'Teams_NHL' has been created.
# 2. Table 'Teams_NHL' is empty.
# (Please note that queries for emptying the 'Teams_NHL' table and creating 
# the table are in the Queries section below)
# =============================================================================

#Pull Data about NHL teams - Don't comment these out!
NHL_teams_url = 'https://statsapi.web.nhl.com/api/v1/teams'
NHL_teams = re.get(NHL_teams_url, headers=header).json()['teams']
#
##Loop through the teams in the NHL extracting key data elements.
#for i in range(len(NHL_teams)):
#    team_id = NHL_teams[i]['id']
#    team_name = NHL_teams[i]['name']
#    stadium = NHL_teams[i]['venue']['name']
#    city = NHL_teams[i]['venue']['city']
#    short_name = NHL_teams[i]['abbreviation']
#    first_year = NHL_teams[i]['firstYearOfPlay']
#    division = NHL_teams[i]['division']['name']
#    conference = NHL_teams[i]['conference']['name']
#    website = NHL_teams[i]['officialSiteUrl']
#    
#    values_string = str(team_id) + ',\'' + team_name + '\',\'' + stadium + '\',\'' + city + '\',\'' + short_name + '\',\'' + first_year + '\',\'' + division + '\',\'' + conference + '\',\'' + website + '\''
#
#    insert_data_query = '''INSERT INTO [nba-data].[dbo].[Teams_NHL] (Team_ID, Team_Name, Venue, City, Short_Name, Start_Year, Division, Conference, Website_URL)
#        VALUES (''' + values_string + ''')''' 
#        
#    #Execute the insertion of that team's data into Teams_NHL table
#    curs.execute(insert_data_query)
#    
#
#conn.commit()
#conn.close()

# =============================================================================
# Inserting data into 'PLAYERS_NHL'
# We are operating under the following assumptions
# 1. Table 'PLAYER_NHL' has been created.
# 2. Table 'PLAYER_NHL' is empty.
# (Please note that queries for emptying the 'PLAYERS_NHL' table and creating 
# the table are in the Queries section below)
# =============================================================================

###An empty list to store the team id for each team
#team_id_list = []
###Populating the team_id_list
#for i in range(len(NHL_teams)):
#    team_id_list.append(NHL_teams[i]['id'])
#
##Pull Player data from each team one at a time
#for id_number in team_id_list:
#    NHL_roster_url = 'https://statsapi.web.nhl.com/api/v1/teams/'+str(id_number)+'/roster'
#    NHL_roster = re.get(NHL_roster_url, headers=header).json()['roster']
#    
#    #Create temporary storage variables looping through the players on each roster
#    try:
#        for i in range(len(NHL_roster)):
#            team_id = id_number
#            player_id = NHL_roster[i]['person']['id']
#            player_name = NHL_roster[i]['person']['fullName']
#            #Some players have 's in their name
#            player_name = player_name.replace("'", "")
#            number = NHL_roster[i]['jerseyNumber']
#            position = NHL_roster[i]['position']['name']
#            position_type = NHL_roster[i]['position']['type']
#            
#            values_string = str(team_id) + ',' + str(player_id) + ',\'' + player_name + '\',\'' + number + '\',\'' + position + '\',\'' + position_type + '\''
#            
#            insert_data_query = '''INSERT INTO [nba-data].[dbo].[PLAYERS_NHL] (Team_ID, Player_ID, Player_Name, Jersey_Number, Position_Name, Position_Type)
#            VALUES (''' + values_string + ''')'''
#            
#            curs.execute(insert_data_query)
#    except Exception:
#        print("Name: ", player_name, "Team: ", team_id)
#        print("An error occurred")
##        
#conn.commit()
#conn.close()int


##########################
#Table Creation Queries
##########################

#The Table Creation Queries below have the following schema:
#The Teams_NHL table has a team_id field provided by the API data, which is designated as Primary Key and donated to the PLAYERS_NHL table
#The PLAYERS_NHL table accepts the team_id field as a foreign key. The code below is functional.

## Build the table Teams_NHL
# curs.execute('''
#       CREATE TABLE [nba-data].[dbo].[Teams_NHL] (
#        Team_ID int primary key,
#        Team_Name VarChar(100),
#        Venue VarChar(100),
#        City VarChar(50),
#        Short_Name VarChar(50),
#        Start_Year VarChar(10),
#        Division VarChar(30),
#        Conference VarChar(50),
#        Website_URL VarChar(150))
##     ''')

## Build the table PLAYERS_NHL
#curs.execute('''CREATE TABLE [nba-data].[dbo].[PLAYERS_NHL](
#                	PLAYER_NHL_ID int primary key clustered identity(1,1),
#                   Team_ID int FOREIGN KEY REFERENCES [nba-data].[dbo].[Teams_NHL](Team_ID),
#                	Player_ID int,
#                	Player_Name VarChar(50),
#                	Jersey_Number VarChar(5),
#                	Position_Name VarChar(50),
#                	Position_Type VarChar(50))''')

