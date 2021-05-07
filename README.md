# machine_learning_clusters

<p align="center">
  <img width="700"src="snapshots/abstract.png">
</p>

## Motivation
Visualize and classify complex multidimensional datasets with only two clicks.  The app can be used in combination with my **MyDirtyDjango/DjangoMachineLearning/** repository


## How to use it
Load unclassified datasets from your local machine or remote resources via url. 

<p align="center">
  <img src="snapshots/load_data.png" width="800" />
</p>

The dataset is then projected in two dimensions via Principal Component Analysis (**PCA**). A plotly express scatter plot will be displayed as in the following snapshot. Underneath you find the head of the data table you just loaded. Type the number of clusters (or increment by arrows) that you expect, meaning how many clusters do you see in the plot. Submit again.
<p align="center">
  <img src="snapshots/projection.png" width="800" /> 
</p>
Datapoints are now assigned to clusters in both, the plot and the data table underneath. The classification has taken place via the k_Means_Algorithm. The classified multidimensional data locally stored in the data folder for further processing. E.g. classify new data with my supervised machine learning application **DjangoMachineLearning**.

<p align="center">
  <img src="snapshots/clusters.png" width="800" />
</p>
Test the application with the iris data under data/iris-test-data.csv




#### Get a feeling for the meaning of the results with createTestData.py

## Details of the code in this project and lessons to be learned
### Crucial logics

###### Note: the URls of the model data and teh test data are also passed from view to view by meeans of hidden input forms such as the following

### How to get Plotly graphs from the views.py to a template 





### models.py

###### Note: The objects in the database are mainly identified by the url of the csv. Any modification in the original csv file (such as additional or corrected data) will thus only be recognized if the url is changed as well. 
Pandas Frames and plots are stored as PickleFireldobjects. 

#### deficites of the code


#### yet to be done








