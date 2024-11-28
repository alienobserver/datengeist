from functools import partial
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

from datengeist.utils.feature_tools import filter_str_categorical_features, \
    filter_num_categorical_features, filter_continuous_features
from datengeist.utils.helper import truncate_str
from datengeist.utils.style import ColorGenerator


def box_chart(dataframe: pd.DataFrame, column: str, max_str_len: int = 15) -> go.Figure:
    """
    Generates a box plot to visualize the distribution of a column in the DataFrame.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing the data.
        column (str): The column name for which the box plot will be generated.
        max_str_len (int): The maximum length for truncated column names (default is 15).

    Returns:
        go.Figure: A Plotly figure containing the box plot.
    """

    # Prepare data, dropping NaN values
    chart_data = pd.DataFrame({"Value": dataframe[column].dropna()})

    # Create figure
    fig = go.Figure()

    # Add box plot trace
    fig.add_trace(go.Box(
        y=chart_data["Value"],
        name=column,
        boxpoints='outliers',
        marker=dict(color='#B67108'),
    ))

    # Update layout with titles
    fig.update_layout(
        title=dict(
            text="Box Distribution",
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        yaxis=dict(
            title=dict(
                text=column,
                font=dict(size=16)
            ),
            zeroline=True,
        )
    )

    return fig


def hist_chart(dataframe: pd.DataFrame, df_col: str) -> go.Figure:
    """
    Creates a histogram for a specified column in the DataFrame, with an overlaid normal distribution curve.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        df_col (str): The column name to be visualized.

    Returns:
        go.Figure: A Plotly figure containing the histogram and the normal distribution curve.
    """

    # Clean data by removing NaN values
    data = dataframe[df_col].dropna()

    # Create figure
    fig = go.Figure()

    # Add histogram trace
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=50,
        name=df_col,
        histnorm='probability density',
        marker=dict(color='#5D8D06', line=dict(color='black', width=1)),
        opacity=0.75
    ))

    # Add normal distribution curve
    x = np.linspace(min(data), max(data), 1000)
    y = norm.pdf(x, np.mean(data), np.std(data))

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Normal Distribution',
        line=dict(color='#B1B1B1')
    ))

    # Update layout with appropriate titles and style
    fig.update_layout(
        title=dict(
            text="Histogram with Normal Distribution",
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        xaxis_title="Value",
        yaxis_title="Density",
        showlegend=True,
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(128,128,128,0.2)', zeroline=True),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)', zeroline=True),
        legend=dict(orientation="h", yanchor="top", y=-.2, xanchor="center", x=0.4)
    )

    return fig


def pie_chart(dataframe: pd.DataFrame, column: str, max_cats: int = 10, max_str_len: int = 15) -> go.Figure:
    """
    Generates a donut pie chart to show the distribution of categories in a column.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        column (str): The column name containing the categorical data.
        max_cats (int): The maximum number of categories to show before grouping the rest as "Others".
        max_str_len (int): Maximum length of category names before truncating them.

    Returns:
        go.Figure: A Plotly figure containing the donut pie chart.
    """
    # Count the occurrences of each category
    df_value_counts = dataframe[column].value_counts()
    df_value_counts_top = df_value_counts.head(max_cats)

    print(df_value_counts)

    others = df_value_counts[max_cats:].sum()
    others_pd_series = pd.Series({'Others': others})
    df_most_frequent_with_others = pd.concat([df_value_counts_top, others_pd_series])

    # Prepare category counts
    category_counts = df_most_frequent_with_others if len(df_value_counts) > max_cats else df_value_counts_top

    # Format data for pie chart
    formatted_data = pd.DataFrame({
        'Category': category_counts.index,
        'Values': category_counts.values
    })

    # Truncate category names for better display
    truncate_categories = partial(truncate_str, max_str_len=max_str_len)
    truncated_categories = formatted_data['Category'].apply(lambda x: truncate_categories(x))

    gen_colors = ColorGenerator(lightness=0.5, saturation=0.6)
    custom_colors = gen_colors.generate_hex_colors(11)

    # Create figure for the donut pie chart
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=truncated_categories,
        values=formatted_data['Values'],
        hole=0.4,  # Hollow center for the donut chart
        textinfo='label+percent',  # Show label and percent
        hoverinfo='label+percent+value',
        marker=dict(
            colors=custom_colors
        )
    ))

    # Update layout
    fig.update_layout(
        title=dict(
            text="Categories",
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        legend=dict(orientation="h", yanchor="top", y=-.2, xanchor="center", x=0.5)
    )

    return fig


def feature_categories_pie_chart(dataframe: pd.DataFrame, threshold: float) -> go.Figure:
    """
    Generates a donut pie chart showing the distribution of different feature types in the DataFrame.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        threshold (float): The threshold for filtering features based on their non-null values.

    Returns:
        go.Figure: A Plotly figure containing the donut pie chart showing feature types.
    """
    # Filter features by their types
    str_categorical_features = filter_str_categorical_features(dataframe, threshold)
    num_categorical_features = filter_num_categorical_features(dataframe, threshold)
    num_continuous_features = filter_continuous_features(dataframe, threshold)

    # Calculate feature type proportions
    str_categorical_features_pct = len(str_categorical_features) / dataframe.shape[1]
    num_categorical_features_pct = len(num_categorical_features) / dataframe.shape[1]
    num_continuous_features_pct = len(num_continuous_features) / dataframe.shape[1]

    others_count = 1 - str_categorical_features_pct - num_continuous_features_pct - num_categorical_features_pct

    # Prepare data for pie chart
    formatted_data = pd.DataFrame({
        'Category': ['Nominal Categorical Features', 'Ordinal Features', 'Numerical Features', 'Others'],
        'Values': [str_categorical_features_pct, num_categorical_features_pct, num_continuous_features_pct,
                   others_count]
    })

    gen_colors = ColorGenerator(lightness=0.5, saturation=0.6)
    custom_colors = gen_colors.generate_hex_colors(4)

    # Create figure for the feature type donut pie chart
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=formatted_data['Category'],
        values=formatted_data['Values'],
        hole=0.4,  # Hollow center for the donut chart
        textinfo='percent',  # Show only percentage
        hoverinfo='label+percent',
        marker=dict(colors=custom_colors)
    ))

    # Update layout
    fig.update_layout(
        title=dict(
            text="Feature Types",
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-.2,
            xanchor="center",
            x=0.5
        )
    )

    return fig
