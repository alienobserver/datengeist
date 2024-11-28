import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, pointbiserialr
import streamlit as st

def cramers_v(x: pd.Series, y: pd.Series) -> float:
    """
    Calculate Cramér's V statistic for measuring association between two categorical variables.

    Parameters:
    - x (pd.Series): The first categorical variable.
    - y (pd.Series): The second categorical variable.

    Returns:
    - float: Cramér's V statistic, a value between 0 (no association) and 1 (perfect association).
    """
    # Create a contingency table
    contingency_table = pd.crosstab(x, y)
    chi2_statistic, p_value, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()
    phi2 = chi2_statistic / n
    r, k = contingency_table.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    k_corr = k - (k - 1)**2 / n
    r_corr = r - (r - 1)**2 / n
    v = np.sqrt(phi2corr / min(k_corr - 1, r_corr - 1))

    return v

@st.cache_data(persist='disk')
def cramers_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a matrix of Cramér's V statistics for all pairs of categorical variables in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing categorical variables.

    Returns:
    - pd.DataFrame: A DataFrame where each entry (i, j) is the Cramér's V statistic for the variables `df[i]` and `df[j]`.
    """
    # Filter categorical columns only
    categorical_vars = df.select_dtypes(include=['object', 'category']).columns

    # Initialize a DataFrame to store the results
    cramers_v_matrix = pd.DataFrame(index=categorical_vars, columns=categorical_vars, dtype=float)

    # Calculate Cramér's V for each pair of variables
    for var1 in categorical_vars:
        for var2 in categorical_vars:
            cramers_v_matrix.loc[var1, var2] = cramers_v(df[var1], df[var2])

    return cramers_v_matrix

@st.cache_data(persist='disk')
def point_biserial_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a matrix of point-biserial correlation coefficients for numerical variables in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing numerical variables.

    Returns:
    - pd.DataFrame: A DataFrame where each entry (i, j) is the point-biserial correlation for `df[i]` and `df[j]`.
    """
    # Filter numerical columns only
    numerical_vars = df.select_dtypes(include=[np.number]).columns

    # Initialize a DataFrame to store the results
    pb_matrix = pd.DataFrame(index=numerical_vars, columns=numerical_vars, dtype=float)

    # Calculate point-biserial correlation for each pair of variables
    for var1 in numerical_vars:
        for var2 in numerical_vars:
            if var1 != var2:  # Skip self-correlation for clarity
                corr, _ = pointbiserialr(df[var1], df[var2])
                pb_matrix.loc[var1, var2] = corr
            else:
                pb_matrix.loc[var1, var2] = 1.0  # Perfect correlation with itself

    return pb_matrix
