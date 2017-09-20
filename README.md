# RefBot
date of last update = Sep 20, 2017

The discord bot for the "Little League" League of Legends fan-made game mode.


Functionality currently working as intended as of date of last update:
========================================================================================================================================

1. "aye <summoner name>" - Verifies that the summoner name is correct then adds that summoner to the list of participating players. Will not add the same player twice.

2. "bye <summoner name>" - Removes the summoner from the list of participating players

3. "!on <feature>" - Sets the specified feature to active for the !draft command. Features currently implemented: rChamps <n>, rLanes, matchmade.
a... "rChamps <n>" - Makes a two pools of n number of unique champions, one pool for each team
b... "rLanes" - Randomly assigns players on each team to a different role (TOP, JNG, MID, ADC, SUP)
c... "matchmade" - Assigns players a value based on their current ranked standing (Solo/Duo first, Flex if no Solo/Duo found) and then separates the players into teams based on the lowest possible difference in value between the two teams

4. "!off <feature>" - Sets the specified feature to inactive for the !draft command. Features currently implemented: rChamps <n>, rLanes, matchmade.

5. "!draft" - Divides the player group into two teams and then performs additional acts based on features that are currently active via the !on command.
