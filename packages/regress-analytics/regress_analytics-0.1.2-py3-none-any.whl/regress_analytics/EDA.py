import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .utilities.utils import generate_hex_colors

# Suppress warnings
warnings.filterwarnings("ignore")


class DataDist:
    def plot(
        self,
        data_sets: list[pd.DataFrame],
        data_set_names: list[str],
        numerical_feature_names: list[str],
        categorical_feature_names: list[str],
        figsize: tuple = (9, 11),
    ):
        """
        Plots the distribution of numerical and categorical features for multiple datasets.

        Parameters
        ----------
        data_sets : list[pd.DataFrame]
            List of pandas DataFrames containing the data sets.
        data_set_names : list[str]
            List of names corresponding to each data set.
        numerical_feature_names : list[str]
            List of names of numerical features to plot.
        categorical_feature_names : list[str]
            List of names of categorical features to plot.
        figsize : tuple, optional
            Size of the figure for the plots (default is (9, 11)).

        Returns
        -------
        None
        """
        # generate custom colors
        custom_colors = generate_hex_colors(len(data_sets))
        # prepare data
        data_sets = [data.reset_index(drop=True).copy() for data in data_sets]
        all_data = pd.DataFrame(columns=list(data_sets[0].columns) + ["dataset_name"])
        for data, data_name in zip(data_sets, data_set_names):
            data["dataset_name"] = data_name
            all_data = pd.concat([all_data, data])

        all_data = all_data.reset_index(drop=True)

        # distribution plots for each feature
        if numerical_feature_names is not None:
            for feature_name in numerical_feature_names:
                fig, ax = plt.subplots(2, 1, figsize=figsize)
                # histplot and PDF
                sns.histplot(
                    data=all_data,
                    x=feature_name,
                    hue="dataset_name",
                    kde=True,
                    label=data_name,
                    stat="density",
                    ax=ax[0],
                    palette=custom_colors,
                )
                if len(data_sets) == 1:
                    ax[0].axvline(
                        data[feature_name].mean(),
                        color="magenta",
                        linestyle="dashed",
                        linewidth=2,
                        label="mean",
                    )
                    ax[0].axvline(
                        data[feature_name].median(),
                        color="cyan",
                        linestyle="dashed",
                        linewidth=2,
                        label="median",
                    )
                    ax[0].legend()
                histplot_title = f"histplot and PDF for {feature_name}"
                ax[0].set_title(
                    histplot_title,
                    fontsize=15,
                )
                # box plot
                sns.boxplot(
                    data=all_data,
                    x=feature_name,
                    y="dataset_name",
                    palette=custom_colors,
                    orient="h",
                    ax=ax[1],
                )
                boxplot_title = f"box plot for {feature_name}"
                ax[1].set_title(
                    boxplot_title,
                    fontsize=15,
                )
                plt.show()

        if categorical_feature_names is not None:
            for feature_name in categorical_feature_names:
                grouped_data = (
                    all_data.groupby(by=["dataset_name", feature_name])
                    .size()
                    .reset_index(name="count")
                )
                grouped_data["normalized_count"] = grouped_data.groupby("dataset_name")[
                    "count"
                ].apply(lambda x: x / x.sum())
                categorical_figsize = (figsize[0], int(figsize[1] / 2))
                fig, ax = plt.subplots(1, 1, figsize=categorical_figsize)
                sns.barplot(
                    data=grouped_data,
                    x=feature_name,
                    y="normalized_count",
                    hue="dataset_name",
                    palette=custom_colors,
                    ax=ax,
                )
                barplot_title = f"bar plot for {feature_name}"
                ax.set_title(
                    barplot_title,
                    fontsize=15,
                )
                plt.show()


class CorrelationMap:
    def plot(self, data: pd.DataFrame, col_names: list[str], figsize=(8, 8)):
        """
        Plots a heatmap of the correlation matrix for the specified columns in the dataset.

        Parameters
        ----------
        data : pd.DataFrame
            The dataset containing the data.
        col_names : list[str]
            List of column names to include in the correlation matrix.
        figsize : tuple, optional
            Size of the figure for the heatmap (default is (8, 8)).

        Returns
        -------
        None
        """
        corr = data.corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)

        # Add a title and show the plot
        plt.title("Correlation map")
        plt.show()
