import pandas as pd
import plotly.express as px
import numpy as np
import itertools
import umap
import math
import plotly.graph_objects as go
import scipy.stats as stats

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
from statistics import mean
from sklearn.mixture import GaussianMixture

emb_space_colours = ["#56638A", "#BAD9B5", "#D77A61", "#D77A61", "#40531B"]
distance_metric_aliases = {
    "euclidean": "Euclidean",
    "cityblock": "Manhattan",
    "cosine": "Cosine",
    "sqeuclidean": "Standardised Euclidean",
    "sqeuclidean_normalised": "Normalised Standardised Euclidean",
    "euclidean_normalised": "Normalised Euclidean",
    "cityblock_normalised": "Normalised Manhattan",
    "adjusted_cosine": "Adjusted Cosine",
    "mahalanobis": "Mahalanobis",
}


class EmbeddingHandler:
    def __init__(self, sample_meta_data: pd.DataFrame):
        """Initialise EmbeddingHandler object.

        Parameters:
        sample_meta_data (pd.DataFrame): Meta data for samples. \
            Should have sample identifiers in the first column. \
            Should have a header row.

        Object attributes:
        meta_data (pd.DataFrame): Meta data for samples.
        meta_data_first_column (str): Name of the first column in meta_data.
        meta_data_numeric_columns (list): List of column names of columns \
            in meta_data with numerical data.
        meta_data_categorical_columns (list): List of column names of columns \
            in meta_data with categorical data.
        sample_names (list): List of sample names as defined in the first \
            column of the metadata. The order is determined by the order \
            of the samples in the metadata.
        colour_map (dict): Dictionary with colour codes for categorical \
            features in meta_data.
        emb (dict): Dictionary for embedding spaces which can be added later.
        pw_meta_data (dict): Dictionary for pairwise meta data which can \
            be added later.
        """
        self.meta_data = sample_meta_data
        self.meta_data_first_column = self.meta_data.columns[0]
        self.meta_data_numeric_columns = self.__identify_numerical_columns__()
        self.meta_data_categorical_columns = [
            col
            for col in self.meta_data.columns[1:]
            if col not in self.meta_data_numeric_columns
        ]
        self.sample_names = self.meta_data.iloc[:, 0].tolist()
        self.colour_map = self.__get_colour_map_for_features__()
        self.emb = dict()
        self.pw_meta_data = dict()
        print(f"{len(self.sample_names)} samples loaded.")
        print(f"Categories in meta data: {self.meta_data_categorical_columns}")
        print(
            f"Numerical columns in meta data: {self.meta_data_numeric_columns}"
        )
        return

    def __identify_numerical_columns__(self) -> list:
        """Identify numerical columns in meta_data.

        Returns:
        list: List of the column names of all numerical columns in meta_data.
        """
        # find columnns in meta data which are numerical
        numerical_columns = (
            self.meta_data.iloc[:, 1:]
            .select_dtypes(include=["int64", "float64"])
            .columns.tolist()
        )
        return numerical_columns

    def __get_colour_map_for_features__(self) -> dict:
        """Generate colour map for categorical features in the meta_data. \
        The colour map is used for visualisation. \
        The colour map is generated based on the number of unique values \
        in the columns of the meta_data. \
        Only defined for columns with less than 15 unique values.

        Returns:
        dict: Dictionary with colour codes for categorical features in \
            the meta_data.
        """
        if len(self.meta_data.columns) == 1:
            print("No meta data provided. Cannot generate colour map.")
            return None
        colour_map = dict()
        for column in self.meta_data[
            self.meta_data_categorical_columns
        ].columns:
            column_values = self.meta_data[column].unique()
            if len(column_values) > 15:
                print(
                    f"Column {column} has more than 15 unique values. \
                        Skipping."
                )
                continue
            colour_map[column] = dict()

            colours = px.colors.qualitative.Set2 + px.colors.qualitative.Set3

            # Check if the colours list is empty
            if not colours:
                raise ValueError("The colours list is empty.")

            for i, value in enumerate(column_values):

                # Check if the index i is within the range of the colours list
                if i >= len(colours):
                    raise IndexError(
                        f"The index i is out of range for {column_values}"
                    )
                if (str(value) == "True") or (str(value) == "Disordered"):
                    colour_map[column][str(value)] = "steelblue"
                elif (str(value) == "False") or (
                    str(value) == "Non-disordered"
                ):
                    colour_map[column][str(value)] = "darkred"
                else:
                    colour_map[column][value] = colours[i]
        return colour_map

    def __check_for_emb_space__(self, emb_space_name: str) -> None:
        """Check if emb_space_name is present in emb.

        Parameters:
        emb_space_name (str): Name of the embedding space.

        Raises:
        ValueError: If emb_space_name is not present in emb.
        """
        if emb_space_name not in self.emb.keys():
            raise ValueError(f"Embedding space {emb_space_name} not found.")
        else:
            return True

    def __check_col_in_meta_data__(self, col) -> None:
        """Check if a column name is present in meta_data.

        Parameters:
        col (str): Column name.

        Raises:
        ValueError: If col is not present in meta_data.
        """
        if col not in self.meta_data.columns:
            raise ValueError(f"Column {col} not found in meta data.")

    def __check_col_categorical__(self, col) -> None:
        """Check if col is a categorical column in meta_data.

        Parameters:
        col (str): Column name.

        Raises:
        ValueError: If col is not categorical in meta_data.
        """
        if col not in self.meta_data_categorical_columns:
            raise ValueError(f"Column {col} is not categorical in meta data.")
            return False
        return True

    def __check_col_numeric__(self, col) -> None:
        """Check if col is numerical in meta_data.

        Parameters:
        col (str): Column name.

        Raises:
        ValueError: If col is not numerical in meta_data.
        """
        if col not in self.meta_data_numeric_columns:
            raise ValueError(f"Column {col} is not numerical in meta data.")
            return False
        return True

    def __sample_indices_to_groups__(self, group: str) -> dict:
        """Find sample indices for each group in a column of meta_data.

        Parameters:
        group (str): Column name in meta_data to group by.

        Returns:
        dict: Dictionary with group names as keys and sample indices as values.
        """
        self.__check_col_categorical__(group)
        group_indices = dict()
        # convert all values in the meta data to strings
        self.meta_data[group] = self.meta_data[group].astype(str)
        for group_name in self.meta_data[group].unique():
            group_indices[group_name] = self.meta_data[
                self.meta_data[group] == group_name
            ].index.tolist()
        return group_indices

    def __calculate_clusters__(
        self, emb_space_name: str, n_clusters: int = None
    ) -> None:
        """Calculate clusters using KMeans clustering algorithm.
        If n_clusters is not provided, the number of clusters is calculated
        based on the number of unique values in the meta_data columns.
        The number of clusters is the average of the number of unique values
        in the columns of the meta_data, excluding the first column.
        If only one column is present, the number of clusters is set to 5.
        If the number of clusters is less than 2, it is set to 3.
        If the number of clusters is more than 15, it is set to 15.
        The cluster labels are added to the meta_data in a new column.
        The new column is named "cluster_" + emb_space_name.
        
        Parameters:
        emb_space_name (str): Name of the embedding space.
        n_clusters (int): Number of clusters. If not provided, the number of \
            clusters is calculated based on the number of unique values in \
                the meta_data columns.
        
        Raises:
        ValueError: If emb_space_name is not present in emb.
        """
        self.__check_for_emb_space__(emb_space_name)

        if n_clusters is None:
            if len(self.meta_data.columns) > 1:
                n_clusters = math.floor(
                    mean(
                        self.meta_data[
                            self.meta_data_categorical_columns
                        ].nunique()
                    )
                )
                if n_clusters < 2:
                    n_clusters = 3
                if n_clusters > 15:
                    n_clusters = 15
            else:
                n_clusters = 5
        km = KMeans(n_clusters=n_clusters, n_init="auto", random_state=8)
        km.fit(self.emb[emb_space_name]["emb"])
        km.predict(self.emb[emb_space_name]["emb"])

        # add cluster labels to meta_data
        self.meta_data["cluster_" + emb_space_name] = km.labels_.astype(str)
        self.meta_data_categorical_columns.append("cluster_" + emb_space_name)
        self.colour_map = self.__get_colour_map_for_features__()
        print(f"{n_clusters} clusters calculated for {emb_space_name}.")
        return

    def __calculate_pwd__(self, emb_space_name: str, metric: str) -> np.array:
        """Calculate pairwise distance matrix for an embedding space.

        Args:
            emb_space_name (str): Name of the embedding space.
            metric (str): Distance metric. Can be one of the following:
                - "sqeuclidean_normalised"
                - "euclidean_normalised"
                - "cityblock_normalised"
                - "adjusted_cosine"
                - "euclidean"
                - "cityblock"
                - "cosine"
                - "sqeuclidean"
                - "mahalanobis"

        Returns:
            np.array: _description_
        """

        if metric == "sqeuclidean_normalised":
            # divide each row by its norm
            emb = self.emb[emb_space_name]["emb"]
            emb_norm = np.linalg.norm(emb, axis=1)
            emb = emb / emb_norm[:, None]  # divide each row by its norm
            emb_pwd = squareform(pdist(emb, metric="sqeuclidean"))
            return emb_pwd

        elif metric == "euclidean_normalised":

            # divide each row of the emb by its norm
            emb = self.emb[emb_space_name]["emb"]
            emb_norm = np.linalg.norm(emb, axis=1)
            emb = emb / emb_norm[:, None]  # divide each row by its norm
            emb_pwd = squareform(pdist(emb, metric="euclidean"))
            return emb_pwd

        elif metric == "cityblock_normalised":
            emb_pwd = squareform(
                pdist(self.emb[emb_space_name]["emb"], metric="cityblock")
            )
            emb_pwd = emb_pwd / len(self.emb[emb_space_name]["emb"][1])
            return emb_pwd

        elif metric == "adjusted_cosine":
            # substract the mean of each column from each value
            emb = self.emb[emb_space_name]["emb"]
            emb = emb - np.median(emb, axis=0)  # emb.median(axis=0)
            emb_pwd = squareform(pdist(emb, metric="cosine"))
            return emb_pwd

        emb_pwd = squareform(
            pdist(self.emb[emb_space_name]["emb"], metric=metric)
        )
        return emb_pwd

    def add_emb_space(self, embeddings: np.array, emb_space_name: str) -> None:
        """Add embedding space to emb object.

        Parameters:
        embeddings (np.array): Embedding space. Embeddings need to be \
            in the shape (n_samples, n_features). The order of samples should \
            match the order of samples in the meta_data.
        emb_space_name (str): Name of the embedding space. Can be any string. \
            Should be unique. If the name already exists, an error is raised.
        """
        if emb_space_name in self.emb.keys():
            raise ValueError(
                f"Embedding space {emb_space_name} already exists."
            )
        if embeddings.shape[0] != len(self.sample_names):
            raise ValueError(
                f"Number of samples in embeddings ({embeddings.shape[0]}) \
                    does not match the number of samples in meta_data \
                    ({len(self.sample_names)})"
            )
        self.emb[emb_space_name] = dict()
        self.emb[emb_space_name]["emb"] = embeddings
        self.__calculate_clusters__(emb_space_name, n_clusters=None)
        # add a default colour for the new embedding space
        if len(self.emb.keys()) > len(emb_space_colours):
            self.emb[emb_space_name]["colour"] = px.colors.qualitative.Set3[
                len(self.emb.keys()) - len(emb_space_colours)
            ]
        else:
            self.emb[emb_space_name]["colour"] = emb_space_colours[
                len(self.emb.keys()) - 1
            ]
        print(f"Embedding space {emb_space_name} added.")
        print(f"Embeddings have length {embeddings.shape[1]}.")
        return

    def remove_emb_space(self, emb_space_name: str) -> None:
        """Remove embedding space from emb.

        Parameters:
        emb_space_name (str): Name of the embedding space to be removed.
        Will raise an error if the embedding space does not exist.
        """
        self.__check_for_emb_space__(emb_space_name)
        del self.emb[emb_space_name]
        return

    def add_pw_metadata(
        self, pw_metadata: pd.DataFrame, pw_metadata_name: str
    ) -> None:
        """Add pairwise metadata to emb.

        Parameters:
        pw_metadata (pd.DataFrame): Pairwise metadata. The dataframe should \
            have the same number of rows and columns as the number of samples.
        """
        if pw_metadata_name in self.pw_meta_data.keys():
            raise ValueError(
                f"Pairwise metadata {pw_metadata_name} already exists."
            )
            return

        if pw_metadata_name in self.meta_data.columns:
            raise ValueError(
                f"Pairwise metadata name {pw_metadata_name} already exists."
            )

        # check that all column names are the same as the sample names
        # regardless of the order
        if not set(pw_metadata.columns.tolist()) == set(self.sample_names):
            raise ValueError(
                "Column names of pw_metadata do not match the sample names."
            )

        # check that all indices are the same as the sample names
        # regardless of the order
        if not set(pw_metadata.index.tolist()) == set(self.sample_names):
            raise ValueError(
                "Indices of pw_metadata do not match the sample names."
            )
        # reorder the pairwise metadata to match the order of the samples
        pwd_metadata = pw_metadata.reindex(
            index=self.sample_names, columns=self.sample_names
        )

        self.pw_meta_data[pw_metadata_name] = np.array(pwd_metadata)
        return

    def remove_pw_metadata(self, pw_metadata_name: str) -> None:
        """Remove pairwise metadata from emb object. Will raise an error if \
            the pairwise metadata does not exist.

        Parameters:
        pw_metadata_name (str): Name of the pairwise metadata to be removed.
        """
        if pw_metadata_name in self.pw_meta_data.keys():
            del self.pw_meta_data[pw_metadata_name]
        else:
            raise ValueError(
                f"Pairwise metadata {pw_metadata_name} not found."
            )
        return

    def recalculate_clusters(
        self, emb_space_name: str, n_clusters: int = None
    ) -> None:
        """Recalculate unsupervised clusters for an embedding space.

        Parameters:
        emb_space_name (str): Name of the embedding space.
        n_clusters (int): Number of clusters. If not provided, the number of \
            clusters is calculated based on the number of unique values in \
            the meta_data columns.
        """
        self.__check_for_emb_space__(emb_space_name)
        self.__calculate_clusters__(emb_space_name, n_clusters)
        return

    def get_sample_names(self) -> list:
        """Return list of sample names.

        Returns:
            list: List of sample names.
        """
        return self.sample_names

    def get_samples_per_group_value(
        self, group: str, group_value: str
    ) -> pd.DataFrame:
        """Return sample names for a group value.

        Parameters:
        group (str): Column name in meta_data.
        group_value (str): Value in the column.

        Returns:
            list: List of sample names for the group value.
        """
        self.__check_col_categorical__(group)
        if group_value not in self.meta_data[group].unique():
            raise ValueError(f"{group_value} not found in {group}.")
        group_samples = self.meta_data[self.meta_data[group] == group_value]
        return group_samples

    def get_emb(self, emb_space_name: str) -> np.array:
        """Return embedding space.

        Parameters:
        emb_space_name (str): Name of the embedding space.

        Returns:
        np.array: Embedding space.
        """
        self.__check_for_emb_space__(emb_space_name)
        return self.emb[emb_space_name]["emb"]

    def get_groups(self) -> list:
        """Return list of columns in meta_data.

        Returns:
            list: List of columns in meta_data.
        """
        return self.meta_data[
            self.meta_data_categorical_columns
        ].columns.tolist()

    def get_col_continuous(self) -> list:
        """Return list of columns in meta_data.

        Returns:
            list: List of columns in meta_data.
        """
        return self.meta_data[self.meta_data_numeric_columns].columns.tolist()

    def get_unique_values_per_group(self, group: str) -> list:
        """Return unique values in a column of meta_data.

        Args:
            group (str): Column name in meta_data.

        Returns:
            list: Unique values in the column ordered alphabetically.
        """
        self.__check_col_categorical__(group)
        group_values = self.meta_data[group].unique().tolist()
        group_values = sorted(group_values)
        return group_values

    def get_value_count_per_group(self, group: str) -> pd.DataFrame:
        """Return unique values in a column of meta_data and their counts.

        Args:
            group (str): Column name in meta_data.

        Returns:
            pd.DataFrame: Unique values in the column and their counts.
        """
        self.__check_col_categorical__(group)
        group_values = self.meta_data[group].value_counts().reset_index()
        group_values.columns = [group, "count"]
        return group_values

    def get_distance_percentiles(
        self, emb_space_name: str, distance_metric: str, rank: str
    ) -> np.array:
        """Return percentiles of pairwise distance matrix.

        Args:
            emb_space_name (str): Name of the embedding space.
            distance_metric (str): Name of the distance metric.
            rank (str): Name of the rank method. Either "order", "normal_dis" \
                or "bimodal_dis".

        Returns:
            np.array: Array with the percentiles of the pairwise \
                distance matrix.
        """
        self.__check_for_emb_space__(emb_space_name)
        emb_pwd = self.get_sample_distance(emb_space_name, distance_metric)
        if rank == "order":
            percentiles = global_rank(emb_pwd)
        elif rank == "normal_dis":
            percentiles = global_percentiles_normal_distribution(emb_pwd)
        elif rank == "bimodal_dis":
            percentiles = global_percentiles_gaussian_mixture(emb_pwd)
        return percentiles

    def get_sample_distance(
        self, emb_space_name: str, metric: str, rank: str = None
    ) -> np.array:
        """Calculate pairwise distance between samples in the embedding space.\
            Columns and rows are ordered by the order of samples in the \
            meta_data. Each element in the matrix is the distance between the \
            corresponding samples in the embedding space.

        Parameters:
        emb_space_name (str): Name of the embedding space.
        metric (str): Distance metric. Can be one of the following:
            - "euclidean"
            - "cityblock"
            - "cosine"
            - "sequclidean"
            - "euclidean_normalised"
            - "cityblock_normalised"
            - "sequclidean_normalised"
            - "adjusted_cosine"
            - "mahalanobis"
        rank (str, optional): Either "order", "normal_dis" or "bimodal_dis". \
            If rank is not None, the distance matrix is converted to \
            percentiles before returning. Default is None.

        Returns:
        np.array: Pairwise distance matrix.
        """
        self.__check_for_emb_space__(emb_space_name)
        # check if distance matrix is already calculated

        if "distance" not in self.emb[emb_space_name].keys():
            self.emb[emb_space_name]["distance"] = dict()
        if metric in self.emb[emb_space_name]["distance"].keys():
            pwd = self.emb[emb_space_name]["distance"][metric]
        else:
            pwd = self.__calculate_pwd__(emb_space_name, metric)
            self.emb[emb_space_name]["distance"][metric] = pwd
        if rank:
            pwd = self.get_distance_percentiles(emb_space_name, metric, rank)
        return pwd

    def get_sample_distance_difference(
        self,
        emb_space_name_1: str,
        emb_space_name_2: str,
        distance_metric: str,
        rank: str = None,
    ) -> np.array:
        """Calculate the difference between two pairwise distance matrices. \
        The difference is calculated as pwd_1 - pwd_2. \
        If rank is not None, the distance matrices are converted to \
        percentiles before calculating the difference.

        Args:
            emb_space_name_1 (str): Name of the first embedding space.
            emb_space_name_2 (str): Name of the second embedding space.
            distance_metric (str): Name of the distance metric.
            rank (str, optional): Name of the rank method. Either "order", \
                "normal_dis" or "bimodal_dis". Default is None.

        Returns:
            np.array: Pairwise distance matrix difference. \
                Each element is the difference between the corresponding \
                elements in the two distance matrices. \
                If rank is not None the difference is in percentiles.
        """
        for emb_space_name in [emb_space_name_1, emb_space_name_2]:
            self.__check_for_emb_space__(emb_space_name)

        pwd_1 = self.get_sample_distance(
            emb_space_name_1,
            distance_metric,
            rank,
        )
        pwd_2 = self.get_sample_distance(
            emb_space_name_2, distance_metric, rank
        )

        delta_emb_pwd = pwd_1 - pwd_2

        return delta_emb_pwd

    def visualise_emb_pca(
        self, emb_space_name: str, colour: str = None
    ) -> go.Figure:
        """Visualise embedding space using PCA. The first two principal \
        components are used for the plot. The variance explained by the \
        first two components is displayed on the axes. The data points are \
        coloured based on the categorical column in the meta_data. If no \
        colour column is provided, the data points are coloured based on \
        the unsupervised clusters calculated using KMeans.

        Args:
            emb_space_name (str): Name of the embedding space.
            colour (str, optional): Categorical column in the meta_data to \
                colour the data points. Default is None and will colour the \
                data points based on their unsupervised clusters.

        Returns:
            go.Figure: PCA plot.
        """
        self.__check_for_emb_space__(emb_space_name)
        if not colour:
            colour = "cluster_" + emb_space_name
            # self.__calculate_clusters__(emb_space_name, n_clusters=None)
            # colour = "cluster_" + emb_space_name

        self.__check_col_categorical__(colour)

        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(self.emb[emb_space_name]["emb"])

        # get variance explained by the first two components
        variance_explained = pca.explained_variance_ratio_

        fig = get_scatter_plot(
            emb_object=self,
            emb_space_name=emb_space_name,
            colour=colour,
            X_2d=X_2d,
            method="PCA",
        )

        # add variance explained to axes
        fig.update_layout(
            xaxis_title="PC1 ({}%)".format(
                round(variance_explained[0] * 100, 2)
            ),
            yaxis_title="PC2 ({}%)".format(
                round(variance_explained[1] * 100, 2)
            ),
        )
        return fig

    def visualise_emb_umap(
        self, emb_space_name: str, colour: str = None
    ) -> go.Figure:
        """Visualise embedding space using UMAP. The data points \
            are coloured based on the categorical column in the meta_data. \
            If no colour column is provided, the data points are coloured \
            based on their unsupervised clusters.

        Args:
            emb_space_name (str): Name of the embedding space.
            colour (str, optional): Categorical column in the meta_data to \
                colour the data points. Default is None and will colour the \
                data points based on their unsupervised clusters.

        Returns:
            go.Figure: UMAP plot.
        """
        self.__check_for_emb_space__(emb_space_name)
        if not colour:
            colour = "cluster_" + emb_space_name
            # self.__calculate_clusters__(emb_space_name, n_clusters=None)
            # colour = "cluster_" + emb_space_name
        self.__check_col_categorical__(colour)

        umap_data = umap.UMAP(n_components=2, random_state=8)
        X_2d = umap_data.fit_transform(self.emb[emb_space_name]["emb"])

        fig = get_scatter_plot(
            emb_object=self,
            emb_space_name=emb_space_name,
            colour=colour,
            X_2d=X_2d,
            method="UMAP",
        )
        return fig

    def visualise_emb_tsne(
        self, emb_space_name: str, colour: str = None, perplexity=10
    ) -> go.Figure:
        """Visualise embedding space using t-SNE. The data points \
            are coloured based on the categorical column in the meta_data. \
            If no colour column is provided, the data points are coloured \
            based on their unsupervised clusters. The perplexity parameter \
            can be adjusted. The default is 10.

        Args:
            emb_space_name (str): _description_
            colour (str, optional): Categorical column in the meta_data to \
                colour the data points. Default is None and will colour the \
                data points based on their unsupervised clusters.
            perplexity (int, optional): Perplexity parameter for t-SNE.\
                Defaults to 10.

        Returns:
            go.Figure: t-SNE plot.
        """
        self.__check_for_emb_space__(emb_space_name)
        if not colour:
            colour = "cluster_" + emb_space_name
            # self.__calculate_clusters__(emb_space_name, n_clusters=None)
            # colour = "cluster_" + emb_space_name
        self.__check_col_categorical__(colour)

        tsne = TSNE(n_components=2, random_state=8, perplexity=perplexity)
        X_2d = tsne.fit_transform(self.emb[emb_space_name]["emb"])

        fig = get_scatter_plot(
            emb_object=self,
            emb_space_name=emb_space_name,
            colour=colour,
            X_2d=X_2d,
            method="t-SNE",
        )
        return fig

    def plot_feature_cluster_overlap(
        self, emb_space_name: str, feature: str
    ) -> go.Figure:
        """Bar plot showing the agreement between unsupervised clusters \
            and a categorical feature in the meta_data. The x-axis shows \
            the feature values and the y-axis shows the number of samples. \
            The bars are coloured based on the unsupervised clusters. \
            The plot is for a specific embedding space.

        Args:
            emb_space_name (str): Name of the embedding space.
            feature (str): Categorical column in the meta_data. \
                Can also refer to an unbiased cluster by specifying \
                "cluster_" + emb_space_name.

        Returns:
            go.Figure: Bar plot.
        """
        self.__check_col_categorical__(feature)
        self.__check_for_emb_space__(emb_space_name)

        # plot a bar plot with features on x-axis and number of samples on
        # y-axis coloured by the different clusters

        fig = (
            px.bar(
                self.meta_data,
                x=feature,
                color="cluster_" + emb_space_name,
                title=f"Agreement between unsupervised clusters and {feature} clusters for {emb_space_name} embeddings",  # noqa
                labels={
                    "cluster_" + emb_space_name: "Unsupervised cluster",
                    feature: feature.capitalize(),
                    "count": "Number of samples",
                },
                color_discrete_map=self.colour_map[
                    "cluster_" + emb_space_name
                ],
            )
            .update_traces(marker_line_width=0)
            .update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        )
        # order x-axis categories by category name
        fig.update_xaxes(categoryorder="category ascending")
        fig = update_fig_layout(fig)
        return fig

    def plot_emb_hist(
        self,
    ) -> go.Figure:
        """Plot histogram of embedding values for all embedding spaces. \
            The colour of the histogram bars corresponds to the embedding \
            space.

        Returns:
            go.Figure: Histogram plot.
        """
        # merge embedding data into one dataframe with emb_name as column
        df_emb = pd.DataFrame(columns=["emb_space", "emb_values"])
        for emb_space in self.emb.keys():
            emb_values = self.emb[emb_space]["emb"].flatten()
            emb_space_col = [emb_space] * len(emb_values)
            df_emb = pd.concat(
                [
                    df_emb,
                    pd.DataFrame(
                        {"emb_space": emb_space_col, "emb_values": emb_values}
                    ),
                ]
            )
        fig = px.histogram(
            df_emb,
            x="emb_values",
            color="emb_space",
            labels={"emb_values": "Embedding values"},
            title="Distribution of embedding values",
            color_discrete_map={
                emb: self.emb[emb]["colour"] for emb in self.emb.keys()
            },
            marginal="box",
            opacity=0.5,
            # do not stack
            barmode="overlay",
        )
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        fig = update_fig_layout(fig)
        return fig

    def plot_emb_box(self, group: str) -> go.Figure:
        """Plot box plot of embedding values for all embedding spaces. \
            Statified by a categorical column in the meta_data. \
            The colour of the box plots corresponds to the embedding space.

        Args:
            group (str): Categorical column in the meta_data. \
                or "sample" to stratify by sample names.

        Returns:
            go.Figure: Box plot.
        """
        # group: either "sample" or "meta_col"
        if group != "sample":
            self.__check_col_categorical__(group)
        df_emb = pd.DataFrame(columns=["emb_space", "emb_group", "emb_values"])
        for emb_space in self.emb.keys():
            emb_values = self.emb[emb_space]["emb"].flatten()
            if group == "sample":
                emb_group = list(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            x, self.emb[emb_space]["emb"].shape[1]
                        )
                        for x in self.sample_names
                    )
                )
            else:
                emb_group = list(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            x, self.emb[emb_space]["emb"].shape[1]
                        )
                        for x in self.meta_data[group].tolist()
                    )
                )
            emb_space_col = [emb_space] * len(emb_values)
            df_emb = pd.concat(
                [
                    df_emb,
                    pd.DataFrame(
                        {
                            "emb_space": emb_space_col,
                            "emb_group": emb_group,
                            "emb_values": emb_values,
                        }
                    ),
                ]
            )
        fig = px.box(
            df_emb,
            x="emb_group",
            y="emb_values",
            color="emb_space",
            title="Distribution of embedding values per {}".format(group),
            color_discrete_map={
                emb: self.emb[emb]["colour"] for emb in self.emb.keys()
            },
            labels={
                "emb_values": "Embedding values",
                "emb_group": group.capitalize(),
            },
        )
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        fig.update_xaxes(categoryorder="category ascending")
        fig = update_fig_layout(fig)
        return fig

    def plot_emb_dis_heatmap(
        self,
        emb_space_name: str,
        distance_metric: str,
        order_x: str = None,
        order_y: str = None,
        rank: str = False,
    ) -> go.Figure:
        """Plot heatmap of pairwise distance matrix for an embedding space. \
            The distance matrix is calculated using a distance metric. \
            The samples can be ordered by a categorical column in the \
            meta_data. The heatmap is coloured based on the distance values. \
            If rank is True, the distance matrix is converted to percentiles \
            before plotting.

        Args:
            emb_space_name (str): Name of the embedding space.
            distance_metric (str): Name of the distance metric.
            order_x (str, optional): Categorical column in the meta_data to \
                order the samples on the x-axis. Defaults to None.
            order_y (str, optional): Categorical column in the meta_data to \
                order the samples on the y-axis. Defaults to None.
            rank (str, optional): Either "order", "normal_dis" or \
                "bimodal_dis". If rank is True, the distance matrix is \
                converted to percentiles before plotting. Defaults to None.

        Returns:
            go.Figure: Heatmap plot.
        """
        self.__check_for_emb_space__(emb_space_name)
        if order_x is not None:
            self.__check_col_categorical__(order_x)
        if order_y is not None:
            self.__check_col_categorical__(order_y)

        emb_pwd = self.get_sample_distance(
            emb_space_name=emb_space_name,
            metric=distance_metric,
            rank=rank,
        )

        # find indices of samples for each order_x and order_y
        if order_x is not None:
            # find all sample ids for each order_x from meta_data
            order_x_indices = [
                self.meta_data[self.meta_data[order_x] == x].index.tolist()
                for x in self.meta_data[order_x].unique()
            ]
            order_x_indices = list(
                itertools.chain.from_iterable(order_x_indices)
            )
            emb_pwd = emb_pwd[order_x_indices, :]
        else:
            order_x_indices = list(range(len(self.sample_names)))

        if order_y is not None:
            # find all sample ids for each order_y from meta_data
            order_y_indices = [
                self.meta_data[self.meta_data[order_y] == y].index.tolist()
                for y in self.meta_data[order_y].unique()
            ]
            order_y_indices = list(
                itertools.chain.from_iterable(order_y_indices)
            )
            emb_pwd = emb_pwd[:, order_y_indices]
        else:
            order_y_indices = list(range(len(self.sample_names)))

        if rank:
            title = f"Rank of {distance_metric_aliases[distance_metric]} distance matrix of {emb_space_name} embedding space"  # noqa
        else:
            title = f"{distance_metric_aliases[distance_metric]} distance matrix of {emb_space_name} embedding space"  # noqa

        fig = px.imshow(
            emb_pwd,
            labels=dict(
                x="Sample",
                y="Sample",
                color=f"{distance_metric_aliases[distance_metric]} Distance",
            ),
            x=[self.sample_names[i] for i in order_x_indices],
            y=[self.sample_names[i] for i in order_y_indices],
            title=title,
            color_continuous_scale="Reds",
        )
        fig = update_fig_layout(fig)
        return fig

    def plot_emb_dis_box(
        self,
        group: str,
        distance_metric: str,
    ) -> go.Figure:
        """Plot box plot of pairwise distance values for all embedding \
            spaces. The distance values are stratified by a categorical \
            column in the meta_data. The colour of the box plots corresponds \
            to the embedding space.

        Args:
            group (str): Categorical column in the meta_data.
            distance_metric (str): Name of the distance metric.

        Returns:
            go.Figure: Box plot.
        """
        # group: either "sample" or "meta_col"
        if group != "sample":
            self.__check_col_categorical__(group)
        df_emb = pd.DataFrame(columns=["emb_space", "emb_group", "emb_values"])
        for emb_space in self.emb.keys():
            emb_dist_values = self.get_sample_distance(
                emb_space, distance_metric
            ).flatten()
            if group == "sample":
                emb_group = list(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            x, self.emb[emb_space]["emb"].shape[0]
                        )
                        for x in self.sample_names
                    )
                )
            else:
                emb_group = list(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            x, self.emb[emb_space]["emb"].shape[0]
                        )
                        for x in self.meta_data[group].tolist()
                    )
                )
            emb_space_col = [emb_space] * len(emb_dist_values)
            df_emb = pd.concat(
                [
                    df_emb,
                    pd.DataFrame(
                        {
                            "emb_space": emb_space_col,
                            "emb_group": emb_group,
                            "emb_values": emb_dist_values,
                        }
                    ),
                ]
            )
        fig = px.box(
            df_emb,
            x="emb_group",
            y="emb_values",
            color="emb_space",
            title=f"Distribution of {distance_metric_aliases[distance_metric]} distance values per {group}",  # noqa
            color_discrete_map={
                emb: self.emb[emb]["colour"] for emb in self.emb.keys()
            },
            labels={
                "emb_values": f"{distance_metric_aliases[distance_metric]} distance",  # noqa
                "emb_group": "",
            },
        )
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        fig.update_xaxes(categoryorder="category ascending")
        fig = update_fig_layout(fig)
        return fig

    def plot_emb_dis_continuous_correlation(
        self,
        emb_space_name: str,
        distance_metric: str,
        feature: str,
        rank: str = None,
    ) -> go.Figure:
        """Plot scatter plot of pair-wise distance values vs continuous \
            feature values. The correlation between the two is calculated \
            using Spearman correlation. The plot is for a specific embedding \
            space.

        Args:
            emb_space_name (str): Name of the embedding space.
            distance_metric (str): Name of the distance metric.
            feature (str): Continuous column in the meta_data.
            rank (str, optional): Name of the rank method. Either "order", \
                "normal_dis" or "bimodal_dis". Defaults to None.

        Returns:
            go.Figure: _description_
        """
        self.__check_for_emb_space__(emb_space_name)
        if feature in self.pw_meta_data.keys():
            feature_matrix = self.pw_meta_data[feature]

        else:
            self.__check_col_numeric__(feature)

            # calculate pairwise differenc between features
            feature_matrix = np.zeros(
                (len(self.sample_names), len(self.sample_names))
            )
            feature_values = self.meta_data[feature].values
            for i in range(len(feature_values)):
                for j in range(i + 1, len(feature_values)):
                    feature_matrix[i, j] = (
                        feature_values[i] - feature_values[j]
                    )

        emb_pwd = self.get_sample_distance(
            emb_space_name, distance_metric, rank
        )

        # convert into 1D array
        emb_pwd_flat = convert_to_1d_array(emb_pwd)
        feature_matrix_flat = convert_to_1d_array(feature_matrix)

        # calculate correlation between distance matrix and feature
        corr, p_value = stats.spearmanr(emb_pwd_flat, feature_matrix_flat)

        # get list with sample names for each pair wise distance
        sample_names = []
        for i in range(len(self.sample_names)):
            for j in range(i + 1, len(self.sample_names)):
                sample_names.append(
                    f"{self.sample_names[i]} - {self.sample_names[j]}"
                )

        fig = px.scatter(
            x=emb_pwd_flat,
            y=feature_matrix_flat,
            hover_data={"sample": sample_names},
            marginal_x="histogram",
            marginal_y="histogram",
            color_discrete_sequence=["darkred"],
            opacity=0.5,
        )

        fig.update_layout(
            title=f"Correlation between pair-wise {distance_metric} distance vs {feature} distance for {emb_space_name} <br> Spearman correlation: {corr:.2f} <br> p-value: {p_value:.2f}",  # noqa
            xaxis_title=f"{distance_metric_aliases[distance_metric]} distance",
            yaxis_title=feature,
            width=800,
            height=600,
        )
        fig.update_layout(showlegend=False)
        fig = update_fig_layout(fig)
        return fig

    def plot_emb_dis_scatter(
        self,
        emb_space_name_1: str,
        emb_space_name_2: str,
        distance_metric: str,
        colour_group: str = None,
        colour_value_1: str = None,
        colour_value_2: str = None,
        rank: str = None,
    ) -> go.Figure:
        """Plot scatter plot of pair-wise distance values between two \
            embedding spaces. The distance values are coloured based on a \
            categorical column in the meta_data. The plot is for a specific \
            embedding space. If only the colour_group is provided, the plot \
            will show all pairs of groups. If colour_value_1 and \
            colour_value_2 are provided, the plot will colour the distance \
            between the two groups.

        Args:
            emb_space_name_1 (str): Name of the first embedding space on the \
                x-axis.
            emb_space_name_2 (str): Name of the second embedding space on \
                the y-axis.
            distance_metric (str): Name of the distance metric.
            colour_group (str, optional): Categorical column in the meta_data \
                to colour the data points. Defaults to None.
            colour_value_1 (str, optional): Value in the colour_group to \
                colour the data points. Defaults to None.
            colour_value_2 (str, optional): Value in the colour_group to \
                colour the data points. Defaults to None.
            rank (str, optional): Name of the rank method. Either "order", \
                "normal_dis" or "bimodal_dis". Defaults to None.

        Returns:
            go.Figure: Scatter plot.
        """

        self.__check_for_emb_space__(emb_space_name_1)
        self.__check_for_emb_space__(emb_space_name_2)

        if colour_group is not None:
            self.__check_col_categorical__(colour_group)
            # check if subset_group_value is in the meta_data
            if colour_value_1 is not None:
                if colour_value_1 not in [
                    str(value)
                    for value in self.meta_data[colour_group].unique()
                ]:
                    raise ValueError(
                        f"{colour_value_1} not found in {colour_group}"
                    )
                if colour_value_2 is not None:
                    if (
                        colour_value_2
                        not in self.meta_data[colour_group].unique()
                    ):
                        raise ValueError(
                            f"{colour_value_2} not found in {colour_group}"
                        )
            else:
                raise ValueError(
                    "Please provide a colour_value or set colour_group=None"
                )

        emb_pwd_1 = self.get_sample_distance(
            emb_space_name_1, distance_metric, rank
        )
        emb_pwd_2 = self.get_sample_distance(
            emb_space_name_2, distance_metric, rank
        )

        if colour_group is not None:
            if colour_value_2 is None:
                # find incides of all groups
                sample_indices_per_group = self.__sample_indices_to_groups__(
                    colour_group
                )
                pairs_of_groups = list(
                    itertools.combinations_with_replacement(
                        sample_indices_per_group.keys(), 2
                    )
                )

                # filter for pairs of groups that contain colour_value_1
                pairs_of_groups = [
                    pair for pair in pairs_of_groups if colour_value_1 in pair
                ]

                colour = []
                # get indices of samples for each group
                for i in range(len(self.sample_names)):
                    for j in range(i + 1, len(self.sample_names)):
                        # get group of sample i
                        group_i = str(
                            [
                                key
                                for key, value in sample_indices_per_group.items()  # noqa
                                if i in value
                            ][0]
                        )
                        group_j = str(
                            [
                                key
                                for key, value in sample_indices_per_group.items()  # noqa
                                if j in value
                            ][0]
                        )

                        if ((group_i, group_j) in pairs_of_groups) or (
                            (group_j, group_i) in pairs_of_groups
                        ):
                            if group_i == colour_value_1:
                                colour.append(
                                    "{} - {}".format(group_i, group_j)
                                )
                            else:
                                colour.append(
                                    "{} - {}".format(group_j, group_i)
                                )
                        else:
                            colour.append(f"Not {colour_value_1}")
                    colour_map = None

            else:
                group_indices_1 = self.meta_data[
                    self.meta_data[colour_group] == colour_value_1
                ].index.tolist()
                group_indices_2 = self.meta_data[
                    self.meta_data[colour_group] == colour_value_2
                ].index.tolist()
                colour = []

                for i in range(len(self.sample_names)):
                    for j in range(i + 1, len(self.sample_names)):
                        if (i in group_indices_1 and j in group_indices_2) or (
                            i in group_indices_2 and j in group_indices_1
                        ):
                            colour.append(f"{colour_value_1}-{colour_value_2}")
                        elif i in group_indices_1 and j in group_indices_1:
                            colour.append(f"{colour_value_1}-{colour_value_1}")
                        elif i in group_indices_2 and j in group_indices_2:
                            colour.append(f"{colour_value_2}-{colour_value_2}")
                        else:
                            colour.append(
                                f"Not {colour_value_1} or {colour_value_2}"
                            )

                    colour_map = {
                        f"{colour_value_1}-{colour_value_2}": "steelblue",
                        f"{colour_value_1}-{colour_value_1}": "darkred",
                        f"{colour_value_2}-{colour_value_2}": "navy",
                        f"Not {colour_value_1} or {colour_value_2}": "lightgray",  # noqa
                    }

        else:
            colour = None
            colour_map = None

        sample_names = []
        # add sample names
        for i in range(len(self.sample_names)):
            for j in range(i + 1, len(self.sample_names)):
                sample_names.append(
                    f"{self.sample_names[i]} - {self.sample_names[j]}"
                )

        if rank in ["order", "normal_dis", "bimodal_dis"]:
            title = f"Rank of {distance_metric_aliases[distance_metric]} distance values between {emb_space_name_1} and {emb_space_name_2} when adjusted by {rank}"  # noqa
        else:
            title = f"{distance_metric_aliases[distance_metric]} distance values between {emb_space_name_1} and {emb_space_name_2}"  # noqa

        # calucalte correlation between emb_pwd_1 and emb_pwd_2
        corr, p_value = stats.spearmanr(
            convert_to_1d_array(emb_pwd_1), convert_to_1d_array(emb_pwd_2)
        )

        fig = px.scatter(
            x=convert_to_1d_array(emb_pwd_1),
            y=convert_to_1d_array(emb_pwd_2),
            labels={
                "x": f"{emb_space_name_1} {distance_metric_aliases[distance_metric]} distance",  # noqa
                "y": f"{emb_space_name_2} {distance_metric_aliases[distance_metric]} distance",  # noqa
            },
            title=title,
            opacity=0.7,
            color=colour,
            color_discrete_map=colour_map,
            hover_data={"Sample pair": sample_names},
            hover_name=sample_names,
        )
        # add correlation to title
        fig.update_layout(
            title=f"{title} <br> Spearman correlation: {corr:.2f} <br> p-value: {p_value:.4f}"  # noqa
        )
        # adjust x and y axis to be the same scale
        fig.update_xaxes(
            range=[0, max(emb_pwd_1.max() * 1.1, emb_pwd_2.max() * 1.1)],
            title=f"{emb_space_name_1} {distance_metric_aliases[distance_metric]} distance",  # noqa
        )
        fig.update_yaxes(
            range=[0, max(emb_pwd_1.max() * 1.1, emb_pwd_2.max() * 1.1)],
            title=f"{emb_space_name_2} {distance_metric_aliases[distance_metric]} distance",  # noqa
        )
        fig = update_fig_layout(fig)
        fig.update_layout(width=800, height=800)

        return fig

    def plot_emb_dis_hist(self, distance_metric: str) -> go.Figure:
        """Plot histogram of pairwise distance values for all embedding \
            spaces. The distance values are flattened and plotted as a \
            histogram. The colour of the histogram bars corresponds to the \
            embedding space.

        Args:
            distance_metric (str): Name of the distance metric.

        Returns:
            go.Figure: Histogram plot.
        """
        for emb_space_name in self.emb.keys():
            if "distance" not in self.emb[emb_space_name].keys():
                self.emb[emb_space_name]["distance"] = dict()
            if (
                distance_metric
                not in self.emb[emb_space_name]["distance"].keys()
            ):
                self.emb[emb_space_name]["distance"][distance_metric] = (
                    self.get_sample_distance(emb_space_name, distance_metric)
                )

        fig = go.Figure()
        for emb_space_name in self.emb.keys():
            fig.add_trace(
                go.Histogram(
                    x=squareform(
                        self.emb[emb_space_name]["distance"][distance_metric]
                    ),
                    name=emb_space_name,
                    opacity=0.8,
                    marker_color=self.emb[emb_space_name]["colour"],
                )
            )
        fig.update_layout(
            title=f"Distribution of {distance_metric_aliases[distance_metric]} distance values for {len(self.emb.keys())} embedding spaces",  # noqa
            xaxis_title=f"{distance_metric_aliases[distance_metric]} distance",
            yaxis_title="Number of samples",
            barmode="overlay",
        )
        fig = update_fig_layout(fig)
        return fig

    def plot_emb_dis_dif_heatmap(
        self,
        emb_space_name_1: str,
        emb_space_name_2: str,
        distance_metric: str,
        rank: str = None,
    ) -> go.Figure:
        """Plot heatmap of pairwise distance difference matrix between two \
            embedding spaces. The distance difference matrix is calculated \
            by subtracting the distance matrix of emb_space_name_2 from \
            emb_space_name_1. The heatmap is coloured based on the distance \
            values. If rank is True, the distance matrix is converted to \
            percentiles before the calculation.

        Args:
            emb_space_name_1 (str): Name of the first embedding space.
            emb_space_name_2 (str): Name of the second embedding space.
            distance_metric (str): Name of the distance metric.
            rank (str, optional): Name of the rank method. Either "order", \
                "normal_dis" or "bimodal_dis". Defaults to None.

        Returns:
            go.Figure: _description_
        """
        for emb_space_name in [emb_space_name_1, emb_space_name_2]:
            self.__check_for_emb_space__(emb_space_name)
        emb_pwd_diff = self.get_sample_distance_difference(
            emb_space_name_1=emb_space_name_1,
            emb_space_name_2=emb_space_name_2,
            distance_metric=distance_metric,
            rank=rank,
        )
        if rank:
            title = f"Rank of {distance_metric_aliases[distance_metric]} distance difference matrix from {emb_space_name_1} to {emb_space_name_2} embedding space"  # noqa
        else:
            title = f"{distance_metric_aliases[distance_metric]} distance difference matrix from {emb_space_name_1} to {emb_space_name_2} embedding space"  # noqa
        fig = px.imshow(
            emb_pwd_diff,
            labels=dict(
                x="Sample",
                y="Sample",
                color="",
            ),
            x=self.sample_names,
            y=self.sample_names,
            title=title,
            color_continuous_scale="rdbu",
        )
        fig.update_layout(
            template="plotly_white",
            font=dict(family="Arial", size=12, color="black"),
        )
        return fig

    def plot_emb_dis_dif_box(
        self,
        emb_space_name_1: str,
        emb_space_name_2: str,
        group: str,
        distance_metric: str,
    ) -> go.Figure:
        """Plot box plot of pairwise distance difference values between two \
            embedding spaces. The distance difference values are stratified \
            by a categorical column in the meta_data. The colour of the box \
            plots corresponds to the pair of embedding spaces.

        Args:
            emb_space_name_1 (str): Name of the first embedding space.
            emb_space_name_2 (str): Name of the second embedding space.
            group (str): Categorical column in the meta_data.
            distance_metric (str): Name of the distance metric.

        Returns:
            go.Figure: Box plot.
        """
        self.__check_col_categorical__(group)

        group_ids = self.__sample_indices_to_groups__(group=group)
        delta_emb_pwd = self.get_sample_distance_difference(
            emb_space_name_1=emb_space_name_1,
            emb_space_name_2=emb_space_name_2,
            distance_metric=distance_metric,
        )

        delta_emb_pwd_per_group = {
            group_name: dict() for group_name in group_ids.keys()
        }
        for group_name, indices in group_ids.items():
            other_indices = list(
                set(list(range(len(self.sample_names)))) - set(indices)
            )
            pairs_within_group = get_unique_pairs(indices)
            pairs_with_outside_group = generate_cross_list_pairs(
                indices_1=indices, indices_2=other_indices
            )
            # get delta_emb_pwd for pairs_within_group
            delta_emb_pwd_per_group[group_name]["within_group"] = [
                delta_emb_pwd[pair] for pair in pairs_within_group
            ]
            delta_emb_pwd_per_group[group_name]["outside_group"] = [
                delta_emb_pwd[pair] for pair in pairs_with_outside_group
            ]
        df = pd.DataFrame(columns=["group", "distance", "pair_type"])
        for group_name, delta_emb_pwd in delta_emb_pwd_per_group.items():
            for pair_type, delta_emb_pwd_values in delta_emb_pwd.items():
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame(
                            {
                                "group": [group_name]
                                * len(delta_emb_pwd_values),
                                "distance": delta_emb_pwd_values,
                                "pair_type": [pair_type]
                                * len(delta_emb_pwd_values),
                            }
                        ),
                    ]
                )
        fig = px.box(
            df,
            x="group",
            y="distance",
            color="pair_type",
            title=f"Distribution of {distance_metric_aliases[distance_metric]} distance difference values per {group}",  # noqa
            color_discrete_map={
                "within_group": "slategray",
                "outside_group": "lightsteelblue",
            },
            labels={
                "distance": f"{distance_metric_aliases[distance_metric]} distance difference",  # noqa
                "group": "",
            },
        )
        # rename legend with more descriptive names
        fig.for_each_trace(
            lambda trace: trace.update(
                name=(
                    "Within group"
                    if trace.name == "within_group"
                    else "Outside group"
                )
            )
        )
        # hide legend title
        fig.update_layout(
            template="plotly_white",
            font=dict(family="Arial", size=12),
            legend=dict(
                title=None,
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        fig.update_xaxes(categoryorder="category ascending")
        fig = update_fig_layout(fig)
        return fig

    def plot_emb_dis_per_group(
        self,
        emb_space_name: str,
        distance_metric: str,
        group: str,
        group_value: str = None,
        rank: str = None,
        plot_type: str = "violin",
        log_scale: bool = False,
    ) -> go.Figure:
        """Plot distribution of pairwise distance values stratified by a \
            categorical column in the meta_data. The plot can be either a \
            violin plot or a box plot. The distance values are coloured based \
            on whether the pairs of samples are within the same group or \
            between different groups. If group_value is provided, the plot \
            will only show the distribution of distance values for that group.

        Args:
            emb_space_name (str): Name of the embedding space.
            distance_metric (str): Name of the distance metric.
            group (str): Categorical column in the meta_data.
            group_value (str, optional): If provided, the plot will only show \
                the distribution of distance values for that group. Defaults \
                to None.
            rank (str, optional): Name of the rank method. Either "order", \
                "normal_dis" or "bimodal_dis". Defaults to None.
            plot_type (str, optional): Either "violin" or "box". Defaults to \
                "violin".
            log_scale (bool, optional): If True, the y-axis will be in log \
                scale. Defaults to False.

        Returns:
            go.Figure: Violin or box plot.
        """
        self.__check_for_emb_space__(emb_space_name)
        self.__check_col_categorical__(group)

        # get pairs of indices for each group
        pw_distances = self.get_sample_distance(
            emb_space_name, distance_metric, rank
        )

        # stratify the pairs of indices by group
        sample_ids_per_group = self.__sample_indices_to_groups__(group=group)

        group_combinations = list(
            itertools.combinations_with_replacement(
                sample_ids_per_group.keys(), 2
            )
        )

        if group_value is not None:
            if group_value not in sample_ids_per_group.keys():
                raise ValueError(f"{group_value} not found in {group}")

            group_combinations = [
                (group_1, group_2)
                for group_1, group_2 in group_combinations
                if (group_1 == group_value) or (group_2 == group_value)
            ]

        # filter group

        # for each group combination, get the pairwise distances
        group_pw_distances = {}

        for group_1, group_2 in group_combinations:
            group_1_indices = sample_ids_per_group[group_1]
            group_2_indices = sample_ids_per_group[group_2]

            group_pw_distances[f"{group_1} - {group_2}"] = dict()
            # find all values for each pair of indices
            matrix_idx = generate_cross_list_pairs(
                group_1_indices, group_2_indices
            )

            group_pw_distances[f"{group_1} - {group_2}"]["pw_distances"] = [
                pw_distances[idx[0], idx[1]] for idx in matrix_idx
            ]
            if group_1 == group_2:
                group_pw_distances[f"{group_1} - {group_2}"][
                    "pair_type"
                ] = "within_group"
            else:
                group_pw_distances[f"{group_1} - {group_2}"][
                    "pair_type"
                ] = "outside_group"

        # create a dataframe for plotting
        df = pd.DataFrame(columns=["group", "distance", "pair_type"])

        for group_combination, group_data in group_pw_distances.items():
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        {
                            "group": [group_combination]
                            * len(group_data["pw_distances"]),
                            "distance": group_data["pw_distances"],
                            "pair_type": [group_data["pair_type"]]
                            * len(group_data["pw_distances"]),
                        }
                    ),
                ]
            )

        if plot_type == "violin":
            fig = px.violin(
                df,
                x="group",
                y="distance",
                color="pair_type",
                color_discrete_sequence=["slategray", "lightsteelblue"],
            )
        elif plot_type == "box":
            fig = px.box(
                df,
                x="group",
                y="distance",
                color="pair_type",
                color_discrete_map={
                    "within_group": "slategray",
                    "outside_group": "lightsteelblue",
                },
            )
        else:
            raise ValueError(
                f"Invalid value for plot_type: {plot_type}. Must be either 'violin' or 'box'"  # noqa
            )
        # update title
        fig.update_layout(
            title=f"Distribution of {distance_metric_aliases[distance_metric]} distance values per {group}",  # noqa
        )
        # update x and y axis labels
        fig.update_xaxes(title_text="")
        fig.update_yaxes(
            title_text=f"{distance_metric_aliases[distance_metric]} distances"
        )
        fig.for_each_trace(
            lambda trace: trace.update(
                name=(
                    "Within group"
                    if trace.name == "within_group"
                    else "Outside group"
                )
            )
        )
        # update name of legend
        fig.update_layout(
            legend=dict(
                title=None,
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        if log_scale:
            fig.update_yaxes(
                type="log",
                title_text=f"Log of {distance_metric_aliases[distance_metric]} distances",  # noqa
            )
        fig = update_fig_layout(fig)
        # change x-axes text to be vertical
        fig.update_layout(xaxis_tickangle=-90)
        return fig

    def plot_emb_dis_his_with_fitted_functions(
        self,
        emb_space_name: str,
        distance_metric: str,
        rank: str,
    ) -> go.Figure:
        """Plot histogram of pairwise distance values for all embedding \
            spaces. The distance values are flattened and plotted as a \
            histogram. The colour of the histogram bars corresponds to the \
            embedding space. The plot also includes fitted Gaussian or \
            Bi-modal Gaussian mixture functions. The rank parameter is used \
            to determine which function to fit.

        Args:
            emb_space_name (str): Name of the embedding space.
            distance_metric (str): Name of the distance metric.
            rank (str): Name of the rank method. Either "normal_dis" or \
                "bimodal_dis".

        Returns:
            go.Figure: Histogram plot.
        """
        self.__check_for_emb_space__(emb_space_name)

        emb_pwd = self.get_sample_distance(
            emb_space_name=emb_space_name,
            metric=distance_metric,
        )

        if rank == "bimodal_dis":
            fig = global_percentiles_gaussian_mixture(emb_pwd, plot=True)
        elif rank == "normal_dis":
            fig = global_percentiles_normal_distribution(emb_pwd, plot=True)
        else:
            raise ValueError(
                f"Invalid value for rank: {rank}. Must be either 'normal_dis' or 'bimodal_dis'"  # noqa
            )
        return fig

    def plot_emb_cor_per_dim(
        self,
        emb_space_name: str,
        feature: str,
    ) -> go.Figure:
        """Plot scatter plot of embedding values for each dimension of the \
            embedding space with a continuous or categorical column in the \
            meta_data. The plot is coloured based on the feature values.

        Args:
            emb_space_name (str): Name of the embedding space.
            feature (str): Continuous or categorical column in the meta_data.

        Returns:
            go.Figure: Scatter plot.
        """
        self.__check_for_emb_space__(emb_space_name)
        self.__check_col_in_meta_data__(feature)

        emb_values = self.emb[emb_space_name]["emb"]
        feature_values = self.meta_data[feature].values

        if feature in self.meta_data_numeric_columns:

            # calculate the correlation between each dimension
            # of the embedding and the feature
            corrs = []
            p_values = []
            p_values_sig = []

            p_value_sig_threshold = 0.05 / emb_values.shape[1]

            for i in range(emb_values.shape[1]):
                corr, p_value = stats.spearmanr(
                    emb_values[:, i], feature_values
                )
                corrs.append(corr)
                p_values.append(p_value)
                p_values_sig.append(p_value < p_value_sig_threshold)
            fig = px.scatter(
                x=list(range(1, emb_values.shape[1] + 1)),
                y=corrs,
                color=p_values_sig,
                hover_data={
                    "Dimension": list(range(1, emb_values.shape[1] + 1)),
                    "Correlation": corrs,
                    "p-value": p_values,
                },
                labels={
                    "x": "Dimension",
                    "y": "Spearman correlation with feature",
                },
                color_discrete_map={True: "darkred", False: "lightgray"},
            )
            fig.update_layout(
                title=f"Spearman correlation between each dimension of the {emb_space_name} embedding and {feature}",  # noqa
                xaxis_title="Dimension",
                yaxis_title="Correlation",
            )
            # rename legend
            fig.for_each_trace(
                lambda trace: trace.update(
                    name=(
                        f"P-value < {p_value_sig_threshold}"
                        if trace.name == "True"
                        else "Not significant"
                    )
                )
            )
            fig = update_fig_layout(fig)
            return fig

        else:

            # create a dataframe with the emb values and the feature
            df = pd.DataFrame(
                emb_values,
                columns=[
                    f"Dimension {i+1}" for i in range(emb_values.shape[1])
                ],
            )

            # add the feature values
            df[feature] = feature_values

            # melt the dataframe

            df_melt = df.melt(
                id_vars=[feature],
                var_name="Dimension",
                value_name="Embedding value",
            )

            # create the plot
            fig = px.scatter(
                df_melt,
                x="Dimension",
                y="Embedding value",
                color=feature,
                labels={
                    "Embedding value": "Embedding value",
                    "Dimension": "Dimension",
                    feature: feature,
                },
                opacity=0.5,
                title=f"Embedding values for each dimension of the {emb_space_name} embedding coloured by {feature}",  # noqa
            )
            fig = update_fig_layout(fig)

            return fig

    def get_distances_per_group(
        self,
        emb_space_name: str,
        distance_metric: str,
        group: str,
        group_value: str = None,
        rank: str = None,
    ) -> dict:
        """Returns a dictionary with the distance values stratified by a \
            categorical column in the meta_data. The keys of the dictionary \
            are the group names and the values are lists of distance values. \
            If group_value is provided, the dictionary will only contain the \
            distance values for that group.

        Args:
            emb_space_name (str): Name of the embedding space.
            distance_metric (str): Name of the distance metric.
            group (str): Categorical column in the meta_data.
            group_value (str, optional): If provided, the distance values \
                will only be returned for that group. Defaults to None.
            rank (str, optional): Name of the rank method. Either "order", \
                "normal_dis" or "bimodal_dis". Defaults to None.

        """
        self.__check_for_emb_space__(emb_space_name)
        self.__check_col_categorical__(group)

        # get pairs of indices for each group
        pw_distances = self.get_sample_distance(
            emb_space_name, distance_metric, rank
        )

        # stratify the pairs of indices by group
        sample_ids_per_group = self.__sample_indices_to_groups__(group=group)

        group_combinations = list(
            itertools.combinations_with_replacement(
                sample_ids_per_group.keys(), 2
            )
        )

        if group_value is not None:
            if group_value not in sample_ids_per_group.keys():
                raise ValueError(f"{group_value} not found in {group}")

            group_combinations = [
                (group_1, group_2)
                for group_1, group_2 in group_combinations
                if (group_1 == group_value) or (group_2 == group_value)
            ]

        # filter group

        # for each group combination, get the pairwise distances
        group_pw_distances = {}

        for group_1, group_2 in group_combinations:
            group_1_indices = sample_ids_per_group[group_1]
            group_2_indices = sample_ids_per_group[group_2]

            group_pw_distances[f"{group_1} - {group_2}"] = dict()
            # find all values for each pair of indices
            matrix_idx = generate_cross_list_pairs(
                group_1_indices, group_2_indices
            )

            group_pw_distances[f"{group_1} - {group_2}"]["pw_distances"] = [
                pw_distances[idx[0], idx[1]] for idx in matrix_idx
            ]
            if group_1 == group_2:
                group_pw_distances[f"{group_1} - {group_2}"][
                    "pair_type"
                ] = "within_group"
            else:
                group_pw_distances[f"{group_1} - {group_2}"][
                    "pair_type"
                ] = "outside_group"

        # create a dataframe for plotting
        df = pd.DataFrame(columns=["group", "distance", "pair_type"])

        for group_combination, group_data in group_pw_distances.items():
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        {
                            "group": [group_combination]
                            * len(group_data["pw_distances"]),
                            "distance": group_data["pw_distances"],
                            "pair_type": [group_data["pair_type"]]
                            * len(group_data["pw_distances"]),
                        }
                    ),
                ]
            )

        distances_per_group = {}
        # find all values for each group
        for group in df["group"].unique():
            # find all distances
            distances_per_group[group] = list(
                df[df["group"] == group]["distance"]
            )

        return distances_per_group


