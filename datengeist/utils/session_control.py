from types import NoneType
import numpy as np
import pandas as pd
import streamlit as st

def initialize_backup_variable(var_name: str, value, possible_values: list = None):
    """
    Initializes a backup variable in Streamlit session state if it's not already present or if its value is not in the specified possible values.

    Parameters:
    - var_name (str): The name of the variable to be initialized.
    - value: The value to set for the variable.
    - possible_values (list, optional): A list of possible valid values. If provided, the variable will only be initialized if its value is not in this list.
    """
    # Initialize the variable in session_state if it’s not there
    if (f'backup_{var_name}' not in st.session_state or
            (not isinstance(possible_values, NoneType)
             and st.session_state[f'backup_{var_name}']
             not in possible_values)):
        st.session_state[f'backup_{var_name}'] = value


def get_state_variable(var_name: str, container=None):
    """
    Retrieves the value of a variable from Streamlit session state or its backup version.

    Parameters:
    - var_name (str): The name of the variable to retrieve.
    - container (optional): A container (like a pandas Index, list, or numpy array) to locate the variable's position or value within.

    Returns:
    - The value of the variable or its position in the container.
    """
    # Check if the variable is in session_state, otherwise use the backup variable
    if var_name not in st.session_state and f'backup_{var_name}' in st.session_state:
        if isinstance(container, pd.Index):
            return container.get_loc(st.session_state[f'backup_{var_name}'])
        if isinstance(container, list) and st.session_state[f'backup_{var_name}'] is not None:
            return container.index(st.session_state[f'backup_{var_name}'])
        if isinstance(container, np.ndarray):
            return st.session_state[f'backup_{var_name}']
        if isinstance(container, NoneType):
            return st.session_state[f'backup_{var_name}']

    elif var_name in st.session_state:
        if container is None:
            return st.session_state[var_name]

        if isinstance(container, pd.Index):
            return container.get_loc(st.session_state[var_name])
        if isinstance(container, list):
            if st.session_state[var_name] not in container and len(container) > 0:
                return 0
            elif st.session_state[var_name] not in container and len(container) == 0:
                return None
            return container.index(st.session_state[var_name])
        if isinstance(container, np.ndarray):
            return st.session_state[var_name]
        if isinstance(container, NoneType):
            return st.session_state[var_name]


def set_initial_variable_to_current(var_name: str):
    """
    Sets the backup variable in session state to match the current value of a variable.

    Parameters:
    - var_name (str): The name of the variable to back up.
    """
    if var_name in st.session_state:
        st.session_state[f'backup_{var_name}'] = st.session_state[var_name]


def get_st_session_df(st_df_name: str) -> pd.DataFrame:
    """
    Retrieves a DataFrame from Streamlit session state, or returns an empty DataFrame if not found.

    Parameters:
    - st_df_name (str): The name of the DataFrame in session state.

    Returns:
    - pd.DataFrame: The DataFrame from session state or an empty DataFrame.
    """
    if st_df_name in st.session_state:
        dataframe = st.session_state[st_df_name]
    else:
        dataframe = pd.DataFrame()

    return dataframe
