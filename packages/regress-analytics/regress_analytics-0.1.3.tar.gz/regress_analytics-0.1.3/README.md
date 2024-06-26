# regress_analytics Package

The `regress_analytics` package provides utilities for exploratory data analysis (EDA) and model performance analysis in regression tasks.

## Functionality Overview

### Exploratory Data Analysis (EDA)

#### Data Distribution (`DataDist`)

- Visualizes the distribution of numerical and categorical features across multiple datasets.
- Generates histograms, density plots (PDFs), and box plots to compare feature distributions.
- Helps in understanding the spread and variability of data within different datasets.

#### Correlation Map (`CorrelationMap`)

- Plots a heatmap of the correlation matrix for specified columns in a dataset.
- Shows pairwise correlations between numerical columns using color intensity.
- Facilitates identifying strong correlations (positive or negative) between features.

### Model Performance Analysis

#### Predictions vs True Values (`PredsVsTrue`)

- Compares predicted values against true values for regression models.
- Visualizes scatter plots and line plots to assess model accuracy and bias.
- Useful for evaluating how well models predict outcomes across different datasets.

#### Sensitivity Test (`SensitivityTest`)

- Conducts sensitivity analysis by varying input features and observing model predictions.
- Plots sensitivity curves to understand how changes in input variables affect model outputs.
- Helps in assessing the robustness and stability of regression models.

#### Binning Analyzer (`BinAnalyzer`)

- Analyzes model predictions across binned segments of a feature.
- Visualizes true values and predicted values within each bin using scatter plots and line plots.
- Provides insights into how well models perform across different segments of the input feature.

#### Category Analyzer (`CategoryAnalyzer`)

- Analyzes model predictions across categorical variables.
- Visualizes distribution of true and predicted values using box plots grouped by categories.
- Helps in understanding how models perform across different categories or classes.

---------------------------------------------------

#### `regress_analytics.EDA.DataDist` class

The `DataDist` class in `regress_analytics.EDA` facilitates visualizing the distribution of numerical and categorical features across multiple datasets. It generates histograms, density plots (PDFs), and box plots to compare feature distributions, aiding in understanding the spread and variability of data within different datasets.

#### Method: `plot`

##### Parameters:

- `data_sets` (list of `pd.DataFrame`): List of datasets to visualize.
- `data_set_names` (list of `str`): Names of the datasets provided in `data_sets`.
- `numerical_feature_names` (list of `str`): Names of numerical features to plot.
- `categorical_feature_names` (list of `str`): Names of categorical features to plot.
- `figsize` (tuple, optional): Figure size for the plots. Default is `(9, 11)`.

##### Returns:

- `None`

###### Example Usage:

```python
from regress_analytics.EDA import DataDist

# Assuming data and feature names are defined
data_sets = [train_data, val_data, test_data]
data_set_names = ["train_data", "val_data", "test_data"]
numerical_feature_names = ["feature1", "feature2"]
categorical_feature_names = ["category1", "category2"]

dist_plotter = DataDist()
dist_plotter.plot(data_sets, data_set_names, numerical_feature_names, categorical_feature_names)
```
---------------------------------------------------
#### `regress_analytics.EDA.CorrelationMap` class

The `CorrelationMap` class in `regress_analytics.EDA`provides functionality to plot a heatmap of the correlation matrix for specified columns in a dataset.

#### Method: `plot`

##### Parameters:

- `data` (`pd.DataFrame`): The dataset containing the data.
- `col_names` (list of `str`): List of column names to include in the correlation matrix.
- `figsize` (tuple, optional): Size of the figure for the heatmap (default is `(8, 8)`).

##### Returns:

- `None`

##### Example Usage:

```python
import pandas as pd
from regress_analytics.EDA import CorrelationMap

# Assuming data and column names are defined
data = pd.read_csv('train_data.csv')
col_names = ['feature1', 'feature2', 'feature3']

corr_plotter = CorrelationMap()
corr_plotter.plot(data, col_names)
```
---------------------------------------------------
#### `regress_analytics.model_performance_analysis.PredsVsTrue` class

The `PredsVsTrue` class in `regress_analytics.model_performance_analysis` provides functionality to plot true values against predicted values for multiple models. Each model's predictions are visualized with a fitted line and scatter plot, and the unity line (y=x) is shown for reference.

