# test.py — clustering metric example using permetrics

import numpy as np
from permetrics import ClusteringMetric

# Example 2D positions for a small set of bacteria (x, y coordinates)
data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])

# Predicted cluster labels for each data point (integer labels)
y_pred = np.array([0, 0, 1, 1, 1])

# Initialize the clustering metric evaluator
cm = ClusteringMetric(X=data, y_pred=y_pred)

# Print commonly used density-based clustering validation scores
print("Density-based clustering validation index:", cm.density_based_clustering_validation_index())
print("DBCV:", cm.DBCVI())