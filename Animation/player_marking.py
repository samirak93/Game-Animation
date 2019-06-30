# -*- coding: utf-8 -*-

# ignore warnings
import warnings
import sys

# importing pandas and numpy
import numpy as np
import pandas as pd

# importing bokeh and its related functions
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox,column
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models.widgets import Slider, Button
from bokeh.plotting import figure

# importing cdist from scipy
from scipy.spatial.distance import cdist

warnings.filterwarnings("ignore")

if sys.version_info[0] < 3:
    raise Exception("This app requires Python 3")


def player_marking(doc, df, headers, id_def, id_att, slider_steps, x_range, y_range,
                   image_url, sport='football', anim_speed=50, attack = True):

    """
                Parameters
        ---------------------------
        :param doc: Plots the graph
        :param df: Gets the user defined dataframe
        :param headers: Give the headers to the dataframe - Headers should be ["x", "y", "team_id", "player_id","time"]

        {x, y - int/float - Player location coordinates x and y
        team_id - int/string - Team Id for both attacking and defending teams
        player_id - int/string - Player Id for both attacking and defending team. Id for ball is optional
        time - int/float - Game time in seconds or any units.}

        :param id_def: Provide id of defending team
        :param id_att: Provide id of attacking team
        :param x_range: Provide x range of the pitch coordinates
        :param y_range: Provide y range of the pitch coordinates
        :param image_url: Provide the location of the background image of the pitch
        :param slider_steps: Provide the slider steps
        :param sport: (football/basketball) - Provide the sport details to change slider function - Default is football(⚽️)
                        Football allows slider timer to move from low to max (0-90 minutes),
                        while sports that have decreasing timer (12 to 0 minutes) should use "basketball".
        :param attack:(True/False) - If 'True', then the attacking team is considered players marking and defending
        team is considered as players being marked. If 'false' then logic is reversed.

        :return: Returns the animation plot

    """
    """
                Value Errors
        ---------------------------

        """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The expected data type of input data is a dataframe but a {} was provided.".format(type(df)))

    accept_dtypes_id = [int, float, str, tuple]

    if type(id_def) not in accept_dtypes_id:
        raise ValueError("The expected data type for defending team-id is either integer, float "
                         "or a string but {} was provided.".format(type(id_def)))

    if type(id_att) not in accept_dtypes_id:
        raise ValueError("The expected data type for defending team-id is either integer, float "
                         "or a string but {} was provided.".format(type(id_att)))

    if not isinstance(x_range, (list, tuple)):
        raise ValueError("The expected data type for x-range is a list but a {} was provided.".format(type(x_range)))

    if not isinstance(y_range, (list, tuple)):
        raise ValueError("The expected data type for y-range is a list but a {} was provided.".format(type(y_range)))

    if len(x_range) != 2:
        raise ValueError("Length of x range of coordinates is {} but expected length is 2.".format(len(x_range)))

    if len(y_range) != 2:
        raise ValueError("Length of y range of coordinates is {} but expected length is 2.".format(len(x_range)))

    if sport not in ['football', 'basketball']:
        raise ValueError(
            "Only football/basketball in accepted as input for sport type, but {} was provided.".format(sport))

    if not isinstance(image_url, list):
        image_url = [image_url]

    all_team = pd.DataFrame(df, columns=headers)

    all_team['x'] = pd.to_numeric(all_team['x'])
    all_team['y'] = pd.to_numeric(all_team['y'])
    all_team['time'] = pd.to_numeric(all_team['time'])
    all_team['player_id'] = all_team['player_id'].apply(str)

    all_team['team_id'] = np.where(((all_team['team_id'] != id_att) & (all_team['team_id'] != id_def)), -99,
                                   all_team['team_id'])
    all_team['player_id'] = np.where(((all_team['team_id'] != id_att) & (all_team['team_id'] != id_def)), " ",
                                     all_team['player_id'])

    if sport == 'basketball':
        all_team['time'] = - all_team['time']
        all_team = all_team.sort_values(['time', 'team_id', 'player_id'], ascending=[False, False, True]).reset_index(
            drop=True)
    else:
        all_team['time'] = all_team['time']
        all_team = all_team.sort_values(['time', 'team_id', 'player_id'], ascending=[True, False, True]).reset_index(
            drop=True)

    team_def = all_team[all_team.team_id == id_def]
    team_att = all_team[all_team.team_id == id_att]

    if team_def.empty:
        raise ValueError("Defending team ID is not valid. Please enter a valid team ID")

    elif team_att.empty:
        raise ValueError("Attacking team ID is not valid. Please enter a valid team ID")

    current_time = all_team['time'].min()

    coord_x = all_team[all_team.time == current_time]['x']
    coord_y = all_team[all_team.time == current_time]['y']

    team_def_xy = team_def[team_def.time == current_time]
    team_att_xy = team_att[team_att.time == current_time]

    player_id = all_team[all_team['time'] == current_time]['player_id']

    c = (['dodgerblue'] * len(team_def['player_id'].unique()) + ['orangered'] * len(team_att['player_id'].unique()) + [
        'gold'])
    """
    For each frame, calculate the nearest player for each given player using cdist
    
    """
    def get_distances(team_def_xy, team_att_xy, attack):

        if attack:
            columns = team_def_xy['player_id'].values.tolist()
            index = team_att_xy['player_id'].values.tolist()
            dist_mat = cdist(team_att_xy[['x', 'y']].values, team_def_xy[['x', 'y']].values)
            source_x,source_y = team_att_xy['x'].values, team_att_xy['y'].values
            merge_df = team_def_xy[['player_id', 'x', 'y']]
        else:
            columns = team_att_xy['player_id'].values.tolist()
            index = team_def_xy['player_id'].values.tolist()
            dist_mat = cdist(team_def_xy[['x', 'y']].values, team_att_xy[['x', 'y']].values)
            source_x, source_y = team_def_xy['x'].values, team_def_xy['y'].values
            merge_df = team_att_xy[['player_id', 'x', 'y']]

        dist_df = pd.DataFrame(dist_mat)
        dist_df.columns = columns
        dist_df.index = index
        nearest_player = dist_df.idxmin(axis=1)
        dist_df['closest_player'] = nearest_player
        dist_df['source_player'] = index
        dist_df['source_x'] = source_x
        dist_df['source_y'] = source_y

        lines_x = pd.merge(dist_df, merge_df, left_on='closest_player',right_on='player_id', sort=False)\
            .rename(columns = {'x':'target_x','y':'target_y'})
        x_lines = list(zip(lines_x['source_x'], lines_x['target_x']))
        y_lines = list(zip(lines_x['source_y'], lines_x['target_y']))

        return x_lines, y_lines

    x_lines, y_lines = get_distances(team_def_xy,team_att_xy,attack)

    source_coord = ColumnDataSource(data=dict(x=coord_x, y=coord_y, player_id=player_id, color=c))
    source_lines = ColumnDataSource(data=dict(xs=x_lines, ys=y_lines))

    """
    Remove plot background and alter other styles

    """

    def plot_clean(plot):

        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None
        plot.axis.major_label_text_font_size = "10pt"
        plot.axis.major_label_standoff = 0
        plot.border_fill_color = "white"
        plot.title.text_font = "times"
        plot.title.text_font_size = '10pt'
        plot.background_fill_color = "white"
        plot.title.align = 'center'
        return plot

    plot = figure(name='base', plot_height=550, plot_width=850,
                  title="Player Marking Animation", tools="reset,save,wheel_zoom,pan",
                  x_range=x_range, y_range=y_range, toolbar_location="below")

    image_min_x, image_min_y, image_max_x, image_max_y = min(x_range), min(y_range), \
                                                         (abs(x_range[0]) + abs(x_range[1])), \
                                                         (abs(y_range[0]) + abs(y_range[1]))

    plot.image_url(url=image_url, x=image_min_x, y=image_min_y, w=image_max_x, h=image_max_y, anchor="bottom_left")

    plot.multi_line('xs', 'ys', source=source_lines, color='orangered',
                    line_width=3, line_alpha=.7, line_cap='round', line_dash="dashed")
    plot.scatter('x', 'y', source=source_coord, size=20, fill_color='color')

    labels = LabelSet(x='x', y='y', text='player_id',
                      source=source_coord, y_offset=-8,
                      render_mode='canvas', text_color='black',
                      text_font_size="8pt", text_align='center')

    plot.add_layout(labels)
    plot.axis.visible = False
    plot = plot_clean(plot)

    slider_start = all_team.time.unique().min()
    slider_end = all_team.time.unique().max()
    game_time = Slider(title="Game Time (seconds)", value=slider_start,
                       start=slider_start, end=slider_end, step=slider_steps)

    """
       Update the figure every time slider is updated.
    """

    def update_data(attrname, old, new):

        slider_value = np.round(game_time.value, 2)

        coord_x = all_team[all_team.time == slider_value]['x']
        coord_y = all_team[all_team.time == slider_value]['y']

        team_def_xy = team_def[team_def.time == slider_value]
        team_att_xy = team_att[team_att.time == slider_value]

        x_lines, y_lines = get_distances(team_def_xy, team_att_xy, attack)

        source_coord.data = dict(x=coord_x, y=coord_y, player_id=player_id, color=c)
        source_lines.data = dict(xs=x_lines, ys=y_lines)


    for w in [game_time]:
        w.on_change('value', update_data)

    """
       Animation
    """

    def animate_update():

        time = game_time.value + slider_steps
        if time > all_team.time.max():
            time = all_team.time.min()
        game_time.value = time

    callback_id = None

    def animate():
        global callback_id
        if button.label == '► Play':
            button.label = '❚❚ Pause'
            callback_id = curdoc().add_periodic_callback(animate_update, anim_speed)
        else:
            button.label = '► Play'
            curdoc().remove_periodic_callback(callback_id)

    button = Button(label='► Play', width=60)
    button.on_click(animate)

    inputs = widgetbox(row(column(game_time, button)))

    layout = column(row(column(plot, inputs)))

    doc.add_root(layout)
    doc.title = "Game Animation"

    return doc

