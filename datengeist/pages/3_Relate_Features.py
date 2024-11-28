import streamlit as st

from datengeist.config.config import set_layout, init_db
from datengeist.utils.constants import CORR_TYPES
from datengeist.utils.feature_tools import filter_continuous_features, filter_categorical_features
from datengeist.utils.session_control import get_st_session_df, set_initial_variable_to_current, get_state_variable, \
    initialize_backup_variable
from datengeist.visual.corr_chart import CorrChart

from datengeist.visual.comparison_chart import comparison_box_charts

def compare_features():
    """
    Displays the 'Relate Features' interface in Streamlit for exploring relationships between features in a DataFrame.
    This includes:
    - Correlation heatmap for numerical features.
    - Box plot comparison for selected categorical and continuous features.
    """
    st.header('Relate Features')

    # Retrieve the sampled DataFrame from session state
    dataframe = get_st_session_df('sampled_df')

    # Only proceed if the dataframe is not empty
    if not dataframe.empty:
        # Initialize session state variables for feature selections and threshold
        set_initial_variable_to_current('select_box_corr_matrix')
        set_initial_variable_to_current('select_box_categorical_feature')
        set_initial_variable_to_current('select_box_continuous_feature')
        set_initial_variable_to_current('slider_columns_division_threshold')

        # Layout: two main columns
        col1, col2 = st.columns(2, gap='large')

        # Render correlation heatmap in the second column
        _render_corr_heatmap(col2, dataframe)

        # Sidebar controls for threshold and feature selection
        continuous_columns, categorical_columns = _render_feature_selection_sidebar(dataframe)

        # Render box plot comparison for selected features
        _render_feature_comparison(col1, dataframe, categorical_columns, continuous_columns)

    else:
        # Show prompt to sample data if the dataframe is empty
        st.page_link('Sample_Dataset.py', label="Sample the data first!")


def _render_corr_heatmap(col, dataframe):
    """
    Renders the correlation heatmap selection in a given column layout.
    """
    # Retrieve the initial value for the correlation type dropdown
    initial_corr_matrix_value = get_state_variable('select_box_corr_matrix', CORR_TYPES)

    # Dropdown to select correlation type
    corr_matrix = col.selectbox(
        "Select The Correlation",
        CORR_TYPES,
        index=initial_corr_matrix_value,
        key='select_box_corr_matrix'
    )

    # Update correlation chart type and display heatmap
    corr_chart = CorrChart(dataframe)
    corr_chart.set_corr_type(corr_matrix)
    col.plotly_chart(corr_chart.get_heatmap())

def _render_feature_selection_sidebar(dataframe):
    """
    Renders the sidebar controls for setting the threshold to differentiate categorical/continuous features.
    Returns lists of continuous and categorical columns.
    """
    # Retrieve the current value of the threshold slider
    slider_columns_division_threshold_value = get_state_variable('slider_columns_division_threshold')

    # Sidebar threshold slider for differentiating between categorical and continuous data
    columns_division_threshold = st.sidebar.number_input(
        'Threshold',
        min_value=0.01,
        max_value=0.99,
        value=slider_columns_division_threshold_value,
        key='slider_columns_division_threshold',
        help='Adjust Threshold to Divide ORDINAL/CATEGORICAL and NUMERICAL/IDENTIFIER Data'
    )

    # Separate columns into continuous and categorical based on the threshold
    continuous_columns = filter_continuous_features(dataframe, columns_division_threshold)
    categorical_columns = filter_categorical_features(dataframe, columns_division_threshold)

    # Initialize backup variables for select boxes
    default_categorical_column = categorical_columns[0] if categorical_columns else None
    default_continuous_column = continuous_columns[0] if continuous_columns else None
    initialize_backup_variable('select_box_categorical_feature', default_categorical_column, categorical_columns)
    initialize_backup_variable('select_box_continuous_feature', default_continuous_column, continuous_columns)

    return continuous_columns, categorical_columns

def _render_feature_comparison(col, dataframe, categorical_columns, continuous_columns):
    """
    Renders the feature comparison box plot for selected categorical and continuous features.
    """
    # Set up columns for select boxes
    col11, col12 = col.columns(2)

    # Select box for categorical feature selection
    initial_categorical_feature_value = get_state_variable('select_box_categorical_feature', categorical_columns)
    categorical_feature = col11.selectbox(
        "Select The Categorical Feature",
        categorical_columns,
        index=initial_categorical_feature_value,
        key='select_box_categorical_feature'
    )

    # Select box for continuous feature selection
    initial_continuous_feature_value = get_state_variable('select_box_continuous_feature', continuous_columns)
    continuous_feature = col12.selectbox(
        "Select The Continuous Feature",
        continuous_columns,
        index=initial_continuous_feature_value,
        key='select_box_continuous_feature'
    )

    # Display box plot comparison if both features are selected
    if categorical_feature and continuous_feature:
        col.plotly_chart(comparison_box_charts(dataframe, categorical_feature, continuous_feature))


if __name__ == '__main__':
    set_layout()
    init_db()

    compare_features()