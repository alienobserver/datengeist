import sys
import os
import streamlit as st

# Set up project root path for importing modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # 3 levels
sys.path.append(project_root)

# Import custom modules
from datengeist.utils.style import set_page_link_button_style, set_st_padding, set_logo, add_top_margin_div
from datengeist.utils.feature_tools import filter_continuous_features, filter_categorical_features
from datengeist.utils.session_control import get_st_session_df, initialize_backup_variable
from datengeist.utils.helper import get_abs_filename
from datengeist.utils.constants import CORR_TYPES

def set_layout():
    # ---- Application Configuration ----
    # Set wide layout for the Streamlit app and apply custom styling
    st.set_page_config(layout='wide')
    set_st_padding(25)  # Adjust padding for a clean layout
    set_page_link_button_style()  # Style for page link buttons

    # ---- Logo Setup ----
    # Load and display the logo in the sidebar
    logo_path = get_abs_filename('datengeist/assets/logo/logo.png')
    set_logo(logo_path)

def init_uploader():
    # Sidebar file uploader to upload a new CSV dataset
    with st.sidebar:
        if 'uploaded_file' not in st.session_state or st.session_state['uploaded_file'] is None:
            uploaded_file = st.file_uploader("Choose a dataset", type=['csv', 'xlsx'])
            st.session_state['uploaded_file'] = uploaded_file

            if st.session_state['uploaded_file'] is not None:
                st.rerun()

        else:
            cols = st.columns(2)

            with cols[0]:
                st.subheader(st.session_state['uploaded_file'].name)
            with cols[1]:
                delete_file = st.button("Remove")

            if delete_file:
                st.session_state['uploaded_file'] = None
                st.rerun()

    # Reset session data if a new file is uploaded
    if st.session_state['uploaded_file'] is None:
        st.session_state.pop('sampled_df', None)
        st.session_state.pop('raw_csv_file', None)


def init_db():
    # ---- Dataframe Setup ----
    # Load the dataframe from session state if previously stored
    dataframe = get_st_session_df('sampled_df')

    # ---- Data Processing ----
    if not dataframe.empty:
        # Convert categorical (object) columns to string type
        categorical_features = dataframe.select_dtypes(include=['object'])
        for col in categorical_features:
            dataframe[col] = dataframe[col].astype(str)

        # Identify continuous and categorical columns based on a 10% threshold
        continuous_columns = filter_continuous_features(dataframe, threshold=0.1)
        categorical_columns = filter_categorical_features(dataframe, threshold=0.1)
        nominal_features = dataframe.select_dtypes(include=['object'])

        # Initialize backup variables in session state for UI element states
        initialize_backup_variable('select_box_feature_info', dataframe.columns[0], dataframe.columns)
        initialize_backup_variable('select_box_categorical_feature', None, categorical_columns)
        initialize_backup_variable('select_box_continuous_feature', None, continuous_columns)
        initialize_backup_variable('select_box_corr_matrix', CORR_TYPES[0], CORR_TYPES)
        initialize_backup_variable('slider_columns_division_threshold', 0.01)

        # Initialize backup variables for handling missing data in nominal features
        for col in nominal_features:
            initialize_backup_variable(f'text_input_missing_{col}', 'nan')