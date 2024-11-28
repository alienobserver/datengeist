from functools import partial

import pandas as pd

import streamlit as st

from datengeist.utils.feature_tools import count_missing_values_column
from datengeist.utils.helper import truncate_str
from datengeist.utils.session_control import get_state_variable


class MissingValPieChart:
    def __init__(self, dataframe: pd.DataFrame, max_str_len: int=15):
        """
        Initializes the MissingValPieChart object with a dataframe and an optional max string length for column names.

        Parameters:
        - dataframe (pd.DataFrame): The DataFrame containing the data for the missing value analysis.
        - max_str_len (int): Maximum length of the feature name to display in the chart (default is 15).
        """
        self.dataframe = dataframe
        self.max_str_len = max_str_len
        self.feature = None

        self.missing_data_count = None
        self.complete_data_count = None
        self.formatted_data = None
        self.truncate_categories = None
        self.truncated_categories = None

        self.truncated_title = "Missing Data"

    def update_feature(self, feature, missing_data_keywords=None):
        """
        Updates the feature to analyze and computes the counts of missing and complete data for the feature.

        Parameters:
        - feature (str): The name of the feature (column) to analyze for missing data.
        - missing_data_keywords (str): Optional string of keywords to identify missing data.
            If provided, it will filter the missing values based on these keywords.

        Raises:
        - ValueError: If the provided feature is not a valid column name in the DataFrame.
        """
        if feature not in self.dataframe.columns:
            raise ValueError(f"{feature} is not a valid column name!")

        self.feature = feature

        # Count missing data based on keywords if provided
        if missing_data_keywords:
            missing_data_keywords_list = missing_data_keywords.split(',')
            missing_data_keywords_list_unique_values = list(set(missing_data_keywords_list))
            filtered_missing_data_keywords_list = list(filter(None, missing_data_keywords_list_unique_values))
            self.missing_data_count = count_missing_values_column(self.dataframe, self.feature, filtered_missing_data_keywords_list)
        else:
            self.missing_data_count = count_missing_values_column(self.dataframe, self.feature)

        self.complete_data_count = self.dataframe[self.feature].shape[0] - self.missing_data_count

        # Prepare the formatted data for the pie chart
        self.formatted_data = pd.DataFrame({
            'Category': ['Missing Data', 'Complete Data'],
            'Values': [self.missing_data_count, self.complete_data_count]
        })

        # Truncate the category names to the max string length
        self.truncate_categories = partial(truncate_str, max_str_len=self.max_str_len)
        self.truncated_categories = self.formatted_data['Category'].apply(lambda x: self.truncate_categories(x))

    def _get_pie_trace(self):
        """
        Creates the Pie trace for the Plotly chart.

        Returns:
        - go.Pie: The Pie trace object for visualizing the missing vs complete data.
        """
        pie_trace = go.Pie(
            labels=self.truncated_categories,
            values=self.formatted_data['Values'],
            hole=0.4,  # Hole size for the donut chart
            textinfo='percent',  # Show the percentage on the chart
            hoverinfo='label+percent',
            marker=dict(
                colors=['#BE0019', '#29AA81']  # Color scale for the pie chart
            ),
            pull=[0.1, 0]  # Pull the first segment slightly out for emphasis
        )

        return pie_trace

    def get_missing_values_chart(self):
        """
        Generates the donut pie chart showing the proportion of missing and complete data for the selected feature.

        Returns:
        - go.Figure: The Plotly figure containing the donut pie chart.
        """
        fig = go.Figure()

        # Add the pie trace to the figure
        pie_trace = self._get_pie_trace()
        fig.add_trace(pie_trace)

        # Update layout with title and legend settings
        fig.update_layout(
            title=dict(
                text=self.truncated_title,
                y=0.95,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=24)
            ),
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",
                y=-.2,
                xanchor="center",
                x=0.5
            )
        )

        return fig

import pandas as pd
import plotly.graph_objects as go
import numpy as np

def missing_values_bar_chart(dataframe: pd.DataFrame, max_str_len: int = 15) -> go.Figure:
    """
    Creates a bar chart to show the count of missing values (NaNs) per column in the DataFrame.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing the data.
        max_str_len (int, optional): The maximum length for truncating column names in the plot (default is 15).

    Returns:
        go.Figure: A Plotly figure containing the bar chart of NaN counts.
    """
    # Initialize a dictionary to store the count of NaNs for each column
    nan_counts = {}

    # Identify nominal (categorical) features in the dataframe
    nominal_features = dataframe.select_dtypes(include=['object'])

    # Loop through each column to calculate NaN counts
    for col in dataframe.columns:
        # For nominal features, apply specific handling if needed
        if col in nominal_features.columns:
            missing_value = get_state_variable(f'text_input_missing_{col}', None)
            if missing_value:  # Ensure it's not None or empty
                missing_data_keywords_list = missing_value.split(',')
                missing_data_keywords_list_unique_values = list(set(missing_data_keywords_list))
                filtered_missing_data_keywords_list = list(filter(None, missing_data_keywords_list_unique_values))
                nan_counts[col] = count_missing_values_column(dataframe, col, filtered_missing_data_keywords_list)
            else:
                missing_data_keywords_list = st.session_state[f'backup_text_input_missing_{col}'].split(',')
                missing_data_keywords_list_unique_values = list(set(missing_data_keywords_list))
                filtered_missing_data_keywords_list = list(filter(None, missing_data_keywords_list_unique_values))
                nan_counts[col] = count_missing_values_column(dataframe, col, filtered_missing_data_keywords_list)
        else:
            # For non-nominal features, count missing values normally
            nan_counts[col] = count_missing_values_column(dataframe, col)

    # Convert the dictionary to a pandas Series for easy manipulation
    nan_counts_pd_series = pd.Series(nan_counts)

    # Calculate the percentage of NaN values per column
    nan_counts_pct = (nan_counts_pd_series.sort_values(ascending=False) / dataframe.shape[0]).round(3)
    # Filter out columns with 0 NaN values
    nan_counts_without_zeros = nan_counts_pct[nan_counts_pct != 0]

    # Create a bar plot using Plotly
    fig = go.Figure()

    # Truncate column names for display purposes
    stripped_columns = np.array(list(map(lambda x: truncate_str(x, max_str_len), nan_counts_without_zeros.index)))

    # Bar chart trace
    nan_bar_chart = go.Bar(
        x=stripped_columns,  # Column names
        y=nan_counts_without_zeros.values,  # NaN counts
        marker=dict(
            color='#D03112',
            line=dict(color='black', width=1)
        ),
        text=nan_counts_without_zeros.values,  # Display the count on each bar
        textposition='auto'  # Position text in the middle of the bar
    )

    # Add the bar chart trace to the figure
    fig.add_trace(nan_bar_chart)

    # Update layout with titles and axis labels
    fig.update_layout(
        title=dict(
            text="NaN Counts per Column",
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        xaxis_title="Columns",
        yaxis_title="NaN Count",
        template="plotly_dark",  # Optional: change theme for better aesthetics
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickangle=45  # Rotate x-axis labels for better readability
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.2)'
        ),
    )

    return fig
