from flask import Flask, render_template, request, url_for
from stravalib.client import Client
import plotly

from activities import get_activities
from plotting import plot_pace_vs_elevation
import token_utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', dashboard_url=url_for('dashboard'))

import json
import pandas as pd
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    workout_dropdown = 'All'
    activity_rb = 'All'

    if request.method == 'POST':
        workout_dropdown = request.form.get('quantity')
        activity_rb = request.form.get('activity_type')

        if workout_dropdown == 'All':
            num_workouts = -1
        else:
            num_workouts = workout_dropdown

        if activity_rb == 'Run':
            activity_filter = ['Run', 'TrailRun']
        elif activity_rb == 'Ride':
            activity_filter = ['Ride', 'GravelRide']
        else:
            activity_filter = ['Run', 'TrailRun', 'Ride', 'GravelRide']

        activities_df = get_dashboard_activities(activity_filter, num_workouts)


        fig = plot_pace_vs_elevation(activities_df)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template(
            'dashboard.html',
            selected_activity=activity_rb,
            quantity=workout_dropdown,
            graphJSON=graphJSON,
            tables=[activities_df.to_html(classes='data')],
            titles=activities_df.columns.values
        )

    return render_template(
        'dashboard.html',
        selected_activity=activity_rb,
        quantity=workout_dropdown
    )

def get_dashboard_activities(activity_filter, num_workouts):
    client = Client()
    token_info = token_utils.load_token_info()
    client.access_token = token_info['APP_ACCESS_TOKEN']

    workouts = get_activities(client, limit=None)
    workouts = {k: v for k, v in workouts.items() if v['sport_type'] in activity_filter}
    workouts = {k: v for k, v in list(workouts.items())[:int(num_workouts)]}

    df = pd.DataFrame({
        'Date': [a['start_date_local'] for a in workouts.values()],
        'Activity Name': [a['name'] for a in workouts.values()],
        'Sport': [a['sport_type'] for a in workouts.values()],
        'Distance': [a['distance'] for a in workouts.values()],
        'Moving Time': [a['moving_time'] for a in workouts.values()],
        'Pace': [a['average_speed'] for a in workouts.values()],
        'Elevation Gain': [a['total_elevation_gain'] for a in workouts.values()]
    })

    return df


if __name__ == '__main__':
    app.run(debug=True)