def global_rank(arr: np.ndarray) -> np.ndarray:
    """
    Return the global rank of each value in the array.

    Parameters:
    arr (numpy.ndarray): Input 2D array.

    Returns:
    numpy.ndarray: Array with the same shape where each value is replaced by \
        its global rank.
    """
    flattened = squareform(arr)
    sorted_indices = np.argsort(
        flattened
    )  # returns the indices that would sort the array
    ranks = np.argsort(sorted_indices)  # get the ranks of the sorted indices
    percentile_array = squareform(ranks)
    return percentile_array


def global_percentiles_normal_distribution(
    arr: np.ndarray, plot: str = False
) -> np.ndarray:
    """
    Return the global percentiles of each value in the array based on a \
        normal distribution.

    Args:
        arr (_type_): Input 2D array.
        plot (_type_, optional): If True, a plot of the fitted normal \

    Returns:
        _type_: Array with the same shape where each value is replaced by \
            its global percentile.
    """
    # check that at least 11 entries in the array
    if len(arr) < 11:
        raise ValueError("Array must have at least 11 entries.")

    # flatten the array
    flattened = squareform(arr)

    # fit the data to a normal distribution
    mu, std = np.mean(flattened), np.std(flattened)

    if plot:
        # Create a range of values for plotting the fitted distribution
        x = np.linspace(min(flattened), max(flattened), 1000)

        # Calculate the PDF of the GMM
        pdf = np.zeros_like(x)
        for mu, cov, weight in zip([mu], [std**2], [1]):
            pdf += weight * stats.norm.pdf(x, loc=mu, scale=np.sqrt(cov))

        # Create the histogram of the data and normalize it
        hist_data = np.histogram(flattened, bins=30, density=True)
        hist_x = (
            hist_data[1][:-1] + hist_data[1][1:]
        ) / 2  # Midpoints of bins
        hist_y = hist_data[0]

        # Create the plotly figure
        fig = go.Figure()

        # Add the histogram bars
        fig.add_trace(
            go.Bar(x=hist_x, y=hist_y, name="Histogram", opacity=0.6)
        )

        # Add the fitted GMM distribution line
        fig.add_trace(
            go.Scatter(
                x=x, y=pdf, mode="lines", name="Fitted Normal Distribution"
            )
        )

        # Update layout
        fig.update_layout(
            title="Histogram and Fitted Normal Distribution",
            xaxis_title="Data Points",
            yaxis_title="Density",
            bargap=0.1,
        )

        fig = update_fig_layout(fig)

        return fig

    # calculate the percentiles
    percentiles = stats.norm.cdf(flattened, mu, std) * 100

    # reshape the percentiles to the original shape
    percentiles = squareform(percentiles)

    return percentiles


