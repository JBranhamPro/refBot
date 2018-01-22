# RefBot
A Discord bot which handles custom 5v5s in League of Legends.

date of last update = Jan 22, 2018


Functionality currently working as intended as of date of last update:
========================================================================================================================================

1. "<b>!a</b> <i>summoner name</i>" - If manual draft is enabled, adds the named summoner to Team A of the game they are currently in

2. "<b>!aye</b> <i>summoner name</i>" - Adds the named summoner to an open game.

3. "<b>!b</b> <i>summoner name</i>" - If manual draft is enabled, adds the named summoner to Team B of the game they are currently in

4. "<b>!bye</b> <i>summoner name</i>" - Removes the named summoner from the game they are currently in

5. "<b>!close</b> <i>game index</i>" - Removes the game at the given index from the list of active games

6. "<b>!get</b> <i>summoner name</i>" - Retrieves the named summoner's data from the Little League database

7. "<b>!open</b>" - Adds a new game to the list of active games

8. "<b>!roles</b> <i>primary</i> <i>secondary</i> <i>summoner name</i>" - Sets the desired primary and secondary role to be displayed for the named summoner

9. "<b>!rollCall</b>" - Displays the list of currently active games and the players enrolled in them

10. "<b>!save</b> <i>game index</i>" - Uploads the current data of the game at the given index to the Little League database