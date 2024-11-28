import os
from io import StringIO

import streamlit as st


def get_abs_filename(relative_path: str) -> str:
    """
    Returns the absolute file path based on the relative path.

    Parameters:
    - relative_path (str): The relative file path to be resolved.

    Returns:
    - str: The absolute file path.
    """
    dir_name = os.path.dirname(__file__)
    src_dir_name = os.path.dirname(dir_name)
    root_dir_name = os.path.dirname(src_dir_name)
    filename = os.path.join(root_dir_name, relative_path)

    return filename

def truncate_str(word: str, max_str_len: int = 15) -> str:
    """
    Truncates a string if it exceeds the maximum length, adding ellipsis.

    Parameters:
    - word (str): The string to be truncated.
    - max_str_len (int): The maximum length of the string. Default is 15.

    Returns:
    - str: The truncated string with ellipsis if necessary.
    """

    return word[:max_str_len] + '...' if len(word) > max_str_len else word

def get_str_from_bytes_file(uploaded_file) -> str:
    """
    Converts a Streamlit uploaded file to a string.

    Parameters:
    - uploaded_file: The file object uploaded by the user.

    Returns:
    - str: The contents of the file as a string.
    """
    # Convert file content to string format
    stringio = StringIO(uploaded_file.getvalue().decode("latin-1"))
    string_data = stringio.read()

    return string_data

def get_n_rows_features_csv(uploaded_file) -> tuple:
    """
    Extracts the number of rows and features from a CSV file uploaded through Streamlit.

    Parameters:
    - uploaded_file: The file object uploaded by the user (assumed to be CSV).

    Returns:
    - tuple: A tuple containing the number of rows and features in the CSV file.
    """
    # Store the raw CSV file content in session state if not already done
    if 'raw_csv_file' not in st.session_state:
        st.session_state['raw_csv_file'] = get_str_from_bytes_file(uploaded_file)

    # Split the raw CSV data into lines and calculate the number of rows and features
    raw_csv_file_split = st.session_state['raw_csv_file'].split('\n')
    n_file_lines = len(raw_csv_file_split)
    n_rows = n_file_lines - 1  # Subtract 1 for the header
    n_features = len(raw_csv_file_split[0].split(','))  # Count columns in the first line

    return n_rows, n_features