def gmm_cdf(x: list, means: list, covariances: list, weights: list) -> list:
    """Calculate the CDF of a Gaussian Mixture Model at a given value.

    Args:
        x (list): Data point at which to calculate the CDF.
        means (list): List of means of the components of the GMM.
        covariances (list): List of covariances of the components of the GMM.
        weights (): List of weights of the components of the GMM.

    Returns:
        list: CDF of the GMM at the given value.
    """
    cdf = 0.0
    for mu, cov, weight in zip(means, covariances, weights):
        cdf += weight * stats.norm.cdf(x, loc=mu, scale=np.sqrt(cov))
    return cdf


def global_percentiles_gaussian_mixture(arr: np.array, plot=False) -> np.array:
    """Return the global percentiles of each value in the array based on a \
        Gaussian Mixture Model.

    Args:
        arr (np.array): Input 2D array.
        plot (bool, optional): If True, a plot of the fitted Gaussian Mixture \
            Model will be returned. Defaults to False.

    Raises:
        ValueError: Array must have at least 11 entries.

    Returns:
        np.array: Array with the same shape where each value is replaced by \
            its global percentile.
    """

    # check that at least 11 entries in the array
    if len(arr) < 11:
        raise ValueError("Array must have at least 11 entries.")

    # flatten the array
    flattened = squareform(arr)

    # fit the data to a Gaussian Mixture Model with 2 components
    gmm = GaussianMixture(n_components=2)
    gmm.fit(flattened.reshape(-1, 1))

    # Extract the means, covariances, and weights of the components
    means = gmm.means_.flatten()
    covariances = gmm.covariances_.flatten()
    weights = gmm.weights_

    if plot:
        # Create a range of values for plotting the fitted distribution
        x = np.linspace(min(flattened), max(flattened), 1000)

        # Calculate the PDF of the GMM
        pdf = np.zeros_like(x)
        for mu, cov, weight in zip(means, covariances, weights):
            pdf += weight * stats.norm.pdf(x, loc=mu, scale=np.sqrt(cov))

        # Create the histogram of the data and normalize it
        hist_data = np.histogram(flattened, bins=30, density=True)
        hist_x = (
            hist_data[1][:-1] + hist_data[1][1:]
        ) / 2  # Midpoints of bins
        hist_y = hist_data[0]

        # Create the plotly figure
        fig = go.Figure()

        # Add the histogram bars
        fig.add_trace(
            go.Bar(x=hist_x, y=hist_y, name="Histogram", opacity=0.6)
        )

        # Add the fitted GMM distribution line
        fig.add_trace(
            go.Scatter(
                x=x, y=pdf, mode="lines", name="Fitted GMM Distribution"
            )
        )

        # Update layout
        fig.update_layout(
            title="Histogram and Fitted GMM Distribution",
            xaxis_title="Data Points",
            yaxis_title="Density",
            bargap=0.1,
        )

        fig = update_fig_layout(fig)

        return fig

    # Calculate the percentiles
    percentiles = np.array(
        [gmm_cdf(x, means, covariances, weights) for x in flattened]
    )

    # reshape the percentiles to the original shape
    percentiles = squareform(percentiles)

    return percentiles


