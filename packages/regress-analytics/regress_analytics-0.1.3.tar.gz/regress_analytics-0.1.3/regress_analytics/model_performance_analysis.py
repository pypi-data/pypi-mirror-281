import warnings
from collections import defaultdict
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import linregress

from .utilities.multi_model_prediction import MultiModelPredictor
from .utilities.utils import generate_hex_colors

# Suppress warnings
warnings.filterwarnings("ignore")


class PredsVsTrue:
    def plot(
        self,
        y_true: np.array,
        y_pred: Union[np.array, list[np.array]],
        model_names: list[str] = None,
        figsize=(8, 6),
    ):
        """
        Plot the true values against the predicted values for multiple models.

        Parameters
        ----------
        y_true : np.array
            The true values.
        y_pred : Union[np.array, list[np.array]]
            The predicted values. Can be a single array or a list of arrays.
        model_names : list[str], optional
            The names of the models. Required if y_pred is a list of arrays.
        figsize : tuple, optional
            The size of the figure (default is (8, 6)).

        Raises
        ------
        ValueError
            If model_names is None or its length does not match y_pred length when y_pred is a list.
        """
        if isinstance(y_pred, list):
            if model_names is None:
                raise ValueError(
                    "model_name cannot be a None value when y_pred is a list of arrays"
                )
            elif len(model_names) != len(y_pred):
                raise ValueError(
                    "length of the y_pred and model_names don't match. {len(y_pred)} != {len(model_names)}"
                )
        else:
            y_pred = [y_pred]

        fig, ax = plt.subplots(1, 1, figsize=figsize)
        colors = generate_hex_colors(len(y_pred))

        # plot the unity line
        unity_line = np.linspace(0, np.max(y_true), 50)
        ax.plot(
            unity_line, unity_line, linestyle="--", color="black", label="Unity Line"
        )
        # add the plots for each model
        for i, preds in enumerate(y_pred):
            self._add_model_plots(y_true, preds, ax, model_names[i], colors[i])

        ax.set_ylabel("predicted_slump")
        ax.legend()
        plt.show()

    def _add_model_plots(self, y_true, y_pred, ax, label, color):
        """
        Add individual model plots to the existing plot.

        Parameters
        ----------
        y_true : np.array
            The true values.
        y_pred : np.array
            The predicted values.
        ax : matplotlib.axes.Axes
            The axes object to plot on.
        label : str
            The label for the plot.
        color : str
            The color for the plot.
        """
        # Fit a line to the results of the models
        slope, intercept, r_value, p_value, std_err = linregress(y_true, y_pred)
        fitted_line = slope * y_true + intercept

        ax.plot(y_true, fitted_line, linestyle="-", color=color, label=label)
        sns.scatterplot(x=y_true, y=y_pred, color=color, ax=ax)


class SensitivityTest:
    def plot(
        self,
        features: pd.DataFrame,
        feature_col_name: str,
        models: list[object],
        model_names: list[str],
        model_features: list[list],
        multi_output_model: list[bool],
        index_to_use: list[int] = None,
        acceptable_feature_range: tuple = None,
        num_samples: int = 100,
        figsize: tuple = (8, 6),
    ):
        """
        Plot the sensitivity test results for multiple models.

        Parameters
        ----------
        features : pd.DataFrame
            The input features for making predictions.
        feature_col_name : str
            The name of the feature column to vary for the sensitivity test.
        models : list[object]
            The list of trained model objects.
        model_names : list[str]
            The names of the models.
        model_features : list[list]
            The features used by each model.
        multi_output_model : list[bool]
            Indicates if the models are multi-output models.
        index_to_use : list[int], optional
            The index to use for multi-output models.
        acceptable_feature_range : tuple, optional
            The range of feature values to test (default is None).
        num_samples : int, optional
            The number of samples to generate within the feature range (default is 100).
        figsize : tuple, optional
            The size of the figure (default is (8, 6)).

        Raises
        ------
        ValueError
            If index_to_use is None when there is at least a multi-output model or is None for any multi-output model.
        """
        features = features.copy(deep=True)

        if acceptable_feature_range is None:
            min_feature_value, max_feature_value = (
                features[feature_col_name].min(),
                features[feature_col_name].max(),
            )
            feature_range = np.linspace(
                min_feature_value, max_feature_value, num_samples
            )
        else:
            feature_range = np.linspace(
                acceptable_feature_range[0], acceptable_feature_range[1], num_samples
            )
        models_predictions = defaultdict(list)

        for i, model in enumerate(models):
            print(f"Running sensitivity test for {model_names[i]}")
            sensitivity_test_preds = []
            for sample in feature_range:
                features.loc[:, feature_col_name] = sample
                preds = model.predict(features[model_features[i]])
                if multi_output_model[i]:
                    if index_to_use is not None:
                        preds = preds[:, index_to_use[i]]
                    else:
                        raise ValueError(
                            "index_to_use cannot be a None value when multi_output_model contains True values"
                        )

                sensitivity_test_preds.append(np.mean(preds))
            models_predictions[model_names[i]] = sensitivity_test_preds

        fig, ax = plt.subplots(1, 1, figsize=figsize)
        colors = generate_hex_colors(len(models))
        chart_min_yval, chart_max_yval = 10e10, 0
        for i, model_name in enumerate(model_names):
            sns.scatterplot(
                x=feature_range,
                y=models_predictions[model_name],
                color=colors[i],
                label=model_name,
            )
            chart_min_yval = min(
                chart_min_yval, np.min(models_predictions[model_name]) * 0.95
            )
            chart_max_yval = max(
                chart_max_yval, np.max(models_predictions[model_name]) * 1.05
            )
        ax.set_title(f"sensitivity test based on {feature_col_name}")
        ax.set_xlabel(feature_col_name)
        ax.set_ylabel("averge model predictions")
        ax.set_ylim(chart_min_yval, chart_max_yval)
        ax.legend()
        plt.show()


