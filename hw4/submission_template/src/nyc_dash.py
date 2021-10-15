from bokeh.plotting import figure, curdoc
from bokeh.palettes import RdYlBu3
from bokeh.models import Button, Dropdown, ColumnDataSource
from bokeh.layouts import column
from random import random
from bokeh.plotting import figure, show
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

ALL_DATA = os.path.join(DATA_DIR, 'all.csv')

df_all = pd.read_csv(ALL_DATA)

source = ColumnDataSource(df_all)
zipList = []

with open(os.path.join(DATA_DIR, 'zip.txt')) as f:
    zipList = f.read().split()
    
menu = [(a, b) for a, b in zip(zipList, zipList)]

zip_source_dict = {}
for zip in zipList:
    zip_source_dict[zip] = ColumnDataSource(pd.read_csv(
        os.path.join(DATA_DIR, f'{zip}.csv')))

dropdown1 = Dropdown(label="zipcode 1", menu=menu)
dropdown2 = Dropdown(label="zipcode 2", menu=menu)


# create a new plot with a title and axis labels
p = figure(title="Monthly average incident creat-to-closed time (in hours)", x_axis_label="Month", y_axis_label="Average time (in hours)")

# add a line renderer with legend and line thickness

l1 = p.line(x='end', y='delta', source=dict(zip_source_dict[zipList[0]].data), legend_label=zipList[0], line_width=2, line_color='green')
l2 = p.line(x='end', y='delta', source=dict(
    zip_source_dict[zipList[1]].data), legend_label=zipList[1], line_width=2)
p.line(x='end', y='delta', source=source, legend_label="All 2020 data", line_width=2, line_color='red')

ds1 = l1.data_source
ds2 = l2.data_source
# curdoc().add_root(column(p))
# show the results


def handler1(event):
    ds1.data = dict(zip_source_dict[event.item].data)
    p.legend.items[0].label['value'] = event.item


def handler2(event):
    ds2.data = dict(zip_source_dict[event.item].data)
    p.legend.items[1].label['value'] = event.item


dropdown1.on_click(handler1)
dropdown2.on_click(handler2)

show(column(dropdown1, dropdown2, p))
curdoc().add_root(column(dropdown1, dropdown2, p))


# create a plot and style its properties
# p = figure()
# # p.border_fill_color = 'black'
# # p.background_fill_color = 'black'
# # p.outline_line_color = None
# # p.grid.grid_line_color = None

# # add a text renderer to the plot (no data yet)
# # r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="26px",
# #            text_baseline="middle", text_align="center")

# # i = 0

# # ds = r.data_source

# # create a callback that adds a number in a random location


# def callback():
#     global i

#     # BEST PRACTICE --- update .data in one step with a new dict
#     new_data = dict()
#     new_data['x'] = ds.data['x'] + [random()*70 + 15]
#     new_data['y'] = ds.data['y'] + [random()*70 + 15]
#     new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i % 3]]
#     new_data['text'] = ds.data['text'] + [str(i)]
#     ds.data = new_data

#     i = i + 1


# # add a button widget and configure with the call back
# button = Button(label="Press Me")
# button.on_click(callback)

# # put the button and plot in a layout and add to the document
# curdoc().add_root(column(button, p))