def get_scatter_plot(
    emb_object: dict,
    emb_space_name: str,
    colour: str,
    X_2d: np.array,
    method: str,
) -> go.Figure:
    """Create a scatter plot of the embeddings after dimnesionality \
        reduction. The points are coloured based on the values of a \
        categorical column in the meta_data.

    Args:
        emb_object (dict): ema object.
        emb_space_name (str): Name of the embedding space.
        colour (str): Name of the column in the meta_data to use for \
            colouring the points.
        X_2d (np.array): 2D array of the embeddings after dimensionality \
            reduction.
        method (str): Name of the method used for dimensionality reduction.

    Returns:
        go.Figure: Scatter plot of the embeddings after dimensionality \
            reduction.
    """
    fig = px.scatter(
        x=X_2d[:, 0],
        y=X_2d[:, 1],
        color=[str(value) for value in emb_object.meta_data[colour]],
        labels={"color": "Cluster"},
        title=f"{method} visualization of variant embeddings of {emb_space_name} embeddings",  # noqa
        hover_data={
            "Sample": emb_object.sample_names,
        },
        opacity=0.5,
        color_discrete_map=emb_object.colour_map[colour],
    )

    # make square aspect ratio
    fig.update_layout(
        width=800,
        height=800,
        autosize=False,
        legend=dict(
            title=f"{colour.capitalize()}",
        ),
    )

    # make dots proportional to number of samples
    fig.update_traces(
        marker=dict(size=max(10, (1 / len(emb_object.sample_names)) * 400))
    )
    fig = update_fig_layout(fig)
    return fig


