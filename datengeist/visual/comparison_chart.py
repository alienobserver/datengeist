from functools import partial

import pandas as pd
import plotly.graph_objects as go

from datengeist.utils.helper import truncate_str


def comparison_box_charts(dataframe: pd.DataFrame, feature_categorical: str, feature_continuous: str,
                          max_str_len: int = 15) -> go.Figure:
    """
    Creates a box plot to compare the distributions of two columns in the DataFrame.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing the data.
        feature_categorical (str): The categorical column name to compare.
        feature_continuous (str): The continuous column name to compare.
        max_str_len (int, optional): The maximum length for truncating column names in the plot (default is 15).

    Returns:
        go.Figure: A Plotly figure containing the box plot comparison.
    """
    # partial of truncate_str function
    truncate_features = partial(truncate_str, max_str_len=max_str_len)

    # Create the chart data
    chart_data = pd.DataFrame({
        f"{feature_categorical}": dataframe[feature_categorical].dropna().astype(str).apply(truncate_features),
        f"{feature_continuous}": dataframe[feature_continuous].dropna()
    })


    # Create figure explicitly as a Figure object
    fig = go.Figure()

    box_trace = go.Box(
        x=chart_data[f"{feature_categorical}"],
        y=chart_data[f"{feature_continuous}"],
        name=f"{feature_categorical} and {feature_continuous} Comparison",
        boxpoints='outliers',
        marker=dict(color='#B67108')
    )

    # Add box plot trace
    fig.add_trace(box_trace)

    # Update layout
    fig.update_layout(
        title=dict(
            text=f"{truncate_features(feature_categorical)} and {truncate_features(feature_continuous)} Comparison",
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=24),
        ),
        showlegend=False,
        margin=dict(t=100, l=40, r=40, b=40),
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=dict(text=feature_categorical, font=dict(size=16)),
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title=dict(text=feature_continuous, font=dict(size=16)),
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.2)'
        ),
        height=600,
    )

    return fig