class BinAnalyzer(MultiModelPredictor):
    def plot(
        self,
        data: pd.DataFrame,
        feature_col_name: str,
        output_col_name: str,
        models: list[object],
        model_names: list[str],
        model_features: list[list],
        multi_output_model: list[bool],
        index_to_use: list[int] = None,
        binning_method: str = "equal_width",
        num_bins: int = 50,
        aggregate_func="mean",
        figsize: tuple = (8, 6),
    ):
        """
        Plot the true values and model predictions across different bins of a specified numerical feature.

        Parameters
        ----------
        data : pd.DataFrame
            The input data containing the features and true output values.
        feature_col_name : str
            The name of the numerical feature column to bin and analyze.
        output_col_name : str
            The name of the output column with the true values.
        models : list[object]
            A list of trained model objects to use for predictions.
        model_names : list[str]
            A list of names for the models.
        model_features : list[list]
            A list of lists, where each sublist contains the feature names used by the corresponding model.
        multi_output_model : list[bool]
            A list indicating whether each model has multiple outputs.
        index_to_use : list[int], optional
            A list of indices specifying which output to use for multi-output models. Defaults to None.
        binning_method : str, optional
            The method used for binning the numerical feature ('equal_width' or 'equal_frequency'). Defaults to 'equal_width'.
        num_bins : int, optional
            The number of bins to create if using 'equal_width' binning method. Defaults to 50.
        aggregate_func : str, optional
            The aggregation function to use for aggregating data within each bin ('mean' or 'median'). Defaults to 'mean'.
        figsize : tuple, optional
            The size of the figure for the plot (default is (8, 6)).

        Returns
        -------
        aggregated_data_based_on_bins : pd.DataFrame
            Aggregated data based on the bins.

        Raises
        ------
        ValueError
            If binning_method is not 'equal_width' or 'equal_frequency'.
        """
        data = data.reset_index().drop(columns=["index"]).copy(deep=True)
        # get models' predictions
        preds = self.get_predictions(
            data=data,
            models=models,
            model_names=model_names,
            model_features=model_features,
            multi_output_model=multi_output_model,
            index_to_use=index_to_use,
        )

        preds = pd.DataFrame(preds)
        data = pd.concat([data, preds], axis=1)

        # make a copy of the feature_col_name if it is the same as output_col_name
        if feature_col_name == output_col_name:
            data[feature_col_name + "_bins"] = data[feature_col_name]
            feature_col_name = feature_col_name + "_bins"

        # Bin the data based on the selected feature
        if binning_method == "equal_width":
            bins = pd.cut(data[feature_col_name], num_bins)
        elif binning_method == "equal_frequency":
            bins = pd.qcut(data[feature_col_name], num_bins, duplicates="drop")
        else:
            raise ValueError(
                f"{binning_method} is not an acceptable bin type. Acceptable types are ['equal_width','equal_frequency']"
            )

        # Group the data based on the created bins
        grouped_data = data.groupby(bins)
        if aggregate_func == "mean":
            aggregated_data_based_on_bins = (
                grouped_data.mean().drop(columns=[feature_col_name]).reset_index()
            )
        elif aggregate_func == "median":
            aggregated_data_based_on_bins = (
                grouped_data.median().drop(columns=[feature_col_name]).reset_index()
            )
        aggregated_data_based_on_bins[feature_col_name] = aggregated_data_based_on_bins[
            feature_col_name
        ].astype(str)

        # plot true and predicted values
        colors = generate_hex_colors(len(models))
        fig, ax = plt.subplots(figsize=figsize)
        plt.xticks(rotation=90)
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.size"] = 12
        chart_name = (
            f"{output_col_name}/predicted_{output_col_name} vs {'_'.join(feature_col_name.split('_')[:-1])} bins"
            if "bins" in feature_col_name
            else f"{output_col_name}/predicted_{output_col_name} vs {feature_col_name} bins"
        )
        ax.set_title(
            chart_name,
            fontsize=20,
        )
        plt.grid(True, which="both", axis="x", linestyle="--")

        sns.scatterplot(
            data=aggregated_data_based_on_bins,
            x=feature_col_name,
            y=output_col_name,
            ax=ax,
            color="black",
        )
        sns.lineplot(
            data=aggregated_data_based_on_bins,
            x=feature_col_name,
            y=output_col_name,
            color="black",
            ax=ax,
            label=output_col_name,
        )

        for i, model_name in enumerate(model_names):

            sns.scatterplot(
                data=aggregated_data_based_on_bins,
                x=feature_col_name,
                y=model_name,
                color=colors[i],
                ax=ax,
            )
            sns.lineplot(
                data=aggregated_data_based_on_bins,
                x=feature_col_name,
                y=model_name,
                color=colors[i],
                ax=ax,
                label=f"{model_name} preds",
            )
        plt.show()
        return aggregated_data_based_on_bins


