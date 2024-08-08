from datetime import datetime as dt

def seconds_to_hhmmss(seconds):
    return str(dt.utcfromtimestamp(seconds).strftime('%H:%M:%S'))

def meters_per_second_to_min_per_mile(mps):
    return round(60 / meters_to_miles(mps), 5)

def meters_to_miles(meters):
    return round(meters * 0.000621371, 5)

def meters_to_feet(meters):
        return round(meters * 3.28084, 5)

def meters_to_kilometers(meters):
    return round(meters * 0.001, 5)

def feet_to_meters(feet):
    return round(feet * 0.3048, 5)

def feet_to_miles(feet):
    return round(feet * 0.000189394, 5)
