
Game Animation
====
An easy way to visualize player tracking data with animation. Built using [Bokeh Plots](https://github.com/bokeh/bokeh), this tool can be used to visualise player movement for all sport. It also includes voronoi and convex hull plots, player speed and total distance covered by each player, all of  which can be interactively plotted on/off.

<img src="sample_images/soccer_animation.gif" alt="Soccer Animation" width="700"/>

The code was tested on **`Python 3.7.1`**, but should work for other versions as well. 

The following packages are needed in order to run the code (*Packages with older versions should work as well*) :

| Package |Version|
|--|--|
| Numpy |1.16.4|
|Pandas|0.24.2|
| Bokeh|1.2.0|
| Scipy|1.3.0|
| Notebook|5.7.8|


The animation plot can be viewed directly on a `Jupyter Notebook`. 

### Usage
--- 
- 2 sample notebook examples ([Soccer_example.ipynb](Soccer_example.ipynb) and [Basketball_example.ipynb](Basketball_example.ipynb)) are placed in the folder. 
- The background pitch images are placed in `/static/images/` folder.  


***Please see [Notes](NOTES.md) for additional information regarding potential errors and usability of the tool.***
 
### Key parameters to `make_plot`

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

### Sample basketball animation
---

```
#import make_plot from game_animation

from Animation.game_animation import make_plot
from bokeh.io import show, output_notebook
import pandas as pd
from functools import partial

#output_notebook shows the graph within the notebook
output_notebook()

df = pd.read_csv("sample_data/sample_basketball.csv")
image_url=["static/images/basketball.png"]

id_def=65
id_att=37
x_range=(0,94)
y_range=(0,50)

make_anim_plot = partial(make_plot, df=df, id_def = id_def, id_att = id_att,
                           headers = ["x", "y", "team_id", "player_id","time"], 
                           image_url=image_url, slider_steps=1,sport='basketball', 
                           x_range=x_range,y_range=y_range, anim_speed=50)

show(make_anim_plot)
```

### Sample soccer animation:
---
```
from Animation.game_animation import make_plot
from bokeh.io import show, output_notebook
import pandas as pd
from functools import partial

output_notebook()

df = pd.read_csv('sample_data/soccer_sample.csv')
image_url = 'static/images/soccer.png'

x_range=(-52.5,52.5)
y_range=(-34, 34)

id_def = 2
id_att = 1

make_anim_plot = partial(make_plot, df=df,image_url=image_url, id_def=id_def, id_att = id_att,
                           x_range=x_range, y_range=y_range, slider_steps=1,
                           headers = ["x", "y", "team_id", "player_id","time"], 
                           anim_speed=60)

show(make_anim_plot)
```

### Sample Outputs:
---

<img src="sample_images/basketball.png" alt="Basketball_example" width="700"/>

<img src="sample_images/soccer.png" alt="Soccer_example" width="700"/>

<img src="sample_images/speed_distance.png" alt="Soccer_example" width="700"/>

---

All feedbacks are appreciated.

Built by Samira Kumar

Reach out to me on [Twitter](https://twitter.com/Samirak93) and you can find my LinkedIn page [here](http://linkedin.com/in/samirakumar/)