class CategoryAnalyzer(MultiModelPredictor):
    def plot(
        self,
        data: pd.DataFrame,
        feature_col_name: str,
        output_col_name: str,
        models: list[object],
        model_names: list[str],
        model_features: list[list],
        multi_output_model: list[bool],
        index_to_use: list[int] = None,
        figsize: tuple = (8, 12),
    ):
        """
        Plot the true values and model predictions across different categories of a specified feature.

        Parameters
        ----------
        data : pd.DataFrame
            The input data containing the features and true output values.
        feature_col_name : str
            The name of the categorical feature column to analyze.
        output_col_name : str
            The name of the output column with the true values.
        models : list[object]
            A list of trained model objects to use for predictions.
        model_names : list[str]
            A list of names for the models.
        model_features : list[list]
            A list of lists, where each sublist contains the feature names used by the corresponding model.
        multi_output_model : list[bool]
            A list indicating whether each model has multiple outputs.
        index_to_use : list[int], optional
            A list of indices specifying which output to use for multi-output models. Defaults to None.
        figsize : tuple, optional
            The size of the figure for the plot (default is (8, 12)).

        Raises
        ------
        ValueError
            If index_to_use is None when any model in multi_output_model is True.
        """
        data = data.reset_index().drop(columns=["index"]).copy(deep=True)
        # get models' predictions
        preds = self.get_predictions(
            data=data,
            models=models,
            model_names=model_names,
            model_features=model_features,
            multi_output_model=multi_output_model,
            index_to_use=index_to_use,
        )

        preds = pd.DataFrame(preds)
        data = pd.concat([data, preds], axis=1)
        # Melt the dataframe
        melted_data = data.melt(
            id_vars=feature_col_name,
            value_vars=[output_col_name] + model_names,
            var_name="model_name",
            value_name=f"True and predicted {output_col_name} values",
        )

        # plot true and predicted values
        colors = generate_hex_colors(len(models) + 1)
        fig, ax = plt.subplots(figsize=figsize)
        plt.xticks(rotation=90)
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.size"] = 12
        chart_name = f"{output_col_name}/predicted_{output_col_name} vs {'_'.join(feature_col_name.split('_')[:-1])} categories"
        ax.set_title(
            chart_name,
            fontsize=20,
        )
        plt.grid(True, which="both", axis="x", linestyle="--")
        # box plot
        sns.boxplot(
            data=melted_data,
            x=f"True and predicted {output_col_name} values",
            y=feature_col_name,
            hue="model_name",
            palette=colors,
            orient="h",
            ax=ax,
        )
        boxplot_title = f"Distribution of {output_col_name}, {' ,'.join(model_names)} across {feature_col_name}"
        ax.set_title(
            boxplot_title,
            fontsize=15,
        )
        plt.show()
