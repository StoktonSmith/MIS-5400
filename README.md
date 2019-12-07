# MIS-5400

## Data Acquisition and Loading
The database_connection.py is a file that creates a team and player table in our database, pulls data from the NHL data API (https://statsapi.web.nhl.com/api/v1/**teams** and https://statsapi.web.nhl.com/api/v1/teams/<teamID>/**roster**), and inserts it into appropriate columns in our AWS hosted database. We use an SQL Server as our DBMS.

## Flask Web App 
The flask_web_app.py hosts a flask web app which returns different types of NHL Data. You can do GET and POST requests and it will pull and write to the Database. The landing page to our web app contains information about what URL will return the information you seek. You can return all the data, a specific team, all teams, a specific player or all players. The data is all returned in JSON format.

## HTML Landing Page
The home.html file contains html and css code that modify the look of the home page and add helpful links. The home.html file must be in a folder named "templates".

## Power BI Insights
The Analytics_Programming_Final_Project.pbix file contains Power BI tiles that provide insights about the data. There are graphs showing the longest standing NHL teams, the geographical location of those teams, and most common player names in the NHL. The data is categorical and therefore difficult to quantitatively analyze, so Power BI was our most optimal tool for adding value to our data.

## Conclusion
The web app and database work well. The only thing that we would do differently would be to not link our Power BI work directly to our database. If we could have the API act as a stand-between for the database and our Power BI insights it would make the project much more secure. 

