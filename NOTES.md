Notes
====

*Some key points to note while using the tool*

- The column names of the dataframe should only be `x,y,team_id,player_id,time`. The format of the columns are as below .<br>
	`x, y` - int/float - Player location coordinates x and y<br>
    `team_id` - int/string - Team id for both attacking and defending teams<br>
    `player_id` - int/string - Player id for both attacking and defending team. id for ball is optional<br>
    `time` - int/float - Game time in seconds or any units.<br>

- The tool doesn't do any processing of the inputted data. Any processing that is being done is only for the purpose of making the plot. So the tool assumes the inputted data is correct. Any missing values in the data would lead to error in the plot.

- The game time should increase uniformly across the dataset. For example, if time difference between frames are 1 unit, then it should be 1 unit across the entire dataset. Unequal time difference between frames would result in error when slider is dragged.

- For sports like soccer, where time starts from 0 to max, sport = `football` should be used. For sports like basketball where time decreases from max - min, sport = `basketball` should be used. Bokeh slider, at present, works from min-max range. So when `basketball` is used, the slider time is converted to negative and starts from min to max (-12 to 0) which is same as normal slider function.

- All plot related aspects like plot width, height, color of plots can only be changed by editing the source code `game_animation.py`. Default colors are too good btw ;) 

- `show_dist_speed` turns the plot on/off for speed and distance of the players. Since there are already too many plots by default, adding this plot might make animation rendering slow. 

