import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import re


from dataclasses import dataclass, field, make_dataclass, asdict
from typing import List, Tuple
import pandas as pd

import csv


@dataclass
class Frame_Info:
    frame_number: int
    new_people_count: int
    total_people_in_frame: int
    cumulative: int
    flow: List[Tuple[float, float, float]]
    coords: List[Tuple[float, float, float]]
    
    
    
fps = 30


#current_video_data = pd.read_csv("pandas_csv.csv")


#returns figure of a graph for custmers per day, given the list of the CSV data lines, with a time interval in mins
def generate_customerspertime_graph(dataFrame, time_interval: float):
    
    df = dataFrame.copy(deep=True)
    
    df['time_min'] = df['frame_number'] / (30 * 60)

    # floor the time_min to the nearest time_interval
    df['time_bin'] = (df['time_min'] // time_interval).astype(int) * time_interval
    
    agg = (
    df
    .groupby('time_bin', as_index=False)
    .agg(last_cum=('cumulative', 'last'))
    )
    # compute new people in each bin
    agg['new_people'] = agg['last_cum'].diff().fillna(agg['last_cum'])


    error_factor = 10
    agg['new_people'] = agg['new_people']/error_factor
    # 5) Plot
    plt.figure(figsize=(8,4))
    
    fig = Figure(figsize=(8,4))
    
    sns.lineplot(
        x='time_bin',
        y='new_people',
        data=agg,
        marker='o'
    )
    
    plt.xlabel(f'Time (minutes, bin={time_interval}m)')
    plt.ylabel(f'New people per {time_interval} min')
    plt.title('People flow per interval')
    plt.tight_layout()
    plt.show()


#get the average number of people
def generate_averagepeople_graph(dataFrame, time_interval: float):
    df = dataFrame.copy(deep=True)
    
    #2) Compute time in minutes
    df['time_min'] = df['frame_number'] / (fps * 60.0)

    # 3) Floor into bins of width=interval_len
    df['time_bin'] = (df['time_min'] // time_interval).astype(int) * time_interval

    # 4) Group & compute average people per frame in each bin
    summary = (
        df
        .groupby('time_bin', as_index=False)
        .agg(
            avg_people=('total_people_in_frame', 'mean'),
            frames_in_bin=('frame_number','count')   # optional
        )
    )

    # 5) Plot
    plt.figure(figsize=(8, 4))
    '''if kind == "bar":
           sns.barplot(
            x='time_bin',
            y='avg_people',
            data=summary,
            color='C1'
        )
    else:'''
    sns.lineplot(
        x='time_bin',
        y='avg_people',
        data=summary,
        marker='o'
    )

    plt.xlabel(f'Time (minutes, bin={time_interval}m)')
    plt.ylabel('Average people per frame')
    plt.title(f'Average # of People per {time_interval}-min Interval')
    plt.tight_layout()
    plt.show()
    

def generate_scatterplot(dataFrame, width, height):
    df = dataFrame.copy(deep=True)
    x_coords = []
    y_coords = []
    for coord_list in df['coords']:
        for obj_id, x, y in coord_list:
            x_coords.append(x)
            y_coords.append(height - y)
    
    plt.figure(figsize=(width, height))
    plt.scatter(x_coords, y_coords, s=3, alpha=0.6, color='blue')

    plt.title("All Object Coordinates Across Frames")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()
        
    
    


#generate_customerspertime_graph("pandas_csv.csv", 1.5)
