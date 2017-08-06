# refBot
The discord bot for the "Little League" League of Legends fan-made game mode.


Desired functionality for RefBot:

1. "!draft" - Randomly order the various roles (Top, Jungle, Mid, ADC, and Support) for manual "Little League" draft and message the list to the lobby ==WORKING AS INTENDED [as of version 6]

2. "!randomChamps <n>" - Pick <n> random champions from the total champion pool (pulled from Riot's API) and message the list to the lobby ==WORKING AS INTENDED [as of version 6]

3. "!aye <summoner name>" - Adds the summoner name given to the roster of currently playing "Little League" players and notifies the lobby when 10 players are reached ==WORKING AS INTENDED [as of version 6]

4. "!bye <summoner name>" - Removes the summoner given from the roster of currently playing "Little League" players. "!bye all" removes all players from the roster ==WORKING AS INTENDED [as of version 6]

5. "!rollCall" - Messages the lobby with the current roster of playing "Little League" players, listed in ascending numeric order

6. "!rank <summoner name>" - Messages the lobby with the Solo/Duo Queue ranked stats for the summoner given

7. "!place <summoner name>" - Assigns the player a numeric value based on the rank of the summoner provided

8. "!roster" - Messages the lobby with the list of players currently assigned values via the !place command

9. "!aDraft" - Uses player values to sort the players that have been placed (using the !place command) into two teams of near equal value