#### Method: `plot`

##### Parameters:

- `y_true` (`np.array`): The true values.
- `y_pred` (Union[`np.array`, list[`np.array`]]): The predicted values. Can be a single array or a list of arrays.
- `model_names` (list of `str`, optional): The names of the models. Required if `y_pred` is a list of arrays.
- `figsize` (tuple, optional): The size of the figure (default is `(8, 6)`).

##### Returns:

- `None`

##### Raises:

- `ValueError`: If `model_names` is `None` or its length does not match `y_pred` length when `y_pred` is a list.

##### Example Usage:

```python
import numpy as np
from regress_analytics.model_performance_analysis import PredsVsTrue

# Example data
y_true = np.array([10, 20, 30, 40, 50])
y_pred_model1 = np.array([12, 22, 29, 41, 52])
y_pred_model2 = np.array([11, 21, 31, 39, 48])
model_names = ["Model 1", "Model 2"]

pred_plotter = PredsVsTrue()
pred_plotter.plot(
    y_true, 
    [y_pred_model1, y_pred_model2],
    model_names)
```
---------------------------------------------------
#### `regress_analytics.model_performance_analysis.SensitivityTest` class

The `SensitivityTest` class in `regress_analytics.model_performance_analysis` provides functionality to plot sensitivity test results for multiple models based on varying a specific feature(`feature_col_name`). The sensitivity test involves predicting with different values of the specified feature and visualizing the average predictions of each model across the feature range.

#### Method: `plot`

##### Parameters:

- `features` (`pd.DataFrame`): The input features for making predictions.
- `feature_col_name` (`str`): The name of the feature column to vary for the sensitivity test.
- `models` (list of `object`): The list of trained model objects.
- `model_names` (list of `str`): The names of the models.
- `model_features` (list of lists): The features used by each model.
- `multi_output_model` (list of `bool`): Indicates if the models are multi-output models.
- `index_to_use` (list of `int`, optional): The index to use for multi-output models.
- `acceptable_feature_range` (`tuple`, optional): The range of feature values to test (default is `None`). In case of `None`, it will use min and max of the feature in the `features`.
- `num_samples` (`int`, optional): The number of samples to generate within the feature range (default is `100`).
- `figsize` (`tuple`, optional): The size of the figure (default is `(8, 6)`).

##### Returns:

- `None`

##### Raises:

- `ValueError`: If `index_to_use` is `None` when there is at least one multi-output model or is `None` for any multi-output model.

##### Example Usage:

```python
import pandas as pd
import numpy as np
from regress_analytics.model_performance_analysis import SensitivityTest

# Example data and models
features = pd.DataFrame({
    'feature1': np.random.rand(100),
    'feature2': np.random.rand(100)
})
# Assuming these are your trained model objects
models = [model1, model2]  
model_names = ['Model 1', 'Model 2']
model_features = [['feature1', 'feature2'], ['feature1']]
multi_output_model = [False, True]
index_to_use = [None, 1]  # Assuming Model 2 is multi-output and we use index 1
acceptable_feature_range = None
num_samples = 50

sensitivity_test = SensitivityTest()
sensitivity_test.plot(
    features =features,
    feature_col_name = "feature1",
    models=  models,
    model_names = model_names,
    model_features = model_features,
    multi_output_model= multi_output_model,
    index_to_use = index_to_use,
    acceptable_feature_range = None,
    num_samples= num_samples,
    )
```
---------------------------------------------------
#### `regress_analytics.model_performance_analysis.BinAnalyzer` class

The `BinAnalyzer` class in `regress_analytics.model_performance_analysis` provides functionality to plot true values and model predictions across different bins of a specified numerical feature/target. It supports binning the data using either equal width or equal frequency methods and allows aggregation within bins using mean or median. It visualizes the aggregated true and predicted values for comparison.

#### Method: `plot`

##### Parameters:

- `data` (`pd.DataFrame`): The input data containing the features and true output values.
- `feature_col_name` (`str`): The name of the numerical feature column to bin and analyze.
- `output_col_name` (`str`): The name of the output column with the true values.
- `models` (list of `object`): A list of trained model objects to use for predictions.
- `model_names` (list of `str`): A list of names for the models.
- `model_features` (list of lists): A list of lists, where each sublist contains the feature names used by the corresponding model.
- `multi_output_model` (list of `bool`): A list indicating whether each model has multiple outputs.
- `index_to_use` (list of `int`, optional): A list of indices specifying which output to use for multi-output models. Defaults to `None`.
- `binning_method` (`str`, optional): The method used for binning the numerical feature ('equal_width' or 'equal_frequency'). Defaults to 'equal_width'.
- `num_bins` (`int`, optional): The number of bins to create if using 'equal_width' binning method. Defaults to `50`.
- `aggregate_func` (`str`, optional): The aggregation function to use for aggregating data within each bin ('mean' or 'median'). Defaults to 'mean'.
- `figsize` (`tuple`, optional): The size of the figure for the plot (default is `(8, 6)`).

##### Returns:

- `aggregated_data_based_on_bins` (`pd.DataFrame`): Aggregated data based on the bins.

##### Raises:

- `ValueError`: If `binning_method` is not 'equal_width' or 'equal_frequency'.

##### Example Usage:

```python
import pandas as pd
import numpy as np
from regress_analytics.model_performance_analysis import BinAnalyzer

# Example data and models
data = pd.DataFrame({
    'feature1': np.random.rand(100),
    'feature2': np.random.rand(100),
    'output': np.random.rand(100)
})
models = [model1, model2]  # Assuming these are your trained model objects
model_names = ['Model 1', 'Model 2']
model_features = [['feature1', 'feature2'], ['feature1']]
multi_output_model = [False, False]
index_to_use = None  # Assuming both models only predict one target

bin_analyzer = BinAnalyzer()
aggregated_data = bin_analyzer.plot(
    data = data,
    feature_col_name=  'feature1',
    output_col_name = 'output',
    models=  models,
    model_names = model_names,
    model_features = model_features,
    multi_output_model = multi_output_model,
    index_to_use = None,
    binning_method = "equal_width",
    num_bins = 50,
    aggregate_func="mean"
    )
```
---------------------------------------------------
#### `regress_analytics.model_performance_analysis.CategoryAnalyzer` class

The `CategoryAnalyzer` class in `regress_analytics.model_performance_analysis` provides functionality to plot true values and model predictions across different categories of a categorical feature.It visualizes the distribution of true and predicted values using box plots for comparison.

#### Method: `plot`

##### Parameters:

- `data` (`pd.DataFrame`): The input data containing the features and true output values.
- `feature_col_name` (`str`): The name of the categorical feature column to analyze.
- `output_col_name` (`str`): The name of the output column with the true values.
- `models` (list of `object`): A list of trained model objects to use for predictions.
- `model_names` (list of `str`): A list of names for the models.
- `model_features` (list of lists): A list of lists, where each sublist contains the feature names used by the corresponding model.
- `multi_output_model` (list of `bool`): A list indicating whether each model has multiple outputs.
- `index_to_use` (list of `int`, optional): A list of indices specifying which output to use for multi-output models. Defaults to `None`.
- `figsize` (`tuple`, optional): The size of the figure for the plot (default is `(8, 12)`).

##### Raises:

- `ValueError`: If `index_to_use` is `None` when any model in `multi_output_model` is `True`.

##### Example Usage:

```python
import pandas as pd
from regress_analytics.model_performance_analysis import CategoryAnalyzer

# Example data and models
data = pd.DataFrame({
    'category_feature': ['A', 'B', 'C', 'A', 'B', 'C'],
    'output': [1.0, 2.0, 3.0, 1.5, 2.5, 3.5]
})
models = [model1, model2]  # Assuming these are your trained model objects
model_names = ['Model 1', 'Model 2']
model_features = [['category_feature'], ['category_feature']]
multi_output_model = [False, False]
index_to_use = None  # Assuming None of the models is multi-output model

category_analyzer = CategoryAnalyzer()
category_analyzer.plot(
    data = data, 
    feature_col_name = 'category_feature', 
    output_col_name = 'output',
    models = models, 
    model_names = model_names, 
    model_features = model_features,
    multi_output_model=multi_output_model, 
    index_to_use = index_to_use
)
```