def update_fig_layout(fig) -> go.Figure:
    """Update the layout of a plotly figure to adjust the font, line,\
        and grid settings.

    Args:
        fig (_type_): Plotly figure object.

    Returns:
        go.Figurge : Plotly figure object with updated layout.
    """
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Arial", size=12, color="black"),
    )
    # show line at y=0 and x=0
    fig.update_xaxes(showline=True, linecolor="black", linewidth=2)
    fig.update_yaxes(showline=True, linecolor="black", linewidth=2)
    # hide gridlines
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def convert_to_1d_array(matrix) -> np.ndarray:
    """
    Convert a 2D symmetric distance matrix to a 1D array of distances. \
    The distances are extracted from the upper triangular part of the matrix \
    (excluding the diagonal).

    Parameters:
    matrix (numpy.ndarray): 2D symmetric distance matrix.

    Returns:
    numpy.ndarray: 1D array of distances of dimension \
        n(n-1)/2, where n is the number of rows/columns in the matrix.
    """
    # Get the size of the matrix
    n = matrix.shape[0]
    m = matrix.shape[1]

    # Initialize an empty array to store distances
    distances = []

    # Extract upper triangular part of the matrix (excluding diagonal)
    for i in range(n):
        for j in range(i + 1, m):
            distances.append(matrix[i, j])

    return np.array(distances)


def get_unique_pairs(indices) -> list:
    """Generate all unique pairs of indices from a list of indices. \
        Does not include pairs where the indices are the same.

    Args:
        indices (_type_): List of indices.

    Returns:
        _type_: List of unique pairs of indices.
    """
    pairs = set()
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            pairs.add((indices[i], indices[j]))
    return list(pairs)


def generate_cross_list_pairs(indices_1, indices_2) -> list:
    """Generate all pairs of indices from two lists of indices. \
        Does not include pairs where the indices are the same.

    Args:
        indices_1 (_type_): List of indices.
        indices_2 (_type_): List of indices.

    Returns:
        _type_: List of pairs of indices.
    """

    pairs = set()
    for i in range(len(indices_1)):
        for j in range(len(indices_2)):
            pair = tuple(sorted([indices_1[i], indices_2[j]]))
            pairs.add(pair)
    # remove pairs where the indices are the same
    pairs = set([pair for pair in pairs if pair[0] != pair[1]])
    return list(pairs)


if __name__ == "__main__":
    pass