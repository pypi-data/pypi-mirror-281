import pandas as pd


class MultiModelPredictor:
    def get_predictions(
        self,
        data: pd.DataFrame,
        models: list[object],
        model_names: list[str],
        model_features: list[list],
        multi_output_model: list[bool] = [False],
        index_to_use: list[int] = None,
    ):
        """
        Makes predictions using multiple models and returns a dictionary of model predictions.

        Parameters
        ----------
        data : pd.DataFrame
            The input data for making predictions.
        models : list[object]
            List of trained model objects that support the predict method.
        model_names : list[str]
            List of names for the models.
        model_features : list[list]
            List of lists, where each sublist contains the feature names used by the corresponding model.
        multi_output_model : list[bool], optional
            List of booleans indicating if each model is a multi-output model (default is [False]).
        index_to_use : list[int], optional
            List of indices specifying which output to use for each multi-output model. Required if any model is a multi-output model (default is None).

        Returns
        -------
        models_predictions: dict
            A dictionary where keys are model names and values are the predictions made by the models.

        Raises
        ------
        ValueError
            If index_to_use is None when there is at least a multi-output model or is None for any multi-output model.
        """
        models_predictions = dict()
        for i, model in enumerate(models):
            preds = model.predict(data[model_features[i]])
            if multi_output_model[i]:
                if (index_to_use is not None) and (index_to_use[i] is not None):
                    models_predictions[model_names[i]] = preds[:, index_to_use[i]]
                else:
                    raise ValueError(
                        "index_to_use cannot be a None value when multi_output_model contains True values"
                    )
            else:
                models_predictions[model_names[i]] = preds

        return models_predictions
