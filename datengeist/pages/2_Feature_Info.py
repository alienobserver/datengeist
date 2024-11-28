import pandas as pd
import streamlit as st
import pandas.api.types as ptypes

from datengeist.config.config import set_layout, init_uploader, init_db
from datengeist.utils.feature_tools import is_categorical
from datengeist.utils.session_control import get_st_session_df, set_initial_variable_to_current, get_state_variable
from datengeist.utils.style import set_st_hz_block, add_top_margin_div
from datengeist.visual.distribution_chart import hist_chart, box_chart, pie_chart
from datengeist.visual.missing_value import MissingValPieChart


def feature_info_charts():
    """
    Displays detailed information about each feature in the dataset. Allows users to:
    - Select a feature and view its type (e.g., numerical, categorical).
    - Visualize data distribution for numerical and categorical features.
    - Analyze missing values, if any.
    """
    st.header('Feature Info')

    # Retrieve the DataFrame from session state
    dataframe = get_st_session_df('sampled_df')

    # Initialize session variables for selection and thresholds
    set_initial_variable_to_current('select_box_feature_info')
    set_initial_variable_to_current('slider_columns_division_threshold')
    set_initial_variable_to_current('text_input_missing')

    nominal_features = dataframe.select_dtypes(include=['object'])
    for col in nominal_features:
        set_initial_variable_to_current(f'text_input_missing_{col}')

    if not dataframe.empty:
        # Center the main content
        set_st_hz_block('center')

        # Sidebar controls for feature selection and threshold setting
        with st.sidebar:
            # Dropdown for feature selection
            initial_select_box_value = get_state_variable('select_box_feature_info', dataframe.columns)
            select_box_feature_info = st.selectbox(
                "Feature",
                options=dataframe.columns,
                index=initial_select_box_value,
                key='select_box_feature_info',
                help="Select the feature to analyze"
            )

            # Threshold for categorizing data into continuous or categorical
            slider_columns_division_threshold_value = get_state_variable('slider_columns_division_threshold')
            columns_division_threshold = st.number_input(
                'Threshold',
                min_value=0.01,
                max_value=0.99,
                value=slider_columns_division_threshold_value,
                key='slider_columns_division_threshold',
                help='Set the threshold for distinguishing continuous from categorical data'
            )

        # Analysis and Visualization for Selected Feature
        if select_box_feature_info:
            if ptypes.is_numeric_dtype(dataframe[select_box_feature_info]):
                _render_numeric_feature_info(dataframe, select_box_feature_info, columns_division_threshold)
            elif ptypes.is_object_dtype(dataframe[select_box_feature_info]):
                _render_categorical_feature_info(dataframe, select_box_feature_info, columns_division_threshold)
    else:
        # Show navigation to sample page if the dataset is empty
        st.page_link('Sample_Dataset.py', label="Sample the data first!")


def _render_numeric_feature_info(dataframe: pd.DataFrame, feature_name: str, threshold: float):
    """
    Renders information and visualizations for a selected numerical feature.
    """
    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        feature_type = 'Ordinal' if is_categorical(dataframe[feature_name], threshold) else 'Numerical'
        st.metric("Feature Name", feature_name)
        st.metric("Feature Type", feature_type)

    with col2:
        if dataframe[feature_name].dropna().shape[0] > 0:
            histogram_chart_fig = hist_chart(dataframe, feature_name)
            box_chart_fig = box_chart(dataframe, feature_name)

            # Toggle between histogram and box plot
            change_chart = st.toggle('Show Histogram')
            st.plotly_chart(histogram_chart_fig if change_chart else box_chart_fig)

        else:
            st.subheader("The feature consists of only NaN values")

    with col3:
        add_top_margin_div(56)

        # Display missing values pie chart if missing values exist
        missing_val_chart = MissingValPieChart(dataframe)
        missing_val_chart.update_feature(feature_name)
        st.plotly_chart(missing_val_chart.get_missing_values_chart())


def _render_categorical_feature_info(dataframe: pd.DataFrame, feature_name: str, threshold: float):
    """
    Renders information and visualizations for a selected categorical feature.
    """
    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        feature_type = 'Categorical' if is_categorical(dataframe[feature_name], threshold) else 'Identifier'
        st.metric("Feature Name", feature_name)
        st.metric("Feature Type", f"Nominal {feature_type}")
        st.metric("Categories", len(dataframe[feature_name].unique()))

    with col2:
        if dataframe[feature_name].dropna().shape[0] > 0:
            # Display pie chart for categorical distribution
            categorical_chart = pie_chart(dataframe, feature_name)
            st.plotly_chart(categorical_chart)

        else:
            st.subheader("The feature consists of only NaN values")
    with col3:
        # Allow user to specify keywords for NaN values and display missing values chart
        with st.sidebar:
            missing_data_keywords = st.text_input(
                "NaN Keywords",
                get_state_variable(f'text_input_missing_{feature_name}'),
                key=f'text_input_missing_{feature_name}',
                help="Specify keywords to recognize as NaN (comma-separated)"
            )

        missing_val_chart = MissingValPieChart(dataframe)
        missing_val_chart.update_feature(feature_name, missing_data_keywords)
        st.plotly_chart(missing_val_chart.get_missing_values_chart())

if __name__ == "__main__":
    set_layout()
    init_db()

    feature_info_charts()