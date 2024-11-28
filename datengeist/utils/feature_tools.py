import pandas as pd

def filter_categorical_features(dataframe: pd.DataFrame, threshold: float = 0.02) -> list:
    """
    Filters the categorical features in a DataFrame based on the threshold for the ratio of unique values to total values.

    Parameters:
    - dataframe (pd.DataFrame): The input DataFrame.
    - threshold (float): The threshold ratio for identifying categorical features. Default is 0.02.

    Returns:
    - list: A list of column names that are considered categorical features.
    """
    categorical_features = []

    if not dataframe.empty:
        for name, column in dataframe.items():
            unique_count = column.unique().shape[0]
            total_count = column.shape[0]

            if unique_count / total_count < threshold:
                categorical_features.append(name)

    return categorical_features


def filter_continuous_features(dataframe: pd.DataFrame, threshold: float = 0.02) -> list:
    """
    Filters the continuous (numerical) features in a DataFrame based on the threshold for the ratio of unique values to total values.

    Parameters:
    - dataframe (pd.DataFrame): The input DataFrame.
    - threshold (float): The threshold ratio for identifying continuous features. Default is 0.02.

    Returns:
    - list: A list of column names that are considered continuous features.
    """
    continuous_features = []
    quantitative_columns = dataframe.select_dtypes(include=['int', 'float']).dropna()

    if not quantitative_columns.empty:
        for name, column in quantitative_columns.items():
            unique_count = column.unique().shape[0]
            total_count = column.shape[0]

            if unique_count / total_count > threshold:
                continuous_features.append(name)

    return continuous_features


def filter_str_categorical_features(dataframe: pd.DataFrame, threshold: float = 0.2) -> list:
    """
    Filters string-type categorical features in a DataFrame based on the threshold for the ratio of unique values to total values.

    Parameters:
    - dataframe (pd.DataFrame): The input DataFrame.
    - threshold (float): The threshold ratio for identifying categorical features. Default is 0.2.

    Returns:
    - list: A list of column names that are considered string-type categorical features.
    """
    df_with_string_features = dataframe.select_dtypes(include=['object'])
    categorical_features = []

    if not df_with_string_features.empty:
        for name, column in df_with_string_features.items():
            unique_count = column.unique().shape[0]
            total_count = column.shape[0]

            if unique_count / total_count < threshold:
                categorical_features.append(name)

    return categorical_features


def filter_num_categorical_features(dataframe: pd.DataFrame, threshold: float = 0.2) -> list:
    """
    Filters numerical columns that behave as categorical features (low number of unique values relative to total values).

    Parameters:
    - dataframe (pd.DataFrame): The input DataFrame.
    - threshold (float): The threshold ratio for identifying numerical categorical features. Default is 0.2.

    Returns:
    - list: A list of column names that are considered numerical categorical features.
    """
    df_with_numerical_features = dataframe.select_dtypes(include=['int', 'float'])
    categorical_features = []

    if not df_with_numerical_features.empty:
        for name, column in df_with_numerical_features.items():
            unique_count = column.unique().shape[0]
            total_count = column.shape[0]

            if unique_count / total_count < threshold:
                categorical_features.append(name)

    return categorical_features


def is_categorical(feature: pd.Series, threshold: float = 0.2) -> bool:
    """
    Determines if a feature (column) in a DataFrame is categorical based on the ratio of unique values to total values.

    Parameters:
    - feature (pd.Series): The input feature (column) to be evaluated.
    - threshold (float): The threshold ratio for determining if the feature is categorical. Default is 0.2.

    Returns:
    - bool: True if the feature is categorical, False otherwise.
    """
    if not feature.empty:
        unique_count = feature.unique().shape[0]
        total_count = feature.shape[0]

        if unique_count / total_count < threshold:
            return True
        else:
            return False


def count_missing_values_column(dataframe: pd.DataFrame, column: str, missing_data_keywords: list = []) -> int:
    """
    Counts the missing values in a DataFrame column, optionally considering specific missing data keywords.

    Parameters:
    - dataframe (pd.DataFrame): The input DataFrame.
    - column (str): The name of the column to count missing values in.
    - missing_data_keywords (list): A list of keywords representing missing data values (e.g., 'nan', 'N/A'). Default is an empty list.

    Returns:
    - int: The count of missing values in the column.
    """
    missing_data_count = 0

    if len(missing_data_keywords) > 0:
        # Count occurrences of each keyword
        for keyword in missing_data_keywords:
            missing_data_count += dataframe[column].str.contains(rf'\b{keyword}\b', case=True).sum()
    else:
        missing_data_count = dataframe[column].isna().sum()

    return missing_data_count
