import streamlit as st

from datengeist.config.config import set_layout, init_uploader, init_db
from datengeist.utils.session_control import get_st_session_df
from datengeist.utils.style import add_top_margin_div
from datengeist.visual.distribution_chart import feature_categories_pie_chart
from datengeist.visual.missing_value import missing_values_bar_chart


def general_info():
    """
    Displays general information about the dataset, including the number of instances and features,
    feature category distribution, and the presence of missing values.

    This page uses data from a sampled DataFrame stored in Streamlit's session state under the key 'sampled_df'.
    """
    st.header('General Info')

    # Retrieve the sampled dataset from session state
    dataframe = get_st_session_df('sampled_df')

    # Check if the dataset is available and contains data
    if not dataframe.empty:
        # Add visual spacing for UI alignment
        add_top_margin_div(25)

        # Define two main columns for displaying metrics and charts
        col1, col2 = st.columns(2, gap='large')

        # Column 1: Dataset size metrics and feature category distribution
        with col1:
            # Sub-columns for displaying instance and feature counts
            col11, col12 = st.columns(2, gap='large')
            col11.metric('Number of Instances', dataframe.shape[0])
            col12.metric('Number of Features', dataframe.shape[1])

            # Add spacing and display the feature category distribution chart
            add_top_margin_div(50)
            st.plotly_chart(feature_categories_pie_chart(dataframe, threshold=0.1))

        # Column 2: Completeness metrics and missing values visualization
        with col2:
            # Sub-columns for displaying completeness percentage metrics
            col21, col22 = st.columns(2, gap='large')

            # Calculate percentages of complete and incomplete instances
            complete_instances_pct = round(dataframe.dropna().shape[0] / dataframe.shape[0] * 100, 1)
            incomplete_instances_pct = round(100 - complete_instances_pct, 1)

            col21.metric('Percentage of Complete Instances', f'{complete_instances_pct} %')
            col22.metric('Percentage of Incomplete Instances', f'{incomplete_instances_pct} %')

            # Add spacing and display missing values bar chart if there are NaN values
            add_top_margin_div(50)
            nan_values_chart = missing_values_bar_chart(dataframe)

            if dataframe.isna().sum().sum() > 0:
                st.plotly_chart(nan_values_chart)
            else:
                st.write("No NaN values found in the dataset")

    # Prompt the user to sample the data if the dataset is unavailable
    else:
        st.page_link('Sample_Dataset.py', label="Sample the data first!")

if __name__ == "__main__":
    set_layout()
    init_db()

    general_info()