import datetime as dt

import utils

def metric_to_imperial(activity):
    activity['average_speed'] = utils.meters_per_second_to_min_per_mile(activity['average_speed'])
    activity['max_speed'] = utils.meters_per_second_to_min_per_mile(activity['max_speed'])
    activity['distance'] = utils.meters_to_miles(activity['distance'])
    activity['elev_high'] = utils.meters_to_feet(activity['elev_high'])
    activity['elev_low'] = utils.meters_to_feet(activity['elev_low'])
    activity['total_elevation_gain'] = utils.meters_to_feet(activity['total_elevation_gain'])

    return activity

def get_activities(client, limit=25, imperial=True):
    activities = {}

    for activity in client.get_activities(limit=limit):
        data = {k: v for k, v in activity.to_dict().items() if v is not None}

        # Convert datetime and timedeltas
        data = {k: v.total_seconds() if isinstance(v, dt.timedelta) else v for k, v in data.items()}
        data = {k: str(v) if isinstance(v, dt.datetime) else v for k, v in data.items()}

        # Add readable time formats
        data['elapsed_time_seconds'] = data.pop('elapsed_time')
        data['elapsed_time'] = utils.seconds_to_hhmmss(data['elapsed_time_seconds'])
        data['moving_time_seconds'] = data.pop('moving_time')
        data['moving_time'] = utils.seconds_to_hhmmss(data['moving_time_seconds'])

        if imperial:
            data = metric_to_imperial(data)

        data['athlete'] = data['athlete']['id']
        activities[activity.id] = data

    return activities
