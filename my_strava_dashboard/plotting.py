import plotly.express as px

def plot_pace_vs_elevation(df, sport_type_filter=None):
    """
    df: DataFrame with columns 'Activity Name', 'Sport', 'Pace', 'Elevation'
    sport_type_filter: list of strings
    """

    df = df[df['Sport'].isin(sport_type_filter)]

    fig = px.scatter(
        df,
        x='Elevation', y='Pace',
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
    fig.show()
