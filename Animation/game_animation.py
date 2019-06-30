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
from bokeh.models import ColumnDataSource, LabelSet, CustomJS, Title
from bokeh.models.widgets import Slider, Paragraph, Button, CheckboxButtonGroup
from bokeh.plotting import figure

# importing convexhull and voronoi from scipy
from scipy.spatial import ConvexHull, Voronoi

sys.path.append('/Game_Animation/Animation/')

from Animation.patches_from_voronoi import patches_from_voronoi

warnings.filterwarnings("ignore")

sys.path.append("/Game_Animation/")

if sys.version_info[0] < 3:
    raise Exception("This app requires Python 3")


def make_plot(doc, df, headers, id_def, id_att, slider_steps, x_range, y_range,
              image_url,
              sport='football', anim_speed=50, show_dist_speed=False):

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
    :param anim_speed: Provide speed of animation - milliseconds
    :param show_dist_speed: Turn on/off plotting speed and distance. Default value is False.
                        Note- Turning on speed and distance plot could make animation rending slow.

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
        raise ValueError("Only football/basketball in accepted as input for sport type, but {} was provided.".format(sport))

    if not isinstance(image_url, list):
        image_url = [image_url]

    all_team = pd.DataFrame(df, columns=headers)

    all_team['x'] = pd.to_numeric(all_team['x'])
    all_team['y'] = pd.to_numeric(all_team['y'])
    all_team['time'] = pd.to_numeric(all_team['time'])
    all_team['player_id'] = all_team['player_id'].apply(str)

    all_team['team_id'] = np.where(((all_team['team_id'] != id_att) & (all_team['team_id'] != id_def)), -99, all_team['team_id'])
    all_team['player_id'] = np.where(((all_team['team_id'] != id_att) & (all_team['team_id'] != id_def)), " ", all_team['player_id'])

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

    vor_points = list(zip(coord_x, coord_y))
    vor = Voronoi(vor_points)
    x_patch, y_patch, x_vor_ls, y_vor_ls = patches_from_voronoi(vor)

    """
       Create the convex hull for the coordinates

    """
    def get_convex_hull(team_def, team_att, current_time):

        team_att_t = np.vstack((team_att[team_att.time == current_time].x, team_att[team_att.time == current_time].y)).T
        team_def_t = np.vstack((team_def[team_def.time == current_time].x, team_def[team_def.time == current_time].y)).T

        hull = ConvexHull(team_att_t)
        hull2 = ConvexHull(team_def_t)

        team_att_ch_x = team_att_t[hull.vertices, 0]
        team_att_ch_y = team_att_t[hull.vertices, 1]

        team_def_ch_x = team_def_t[hull2.vertices, 0]
        team_def_ch_y = team_def_t[hull2.vertices, 1]

        return team_att_ch_x, team_att_ch_y, team_def_ch_x, team_def_ch_y

    source_vor = ColumnDataSource(dict(xs=x_patch, ys=y_patch))
    source_vor_ls = ColumnDataSource(dict(xs=x_vor_ls, ys=y_vor_ls))

    team_att_ch_x, team_att_ch_y, team_def_ch_x, team_def_ch_y = get_convex_hull(team_def, team_att, current_time)

    player_id = all_team[all_team['time'] == current_time]['player_id']

    c = (['dodgerblue']*len(team_def['player_id'].unique()) + ['orangered']*len(team_att['player_id'].unique()) + ['gold'])

    source_coord = ColumnDataSource(data=dict(x=coord_x, y=coord_y, player_id=player_id, color=c))
    source_ch_att = ColumnDataSource(data=dict(xc=team_att_ch_x, yc=team_att_ch_y))
    source_ch_def = ColumnDataSource(data=dict(ax=team_def_ch_x, ay=team_def_ch_y))

    """
    Below code for travel distance and speed taken from 
    http://savvastjortjoglou.com/nba-play-by-play-movements.html and modified accordingly
    
    """

    def travel_dist(player_locations):

        diff = np.diff(player_locations, axis=0)

        dist = np.sqrt((diff ** 2).sum(axis=1))

        return np.round(dist.sum())

    def get_distance(team_def, team_att, i):

        if sport == 'football':
            team_def_k = team_def[(team_def.time >= 0) & (team_def.time <= i)]
        elif sport =='basketball':
            team_def_k = team_def[(team_def.time >= team_def.time.min()) & (team_def.time <= i)]

        def_dist = team_def_k.groupby('player_id')[['x','y']].apply(travel_dist).values
        avg_speed_def = np.abs(np.round((def_dist / (i - team_def.time.min())), 2))

        if sport == 'football':
            team_att_k = team_att[(team_att.time >= 0) & (team_att.time <= i)]
        elif sport == 'basketball':
            team_att_k = team_att[(team_att.time >= team_def.time.min()) & (team_att.time <= i)]

        def_dist_att = team_att_k.groupby('player_id')[['x','y']].apply(travel_dist).values
        avg_speed_att = np.abs(np.round((def_dist_att / (i - team_att.time.min())), 2))

        return def_dist, avg_speed_def, def_dist_att, avg_speed_att

    def_dist, avg_speed_def, def_dist_att, avg_speed_att = get_distance(team_def, team_att, current_time)

    source_def_params = ColumnDataSource(data=dict(x=team_def.player_id.unique(), y=def_dist, speed=avg_speed_def))
    source_att_params = ColumnDataSource(data=dict(x=team_att.player_id.unique(), y=def_dist_att, speed=avg_speed_att))


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

    plot = figure(name='base',plot_height=550, plot_width=850,
                  title="Game Animation", tools="reset,save,wheel_zoom,pan",
                  x_range=x_range, y_range=y_range, toolbar_location="below")

    image_min_x, image_min_y, image_max_x, image_max_y = min(x_range), min(y_range), \
                                                         (abs(x_range[0]) + abs(x_range[1])), \
                                                         (abs(y_range[0]) + abs(y_range[1]))

    plot.image_url(url=image_url, x=image_min_x, y=image_min_y, w=image_max_x, h=image_max_y, anchor="bottom_left")

    plot.scatter('x', 'y', source=source_coord, size=20, fill_color='color')

    labels = LabelSet(x='x', y='y', text='player_id',
                      source=source_coord, y_offset=-8,
                      render_mode='canvas', text_color='black',
                      text_font_size="8pt", text_align='center')

    plot.add_layout(labels)
    plot.axis.visible = False
    plot = plot_clean(plot)

    """
    Plot the distance figure
    """
    plot_distance_def = figure(name='distance',plot_height=250, plot_width=250,
                               tools="reset,save", x_axis_type='linear',
                               y_range=source_def_params.data['x'].astype(str),
                               toolbar_location="below")

    plot_distance_def.hbar(y='x', right='y', source=source_def_params, left=0, height=0.5,color='dodgerblue')

    plot_distance_def.xaxis.visible = True
    plot_distance_def.yaxis.visible = True
    plot_distance_def.toolbar.logo = None
    plot_distance_def.toolbar_location = None
    plot_distance_def.add_layout(Title(text="Blue team",text_font_size="10pt",text_font='times'), 'above')
    plot_distance_def.add_layout(Title(text="Total distance covered", text_font_size="10pt",text_font='times'), 'above')

    plot_distance_def = plot_clean(plot_distance_def)

    labels_dist_red = LabelSet(x='y', y='x', text='y', level='glyph',
                               x_offset=-20, y_offset=-9, source=source_def_params,
                               render_mode='css', text_color='white',
                               text_font_size="8pt", text_font_style='bold')

    plot_distance_def.add_layout(labels_dist_red)

    avg_speed_def = figure(name='distance', plot_height=250, plot_width=250,
                           title="Avg Speed of Blue Team", tools="reset,save",
                           y_range=source_def_params.data['x'].astype(str),
                           toolbar_location="below")

    avg_speed_def.hbar(y='x', right='speed', source=source_def_params,
                       height=0.5, color='dodgerblue')

    avg_speed_def.xaxis.visible = True
    avg_speed_def.yaxis.visible = True
    avg_speed_def.toolbar.logo = None
    avg_speed_def.toolbar_location = None

    avg_speed_def = plot_clean(avg_speed_def)

    labels_speed_red = LabelSet(x='speed', y='x', text='speed', level='glyph',
                              x_offset=-20, y_offset=-9, source=source_def_params,
                              render_mode='css', text_color='white',
                              text_font_size="8pt", text_font_style='bold')

    avg_speed_def.add_layout(labels_speed_red)
    """
       Plot the distance figure
    """
    plot_distance_att = figure(name='distance',plot_height=250, plot_width=250,
                               y_range=source_att_params.data['x'].astype(str),
                               toolbar_location="below")

    plot_distance_att.hbar(y='x', right='y', source=source_att_params, height=0.5, color='orangered')

    plot_distance_att.xaxis.visible = True
    plot_distance_att.yaxis.visible = True
    plot_distance_att.toolbar.logo = None
    plot_distance_att.toolbar_location = None
    plot_distance_att.add_layout(Title(text="Red Team", text_font_size="10pt",
                                       text_font='times'), 'above')
    plot_distance_att.add_layout(Title(text="Total distance covered", text_font_size="10pt",
                                       text_font='times'), 'above')
    plot_distance_att = plot_clean(plot_distance_att)

    labels_dist_red_att = LabelSet(x='y', y='x', text='y', level='glyph',
                                   x_offset=-20, y_offset=-9, source=source_att_params,
                                   render_mode='css',text_color='white',
                                   text_font_size="8pt",text_font_style='bold')

    plot_distance_att.add_layout(labels_dist_red_att)

    avg_speed_att = figure(name='avg_speed', plot_height=250, plot_width=250,
                           title="Avg Speed of Red Team", tools="reset,save",
                           y_range=source_att_params.data['x'].astype(str),
                           toolbar_location="below")

    avg_speed_att.hbar(y='x', right='speed', source=source_att_params,
                                     height=0.5, color='orangered')

    avg_speed_att.xaxis.visible = True
    avg_speed_att.yaxis.visible = True
    avg_speed_att.toolbar.logo = None
    avg_speed_att.toolbar_location = None
    avg_speed_att = plot_clean(avg_speed_att)

    labels_speed_red_att = LabelSet(x='speed', y='x', text='speed', level='glyph',
                                  x_offset=-20, y_offset=-9, source=source_att_params,
                                  render_mode='css',text_color='white',
                                  text_font_size="8pt",text_font_style='bold')

    avg_speed_att.add_layout(labels_speed_red_att)

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

        vor_points = list(zip(coord_x, coord_y))
        vor = Voronoi(vor_points)
        x_patch, y_patch, x_vor_ls, y_vor_ls = patches_from_voronoi(vor)

        source_vor.data = dict(xs=x_patch, ys=y_patch)
        source_vor_ls.data = dict(xs=x_vor_ls, ys=y_vor_ls)

        team_att_ch_x, team_att_ch_y, team_def_ch_x, team_def_ch_y = get_convex_hull(team_def, team_att, slider_value)

        source_coord.data = dict(x=coord_x, y = coord_y, player_id=player_id, color=c)
        source_ch_att.data = dict(xc=team_att_ch_x, yc=team_att_ch_y)
        source_ch_def.data = dict(ax=team_def_ch_x, ay=team_def_ch_y)

        def_dist, avg_speed_def, def_dist_att, avg_speed_att = get_distance(team_def, team_att, slider_value)

        source_def_params.data = dict(x=team_def.player_id.unique(), y=def_dist, speed=avg_speed_def)
        source_att_params.data = dict(x=team_att.player_id.unique(), y=def_dist_att, speed=avg_speed_att)


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

    """
       Plot the patches for voronoi and convex hull
    """
    team_att_patch = plot.patch('xc', 'yc', source=source_ch_att, alpha=0, line_width=3, fill_color='orangered')
    team_def_patch = plot.patch('ax', 'ay', source=source_ch_def, alpha=0, line_width=3, fill_color='dodgerblue')

    glyph_vor = plot.patches('xs', 'ys', source=source_vor, alpha=0, line_width=1, fill_color='dodgerblue',
                             line_color='black')
    glyph_ls = plot.multi_line('xs', 'ys', source=source_vor_ls, alpha=0, line_width=1, line_color='black')

    checkbox_def = CheckboxButtonGroup(labels=["Team Defend"], width=100)
    checkbox_att = CheckboxButtonGroup(labels=["Team Attack"], width=100)
    checkbox_vor = CheckboxButtonGroup(labels=["Voronoi"], width=100)

    checkbox_def.callback = CustomJS(args=dict(l0=team_def_patch, checkbox=checkbox_def), code="""
        l0.visible = 0 in checkbox.active;
        l0.glyph.fill_alpha = 0.3;
        """)

    checkbox_att.callback = CustomJS(args=dict(l0=team_att_patch, checkbox=checkbox_att), code="""
        l0.visible = 0 in checkbox.active;
        l0.glyph.fill_alpha = 0.3;
        """)

    checkbox_vor.callback = CustomJS(args=dict(l0=glyph_vor, l1=glyph_ls, checkbox=checkbox_vor), code="""
        l0.visible = 0 in checkbox.active;
        l0.glyph.fill_alpha = .1;
        l0.glyph.line_alpha = 1;
        l1.visible = 0 in checkbox.active;
        l1.glyph.fill_alpha = .1;
        l1.glyph.line_alpha = 1;
        """)

    text_p = Paragraph(text="""Select a team to visualize convex hull""", width=250)

    inputs = widgetbox(row(column(game_time, button),
                           row(column(text_p, row(checkbox_def, checkbox_att)), checkbox_vor)))

    """
       Plot the speed and distance if true
    """
    if not show_dist_speed:
        layout = column(row(column(plot, inputs)))
    else:
        layout = column(row(column(plot, inputs),row(column(plot_distance_def, avg_speed_def),column(plot_distance_att, avg_speed_att))))

    doc.add_root(layout)
    doc.title = "Game Animation"

    return doc

