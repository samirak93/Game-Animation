# -*- coding: utf-8 -*-

#Last Update 30-Jun-19

# ignore warnings
import warnings
import sys

# importing pandas and numpy
import numpy as np
import pandas as pd

#importing bokeh functions
from bokeh.models import ColorBar,BasicTicker,PrintfTickFormatter,HoverTool, LogColorMapper
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.io import output_notebook,show
from bokeh.palettes import YlOrRd

from scipy.spatial.distance import cdist

output_notebook()
warnings.filterwarnings("ignore")

if sys.version_info[0] < 3:
    raise Exception("This app requires Python 3")


def marking_stats(df, headers, id_def, id_att, time_steps, attack=True, threshold=0):

    """
                Parameters
        ---------------------------
        :param df: Gets the user defined dataframe
        :param headers: Give the headers to the dataframe - Headers should be ["x", "y", "team_id", "player_id","time"]

        {x, y - int/float - Player location coordinates x and y
        team_id - int/string - Team Id for both attacking and defending teams
        player_id - int/string - Player Id for both attacking and defending team. Id for ball is optional
        time - int/float - Game time in seconds or any units.}

        :param id_def: Provide id of defending team
        :param id_att: Provide id of attacking team
        :param time_steps: Provide the slider steps
        :param attack:(True/False) - If 'True', then the attacking team is considered players marking and defending
        team is considered as players being marked. If 'false' then logic is reversed.
        :param threshold: (int) - Get the threshold to consider players as marked - players who were tagged as marked
        below threshold would not be considered.

        :return: Returns the heat map plot of % of time player being marked.

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

    if not isinstance(threshold, int):
        raise ValueError("The expected data type for threshold is a integer but a {} was provided.".format(type(threshold)))

    all_team = pd.DataFrame(df, columns=headers)

    all_team['x'] = pd.to_numeric(all_team['x'])
    all_team['y'] = pd.to_numeric(all_team['y'])
    all_team['time'] = pd.to_numeric(all_team['time'])
    all_team['player_id'] = all_team['player_id'].apply(str)

    all_team['team_id'] = np.where(((all_team['team_id'] != id_att) & (all_team['team_id'] != id_def)), -99,
                                   all_team['team_id'])
    all_team['player_id'] = np.where(((all_team['team_id'] != id_att) & (all_team['team_id'] != id_def)), " ",
                                     all_team['player_id'])
    all_team = all_team.sort_values(['time', 'team_id', 'player_id'], ascending=[True, False, True]).reset_index(
        drop=True)

    team_def = all_team[all_team.team_id == id_def]
    team_att = all_team[all_team.team_id == id_att]

    if team_def.empty:
        raise ValueError("Defending team ID is not valid. Please enter a valid team ID")

    elif team_att.empty:
        raise ValueError("Attacking team ID is not valid. Please enter a valid team ID")

    marking_df = pd.DataFrame()

    for time in range(all_team['time'].min(), all_team['time'].max()+time_steps, time_steps):

        team_def_xy = team_def[team_def.time == time]
        team_att_xy = team_att[team_att.time == time]

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
        min_dist = dist_df.min(axis=1)
        nearest_player = dist_df.idxmin(axis=1)

        dist_df['min_distance'] = min_dist
        dist_df['closest_player'] = nearest_player
        dist_df['source_player'] = index
        dist_df['source_x'] = source_x
        dist_df['source_y'] = source_y
        dist_df['time'] = [time]*len(dist_df)

        lines_x = pd.merge(dist_df, merge_df, left_on='closest_player', right_on='player_id', sort=False) \
            .rename(columns={'x': 'target_x', 'y': 'target_y'})

        marking_df = marking_df.append(lines_x[['closest_player', 'source_player', 'time', 'min_distance']])

    marking_df = marking_df.groupby(['source_player', 'closest_player']).filter(lambda x: len(x) >= threshold)

    player_groups = marking_df.groupby(['source_player', 'closest_player'])['min_distance']\
        .mean().reset_index(name='Average Distance')\
        .sort_values('Average Distance')

    player_marking_percent = marking_df.groupby(['source_player','closest_player'])['time'].count().groupby(level=0)\
                                .apply(lambda x: 100 * x / float(x.sum())).reset_index(drop=False)

    player_marking_percent['total_time'] = marking_df.groupby(['source_player', 'closest_player']) \
        .size().reset_index(name='counts')['counts'] * time_steps

    player_marking_percent['average_distance'] = marking_df.groupby(['source_player', 'closest_player'])['min_distance'] \
                                                    .mean().reset_index(name='avg_distance')['avg_distance']
    player_marking_percent = player_marking_percent.rename(columns={'time':'percent_time'})

    colors = sorted(YlOrRd[9], reverse=True)
    mapper = LogColorMapper(palette=colors, low=player_marking_percent.percent_time.min(),
                               high=player_marking_percent.percent_time.max())

    hover = HoverTool(
        tooltips="""
        <style>
        .bk-tooltip {
            background-color: black !important;
            
            }
        </style>
        
        <div style ="border-style: none;border-width: 0px;background:black;">
        <div>
            <span style="font-size: 10px;color: white;">Player Marking:</span>
            <span style="font-size: 10px;color: white;">@source_player</span>
        </div>
        <div>
            <span style="font-size: 10px;color: white;">Player Marked:</span>
            <span style="font-size: 10px;color: white;">@closest_player</span>
        </div>
        <div>
            <span style="font-size: 10px;color: white;">Total Time Marked:</span>
            <span style="font-size: 10px;color: white;">@total_time</span>
        </div>
        <div>
            <span style="font-size: 10px;color: white;">@percent_time % of @source_player's time spent on 
                marking @closest_player</span>
        </div> 
        </div>    
        """)


    plot_time = figure(title='Total time player marked',
                       x_range=list(player_marking_percent.closest_player.unique()),
                       y_range=list(player_marking_percent.source_player.unique()),
                       tools="save", height=450, width=600)

    def plot_clean(plot):
        plot.xaxis.axis_label = 'Player Marked'
        plot.yaxis.axis_label = 'Player Marking'
        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None
        plot.axis.major_label_text_font_size = "10pt"
        plot.axis.major_label_standoff = 0
        plot.border_fill_color = "white"
        plot.title.text_font = "times"
        plot.title.text_font_size = '12pt'
        plot.background_fill_color = "black"
        plot.title.align = 'center'

        return plot

    plot_time = plot_clean(plot_time)
    plot_time.rect(source=player_marking_percent, x='closest_player', y='source_player', width=0.95, height=0.95,
                fill_color={'field': 'percent_time', 'transform': mapper}, hover_line_color='white',
                line_width=2, line_color='black',
                hover_color={'field': 'percent_time', 'transform': mapper},
                fill_alpha=0.9, line_join='round')

    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="7pt",
                         ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(format="%d%%"),
                         label_standoff=6, border_line_color=None, location=(0, 0))
    plot_time.add_layout(color_bar, 'right')
    plot_time.tools.append(hover)

    dist_mapper = LogColorMapper(palette=colors, low=player_marking_percent.average_distance.min(),
                                    high=player_marking_percent.average_distance.max())

    hover = HoverTool(
        tooltips="""
        <style>
        .bk-tooltip {
            background-color: black !important;
            
            }
        </style>
        
        <div style ="border-style: none;border-width: 0px;background:black;">
        <div>
            <span style="font-size: 10px;color: white;">Player Marking:</span>
            <span style="font-size: 10px;color: white;">@source_player</span>
        </div>
        <div>
            <span style="font-size: 10px;color: white;">Player Marked:</span>
            <span style="font-size: 10px;color: white;">@closest_player</span>
        </div>
        <div>
            <span style="font-size: 10px;color: white;">Average Distance:</span>
            <span style="font-size: 10px;color: white;">@average_distance</span>
        </div>
        </div>    
        """)

    plot_dist = figure(title='Average distance between players', x_range=list(player_marking_percent.closest_player.unique()),
               y_range=list(player_marking_percent.source_player.unique()),
               tools="save", height=450, width=600)

    plot_dist = plot_clean(plot_dist)
    plot_dist.rect(source=player_marking_percent, x='closest_player', y='source_player', width=0.95, height=0.95,
                fill_color={'field': 'average_distance', 'transform': dist_mapper}, hover_line_color='white',
                line_width=2, line_color='black',
                hover_color={'field': 'average_distance', 'transform': dist_mapper},
                fill_alpha=0.9, line_join='round')

    color_bar = ColorBar(color_mapper=dist_mapper, major_label_text_font_size="7pt",
                         ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(format="%d"),
                         label_standoff=6, border_line_color=None, location=(0, 0))
    plot_dist.add_layout(color_bar, 'right')
    plot_dist.tools.append(hover)

    return show(column(plot_time, plot_dist))

