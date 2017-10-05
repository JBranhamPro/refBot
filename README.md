# RefBot
The discord bot for the "Little League" League of Legends fan-made game mode.

date of last update = Sep 20, 2017


Functionality currently working as intended as of date of last update:
========================================================================================================================================

1. "<b>!aye</b> <i>summoner name</i>" - Verifies that the summoner name is correct then adds that summoner to the list of participating players.

2. "<b>!bye</b> <i>summoner name</i>" - Removes the summoner from the list of participating players

3. "<b>!on</b> <i>feature</i>" - Sets the specified feature to active for the !draft command. Features currently implemented: rChamps <n>, rLanes, matchmade.

4. "<b>!on rChamps</b> <i>n</i>" - Makes two pools of <i>n</i> number of unique champions, one pool for each team. By default, it pulls 15 champions if no other number is specificied.

5. "<b>!on rLanes</b>" - Randomly assigns players on each team to a different role (TOP, JNG, MID, ADC, SUP)

6. "<b>!on matchmade</b>" - Assigns players a value based on their current ranked standing (Solo/Duo first, Flex if no Solo/Duo found) and then separates the players into teams based on the lowest possible difference in value between the two teams

7. "<b>!off</b> <i>feature</i>" - Sets the specified feature to inactive for the !draft command (works identically to the "!on" command). Features currently implemented: rChamps <n>, rLanes, matchmade.

8. "<b>!draft</b>" - Divides the player group into two teams and then performs additional acts based on features that are currently active via the !on command. By default, it will divide players into two teams randomly if matchmade is turned off.
