Each of the plotting functions are explained in detail here
====
### Key parameters for `make_plot`:

---

**`:param doc:`** Plots the graph<br>
**`:param df:`** Provide the dataframe<br>
**`:param headers:`** Give the headers to the dataframe - Headers should be ["x", "y", "team_id", "player_id","time"]<br>

{ x, y - int/float - Player location coordinates x and y
team_id - int/string - Team Id for both attacking and defending teams
player_id - int/string - Player Id for both attacking and defending team. Id for ball is optional  
time - int/float - Game time in seconds or any units. }  

**NOTE** - Time difference between each frame of game animation should increase uniformly. For example, time different between current and next frame should be same as 1 across the dataset. 

**`:param id_def:`** (int/string) - Provide id of defending team<br>
**`:param id_att:`** (int/string) - Provide id of attacking team<br>
**`:param x_range:`** (list/tuple of min max of pitch dimension) - Provide x range of the pitch dimension<br>
**`:param y_range:`** (list/tuple of min max of pitch dimension) - Provide y range of the pitch dimension<br>
**`:param image_url:`** (string/list of string) - Provide the location of the background image for the pitch<br>

**`:param slider_steps:`** (int/float) - Provide the slider steps - This is the difference in time between each frame of game action.<br>

**`:param sport:`** ('football'/'basketball') - Provide the sport details to change slider function - Default is football(⚽️)<br>
'Football' allows slider timer to move from low to max (0-90 minutes), while sports that have decreasing timer (12 to 0 minutes) should use "basketball".

**`:param anim_speed:`** *Optional* (int/float) - Provide speed of animation - milliseconds<br>
**`:param show_dist_speed:`** (True/False) - Turns on/off plotting speed and distance. - Default value is False.<br>
**Note** - Turning on speed and distance plots could make animation rending slow.

<br>
<br>

### Key parameters for `player_marking`:

---

**`:param doc:`** Plots the graph<br>
**`:param df:`** Provide the dataframe<br>
**`:param headers:`** Give the headers to the dataframe - Headers should be ["x", "y", "team_id", "player_id","time"]<br>

{ x, y - int/float - Player location coordinates x and y
team_id - int/string - Team Id for both attacking and defending teams
player_id - int/string - Player Id for both attacking and defending team. Id for ball is optional  
time - int/float - Game time in seconds or any units. }  

**NOTE** - Time difference between each frame of game animation should increase uniformly. For example, time different between current and next frame should be same as 1 across the dataset. 

**`:param id_def:`** (int/string) - Provide id of defending team<br>
**`:param id_att:`** (int/string) - Provide id of attacking team<br>
**`:param x_range:`** (list/tuple of min max of pitch dimension) - Provide x range of the pitch dimension<br>
**`:param y_range:`** (list/tuple of min max of pitch dimension) - Provide y range of the pitch dimension<br>
**`:param image_url:`** (string/list of string) - Provide the location of the background image for the pitch<br>

**`:param slider_steps:`** (int/float) - Provide the slider steps - This is the difference in time between each frame of game action.<br>

**`:param sport:`** ('football'/'basketball') - Provide the sport details to change slider function - Default is football(⚽️)<br>
'Football' allows slider timer to move from low to max (0-90 minutes), while sports that have decreasing timer (12 to 0 minutes) should use "basketball".

**`:param anim_speed:`** *Optional* (int/float) - Provide speed of animation - milliseconds<br>
**`:param attack:`** (True/False) - If 'True', then the attacking team is considered players marking and defending team is considered as players being marked. If 'false' then logic is reversed.<br>
<br>
<br>

### Key parameters for `marking_stats`:

---

**`:param df:`** Provide the dataframe<br>
**`:param headers:`** Give the headers to the dataframe - Headers should be ["x", "y", "team_id", "player_id","time"]<br>

{ x, y - int/float - Player location coordinates x and y
team_id - int/string - Team Id for both attacking and defending teams
player_id - int/string - Player Id for both attacking and defending team. Id for ball is optional  
time - int/float - Game time in seconds or any units. }  

**NOTE** - Time difference between each frame of game animation should increase uniformly. For example, time different between current and next frame should be same as 1 across the dataset. 

**`:param id_def:`** (int/string) - Provide id of defending team<br>
**`:param id_att:`** (int/string) - Provide id of attacking team<br>
**`:param time_steps:`** (int/float) - Provide the time steps - Difference in time between each frame of game action.<br>
**`:param attack:`** (True/False) - If 'True', then the attacking team is considered players marking and defending team is considered as players being marked. If 'false' then logic is reversed.<br>
**`:param threshold:`** (int) - Get the threshold to consider players as marked - players who were tagged as marked below threshold would not be considered.<br>
<br>
<br>
