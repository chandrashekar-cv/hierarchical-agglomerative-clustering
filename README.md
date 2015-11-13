# hierarchical-agglomerative-clustering
hierarchical clustering of data points.
Script takes 2 arguments.   
1. Number of desired clusters. Euclidean distance is used to calculate the distance between cluster centers. Cluster center is calculated by taking the mean of all points in a cluster for each dimension.   
2. dataset with comma seperated points of k dimension(k-columns). K+1 column contains the tag or name of the actual cluster to which the data point belongs to. This is useful to calculate the precission and recall of clustering. How ever if you do not wish to verify the clustering precission and recall, then comment <code>clustering.calculatePrecissionRecall()</code> statement in main.   
   
