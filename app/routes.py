from app import app
from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure

import random
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import pandas as pd


load_dotenv()

GH_TOKEN = os.environ["GITHUB_TOKEN"]
GH_USERNAME = os.environ["GITHUB_USERNAME"]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/bokeh-multi')
def bokeh_multi():
    # First chart - scatter plot
    p1 = figure(height=350, sizing_mode="stretch_width")
    p1.circle(
        [i for i in range(10)],
        [random.randint(1,50) for j in range(10)],
        size=20,
        color="navy",
        alpha=0.5
    )

    # Second chart - line plot
    language = ["Python", "JavaScript", "C++", "C#", "Java", "Golang"]
    popularity = [85, 91, 63, 58, 80, 77]

    p2 = figure(
        x_range=language,
        height=350,
        title="Popularity",
    )
    p2.vbar(x=language, top=popularity, width=0.5)
    p2.xgrid.grid_line_color = None
    p2.y_range.start = 0

    # Third chart - line plot
    p3 = figure(height=350, sizing_mode="stretch_width")
    p3.line(
        [i for i in range(10)],
        [random.randint(1,50) for j in range(10)],
        line_width=2,
        color="olive",
        alpha=0.5
    )

    script1, div1 = components(p1)
    script2, div2 = components(p2)
    script3, div3 = components(p3)

    # Return all charts to HTML template
    return render_template(
        template_name_or_list='bokeh-multi.html',
        script=[script1, script2, script3],
        div=[div1, div2, div3],
    )

@app.route('/chartjs')
def chartjs():

    # Define plot data
    labels = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    data = [0, 10, 15, 8, 22, 18, 25, 10, 15, 8, 22, 18, 25]

    # Return components to HTML template
    return render_template(
        template_name_or_list='chart-js.html',
        data=data,
        labels=labels,
    )

# @app.route('/github')
def github_events():
    headers = {
        "accept": "application/vnd.github+json",
        "authorization": f"Bearer {GH_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    api_url = "https://api.github.com"

    user_events = f"{api_url}/users/{GH_USERNAME}/events"

    response = requests.get(url=user_events, headers=headers)
    response.raise_for_status()
    events = response.json()

    df = pd.json_normalize(events)



    # return events

github_events()



# @app.route('/git-chart')
# def chart_api():
#     events = github_events()
#     labels = [
#         'CreateEvent',
#         'PushEvent'
#     ]
#
#     # for i in events:
#     #     timestamp = i["created_at"]
#     #     type = i["type"]
#
#     data = [i["type"].count() for i in events]



    # return render_template(
    #     template_name_or_list='chart-js.html',
    #     data=data,
    #     labels=labels,
    # )


