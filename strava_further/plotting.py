import plotly.express as px

def plot_pace_vs_elevation(df, sport_type_filter=None):
    """
    df: DataFrame with columns 'Activity Name', 'Sport', 'Pace', 'Elevation Gain'
    sport_type_filter: list of strings
    """

    if sport_type_filter:
        df = df[df['Sport'].isin(sport_type_filter)]

    fig = px.scatter(
        df,
        x='Elevation Gain', y='Pace',
        color='Sport',
        hover_name='Activity Name',
        trendline="lowess"
    )
    fig.update_layout(
        title='Pace vs Elevation',
        xaxis_title='Elevation (ft)',
        yaxis_title='Pace (min/mile)',
        legend_title='Sport'
    )

    return fig