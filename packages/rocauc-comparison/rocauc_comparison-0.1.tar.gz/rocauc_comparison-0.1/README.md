# rocauc_comparison

`rocauc_comparison` is a Python package designed for comparing Receiver Operating Characteristic (ROC) Area Under the Curve (AUC) scores using DeLong's method. This package provides a statistical test to determine if the difference between two ROC AUC scores is statistically significant.

## Features

- **Compare Two ROC AUC Scores**: Use DeLong's test to compare the ROC AUC scores of two models.
- **Calculate AUC Variance**: Compute the variance of a single ROC AUC score using DeLong's method.
- **Fast and Efficient**: Implemented with optimized numpy operations for efficient computation.

## Installation

You can install the package using `pip`:

```sh
pip install rocauc_comparison

import numpy as np
from rocauc_comparison import delong_roc_test

# Ground truth labels
ground_truth = np.array([0, 1, 0, 1, 0, 1])

# Predictions from the first model
predictions_one = np.array([0.1, 0.4, 0.35, 0.8, 0.5, 0.9])

# Predictions from the second model
predictions_two = np.array([0.05, 0.45, 0.3, 0.7, 0.6, 0.85])

# Calculate the p-value for the difference in AUC
p_value = delong_roc_test(ground_truth, predictions_one, predictions_two)
print(f"p-value: {p_value}")
