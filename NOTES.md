Notes
====

*Some of key points to note while using the tool*

- The column names of the dataframe should only be "x,y,team_id,player_id,time". The format of the columns are as below .
	x, y - int/float - Player location coordinates x and y
    team_id - int/string - Team Id for both attacking and defending teams
    player_id - int/string - Player Id for both attacking and defending team. Id for ball is optional
    time - int/float - Game time in seconds or any units.

- The tool doesn't do any processing of the inputted data. Any processing that is being done is only for the purpose of making the plot. 

- The animation time should increase uniformly across the dataset. For example, if time difference between frames are 1 unit, then it should be 1 unit across the dataset. Uneven time difference between frames would result in error when slider is dragged.

- For sports like soccer, where time starts from 0 to max, sport = `football` should be used. For sports like basketball where time decreases from 12 - min, sport = `basketball` should be used. Bokeh slider, at present, works from min-max range. So when `basketball` is used, the slider time is converted to negative and starts from min to max (-12 to 0) which is similar to normal slider function.

- All plot related aspects like plot width, height, color only be changed by editing the source code `game_animation.py`.

- `show_dist_speed` turns the plot on/off for speed and distance of the players. Since there are already too many plots by default, adding this plot might make animation rendering slow. 

