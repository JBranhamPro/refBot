# refBot
# date of last update = Aug 10, 2017
The discord bot for the "Little League" League of Legends fan-made game mode.


Functionality currently working as intended as of date of last update:
========================================================================================================================================

1. "!draft" - Randomly order the various roles (Top, Jungle, Mid, ADC, and Support) and message the lists to the lobby

2. "!randomChamps <n>" - Pick <n> random champions from the total champion pool (pulled from Riot's API) and messages the list to the lobby 

3. "!aye <summoner name>" - Adds the summoner name given to the list of players interested in playing "Little League" (list: playerNames) and notifies the lobby when 10 players are reached

4. "!bye <summoner name>" - Removes the summoner name given from the list of players interested in playing "Little League". "!bye all" removes all players from the list

5. "!rollCall" - Messages the lobby with the current list of players interested in playing "Little League"

6. "!rank <summoner name>" - Messages the lobby with the Solo/Duo Queue ranked stats for the summoner given

7. "!place <summoner name>" - Assigns the summoner a numeric value based on their rank. "!place all", places all names in the list of interested players (list: playerNames, added from !aye)

8. "!roster" - Messages the lobby with the list of players currently assigned values via the !place command

9. "!aDraft" - Uses player values to sort the players that have been placed (using the !place command) into two teams of near equal value

10. "!replace <summoner name>" - Removes the summoner from the roster of current Little League players (dict: littleLeaguers). "!replace all", it will clear all players from the roster instead.



Functionality NOT working as intended as of date of last update:
========================================================================================================================================

1. "!aPlace" - Pulls the usernames of all users in a designated voice channel on the server, then places the aggregated names (using the same function as the !place command)



Functionality desired but not yet implemented as intended as of date of last update:
========================================================================================================================================

1. "!set <summoner name>" - Sets the username of the user who issued the command to the summoner name provided
