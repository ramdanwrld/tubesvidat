import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.io import show,output_notebook,output_file,curdoc
from bokeh.models import FileInput
from bokeh.models import Button,CheckboxButtonGroup,CustomJS,DatePicker,MultiSelect,ColumnDataSource, DataTable, DateFormatter, TableColumn,Select, FactorRange,Slider,Button,PreText,Toggle
from bokeh.layouts import row,column,gridplot
from bokeh.plotting import figure
from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from pandas import DataFrame
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6
from bokeh.models import CustomJS, RadioButtonGroup
from bokeh.models.widgets import Tabs, Panel
from bokeh.events import ButtonClick
from bokeh.layouts import column

df = pd.read_csv('app/data/android-games.csv')


'''output_file("bar.html")'''

name = df['title'].head(50)
counts = df['total ratings'].head(50)
source = ColumnDataSource(data=dict(name=name, counts=counts))
p = figure(x_range=name, height=800,width=1000, toolbar_location="right", title="Top Android Game Playstore (50 Games Highest to low) ")
p.vbar(x=name, top=counts, width=0.9)
plt.xticks(counts, name)
p.xaxis.major_label_orientation = "vertical"
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.y_range.end = 90000000
'''output_file("pie.html")'''

x = df['category'].value_counts()


data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'category'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]

p1 = figure(height=500,width=800, title="Game Category", toolbar_location='right',
           tools="hover", tooltips="@category: @value", x_range=(-0.5, 1.0))

p1.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='category', source=data)

p1.axis.axis_label = None
p1.axis.visible = False
p1.grid.grid_line_color = None

theme = 'dark_minimal'
curdoc().theme = theme

data = dict(
        title=[a for a in df["title"]],
        category=[category for category in df['category']],
        paid=[paid for paid in df['paid']]
    )
source = ColumnDataSource(data)
columns = [
        TableColumn(field="title", title="Game Name"),
        TableColumn(field="category", title="Category"),
        TableColumn(field="paid", title="Paid ? T/F"),
    ]
data_table = DataTable(source=source, columns=columns, width=400, height=280)

first_panel = Panel(child=p, title='Bar Charts')
second_panel = Panel(child=p1, title='Pie Charts')
tabs = Tabs(tabs=[first_panel, second_panel])

show(row(tabs,data_table))
curdoc().add_root(row(tabs,data_table))