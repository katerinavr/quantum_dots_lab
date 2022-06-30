import streamlit as st
from pandas import DataFrame
import numpy as np
from numpy.random import random
import plotly.graph_objects as go

def exp_surface():
    t = np.linspace(0, 20, 100)
    data1 = DataFrame(random((30, 3)))
    x, y, z = data1[0], data1[1], data1[2]

    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
        size=12,
        color=z,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
    )])

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.update_xaxes(showgrid=False)
    return fig
    