import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as pyo

from PIL import Image


def save_go_fig(figure, filename):
    figure.write_html(filename)


def viz_histogram_tss_diff(tss, sensor_name=None):
    """Creates a plotly histogram of the difference between each timestamp for a particular sensor.
    This can be used to determine if a static or variable tss has to be used in the position prediction model. 

    Args:
        tss (list): List of the timestamps associated to the sensor in a specific tracefile
        sensor_name (str): Type of sensor e.g. acc, mag, or gyro
    """
    tss_diff = np.array(tss[1:], dtype="int")-np.array(tss[:-1], dtype="int")
    df = pd.DataFrame(data={"tss_diff": tss_diff})
    fig = px.histogram(df, labels={"x": "Tss Difference", "y": "Count"})
    return fig


def figures_to_html(figs, filename, add_js=True):
    '''Saves a list of plotly figures in an html file.

    Parameters
    ----------
    figs : list[plotly.graph_objects.Figure]
        List of plotly figures to be saved.

    filename : str
        File name to save in.

    '''
    if not(os.path.isfile(filename)):
        with open(filename, 'w') as dashboard:
            dashboard.write("<html><head></head><body>" + "\n")

            for fig in figs:

                inner_html = pyo.plot(
                    fig, include_plotlyjs=add_js, output_type='div'
                )

                dashboard.write(inner_html)

            dashboard.write("</body></html>" + "\n")


def fig_acc_filter(acc_df):
    return px.line(acc_df, x="tss", y=["non_filtered_acc", "filtered_acc"])


def fig_all_waypoints(floorplan, waypoint_list):
    fig = go.Figure()

    # add floor plan
    floor_plan = Image.open(floorplan["floor_image"])
    fig.update_layout(images=[
        go.layout.Image(
            source=floor_plan,
            xref="x",
            yref="y",
            x=0,
            y=floorplan["height"],
            sizex=floorplan["width"],
            sizey=floorplan["height"],
            sizing="contain",
            opacity=1,
            layer="below",
        )
    ])

    # configure
    fig.update_xaxes(autorange=False, range=[0, floorplan["width"]])
    fig.update_yaxes(autorange=False, range=[0, floorplan["height"]], scaleanchor="x", scaleratio=1)
    fig.update_layout(
        title=go.layout.Title(
            text="No title.",
            xref="paper",
            x=0,
        ),
        autosize=True,
        width=900,
        height=200 + 900 * floorplan["height"] / floorplan["width"],
        template="plotly_white",
    )

    return fig
