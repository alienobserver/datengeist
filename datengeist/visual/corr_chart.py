import numpy as np
import plotly.graph_objects as go

from datengeist.utils.calc import cramers_matrix, point_biserial_matrix
from datengeist.utils.helper import truncate_str


class CorrChart:
    def __init__(self, dataframe, max_str_len=15):
        """
        Initializes the CorrChart object with a dataframe and an optional max string length for column names.

        Parameters:
        - dataframe (pd.DataFrame): The DataFrame containing the data for correlation analysis.
        - max_str_len (int): Maximum length of the column names to display in the heatmap (default is 15).
        """
        self.max_str_len = max_str_len
        self.colorscale = [
            [0.0, '#29AA81'],  # Start of the scale (0) with blue
            [0.5, '#000A19'],  # Middle of the scale (0.5) with black
            [1.0, '#BE0019']  # End of the scale (1) with red
        ]
        self.dataframe = dataframe
        self.stripped_columns = np.array(
            list(map(lambda x: truncate_str(x, max_str_len), self.dataframe.columns.values))
        )
        self.corr_matrix = None
        self.corr_types = ['pearson', 'cramer', 'spearman', 'kendall', 'point biserial']
        self.corr_type = 'pearson'

        self.set_corr_type(self.corr_type)

    def _set_corr_matrix(self):
        """
        Computes the correlation matrix based on the selected correlation type.

        This method calculates different correlation matrices based on the `corr_type` attribute
        (e.g., Pearson, Spearman, Cramér's v, etc.)
        It also updates the column names in `stripped_columns` after truncating the strings based on the
        `max_str_len` parameter.
        """
        match self.corr_type:
            case 'pearson':
                numerical_features = self.dataframe.select_dtypes(include=['int', 'float'])
                numerical_features_no_nan = numerical_features.dropna()
                self.corr_matrix = numerical_features_no_nan.corr()
                self.stripped_columns = np.array(
                    list(map(lambda x: truncate_str(x, self.max_str_len), numerical_features.columns.values))
                )
            case 'kendall':
                numerical_features = self.dataframe.select_dtypes(include=['int', 'float'])
                numerical_features_no_nan = numerical_features.dropna()
                self.corr_matrix = numerical_features_no_nan.corr(method='kendall')
                self.stripped_columns = np.array(
                    list(map(lambda x: truncate_str(x, self.max_str_len), numerical_features.columns.values))
                )
            case 'spearman':
                numerical_features = self.dataframe.select_dtypes(include=['int', 'float'])
                numerical_features_no_nan = numerical_features.dropna()
                self.corr_matrix = numerical_features_no_nan.corr(method='spearman')
                self.stripped_columns = np.array(
                    list(map(lambda x: truncate_str(x, self.max_str_len), numerical_features.columns.values))
                )
            case 'point biserial':
                numerical_features = self.dataframe.select_dtypes(include=['int', 'float'])
                numerical_features_no_nan = numerical_features.dropna()
                self.corr_matrix = point_biserial_matrix(numerical_features_no_nan)
                self.stripped_columns = np.array(
                    list(map(lambda x: truncate_str(x, self.max_str_len), numerical_features.columns.values))
                )
            case 'cramer':
                # Select the categorical features and drop NaN's
                numerical_features = self.dataframe.select_dtypes(include=['object'])
                numerical_features_no_nan = numerical_features.fillna('missing')
                cramers_df = cramers_matrix(numerical_features_no_nan)
                self.corr_matrix = cramers_df.corr()
                self.stripped_columns = np.array(
                    list(map(lambda x: truncate_str(x, self.max_str_len), numerical_features.columns.values))
                )

    def _get_heatmap_title(self):
        """
        Returns the appropriate title for the heatmap based on the selected correlation type.

        Returns:
        - str: The title of the heatmap.
        """
        match self.corr_type:
            case 'pearson':
                return 'Pearson Correlation Matrix'
            case 'cramer':
                return 'Cramér\'s V Correlation Matrix for Categorical Features'
            case 'kendall':
                return 'Kendall Correlation Matrix'
            case 'spearman':
                return 'Spearman Correlation Matrix'
            case 'point biserial':
                return 'Point-Biserial Correlation Matrix'

    def _get_heatmap_trace(self):
        """
        Creates a heatmap trace for Plotly using the correlation matrix and column names.

        Returns:
        - go.Heatmap: The heatmap trace object for plotting.
        """
        heatmap_trace = go.Heatmap(
            x=self.stripped_columns,
            y=self.stripped_columns,
            z=self.corr_matrix,
            zmin=-1,  # Sets the lower bound of the color domain
            zmax=1,
            xgap=1,  # Sets the horizontal gap (in pixels) between bricks
            ygap=1,
            colorscale=self.colorscale
        )

        return heatmap_trace

    def set_corr_type(self, corr_type):
        """
        Sets the correlation type and recalculates the correlation matrix.

        Parameters:
        - corr_type (str): The correlation type to use. Must be one of defined in self.corr_types

        Raises:
        - ValueError: If the provided correlation type is not valid.
        """
        if corr_type not in self.corr_types:
            raise ValueError(f"{corr_type} is not a possible correlation matrix type")

        self.corr_type = corr_type
        self._set_corr_matrix()

    def get_heatmap(self):
        """
        Generates a heatmap figure using Plotly for the current correlation matrix.

        Returns:
        - go.Figure: The Plotly figure containing the heatmap.
        """
        heatmap_trace = self._get_heatmap_trace()
        title = self._get_heatmap_title()

        layout = go.Layout(
            title=dict(
                text=title,
                y=0.95,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=24)
            ),
            width=600,
            height=600,
            xaxis=dict(
                showgrid=False,
            ),
            yaxis=dict(
                showgrid=False,
                autorange='reversed',
            ),
        )

        fig = go.Figure(data=[heatmap_trace], layout=layout)

        return fig
