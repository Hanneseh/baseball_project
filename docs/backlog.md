# Backlog of NL Baseball

We provide here a small list of things to do which would take the dashboard to the next level.

Read the following list if you are looking for inspiration on how to contribute to the dashboard:

## Quality Management:

-	The dashboard was programmed by armature programmers who had barely any knowledge about programming best practices. Maybe you can make the code more efficient and secure?
-	During development, not a lot of resources were allocated towards checking if the data for the players is correct or includes everything that it should. Maybe you want to go through the tasks of making sure that everything gets scraped correctly and is displayed in a way that is helpful to the user
-	The code base grew more and more without making sure that it is efficient and clean. Maybe you like to refactor code to make it easier maintainable. 

## Squad functionality:
This a feature that was planned for the first release but didn’t make it in because the time wasn’t enough. Here is what that functionality should have included:

-	An extra page dedicated to squads. 
-	The user can create and delete squads.
-	The user can add player to a squad
-	A score is created for the squad on how well that squad would perform in a game. That score would be based on the stats of the players in the squad.
-	Squads should be comparable.
-	Squads need to be persistent, meaning they should be saved to mongo DB so that they don’t get lost when the page is refreshed.

## Display performance of a player over time

The idea is that the performance of a player should be visualized in a set of visual elements (different graphs and filters). Ideas:

-	Line/Bar graphs for certain metrics describing the player

## Make browsing players better
 
The career average table was meant to make it easy to browse through the main stats of each player and compare them to other players. Maybe there is a better way of doing this- For example: 

-	Using just the most recent stats of the players to display in that table.
-	Ranking the players based on their scores (check with the user what is important to them)

## Include current game stats and scheduled games for the players

The API provide a lot of data. Most of the endpoints enable the user to query game stats and game schedules. Maybe it is helpful to get that data and create a custom game schedule for only the Dutch players. In that way, the user who monitors these players never misses a game of those player again.
