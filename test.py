import numpy as np
from permetrics import ClusteringMetric

## For integer labels or categorical labels
data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]) # All bacteria positions
y_pred = np.array([0, 0, 1, 1, 1]) #the centroid label

cm = ClusteringMetric(X=data, y_pred=y_pred)

print(cm.density_based_clustering_validation_index())
print(cm.DBCVI())