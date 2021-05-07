from .forms import BaseDataInputForm
from .models import BaseData, ProjectionIn2D

from django.views.generic import TemplateView, FormView

import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import plotly.express as px
from plotly.offline import plot


#############################################################################################################################
#############################################################################################################################
# Part 1 : Data processing 
#############################################################################################################################
#############################################################################################################################

class ClusterBaseData:
    """
    First step is to read in a dataset which is achieved by this class
    self.load_data uses content of form to create url => uses base_data(url) to get dataset => uses data_table to transform the data
    self. base_data uses the url from the form. Reads the data from the database.
    If no Pickle object is present in the database to the given url.
    Is being used by self.data_table and DimRed.projection_in_2D
    self.data_table uses base_data, provides list for templates:
    Takes the pd_frame from base_data and transforms it to a list, which can be read by the template and diplayed as a Data Table
    """

    def load_data(self, form):
        url = form.cleaned_data["base_data"]
        data = self.base_data(url)
        samples, parameters = self.data_table(data)
        return samples, parameters

    def base_data(self, url):
        try:
            base_data_obj = BaseData.objects.get(url=url)
        except:
            base_data = pd.read_csv(url)
            base_data_obj = BaseData()
            base_data_obj.data = base_data
            base_data_obj.url = url
            base_data_obj.save()
        pd_frame = base_data_obj.data
        return pd_frame

    def data_table(self, pd_frame):
        parameters = []
        for col in pd_frame.columns:
            parameters.append(col)
        pd_frame_dict = pd_frame.to_dict()

        samples = []
        for i in range(len(pd_frame.head())):
            sample = [i]
            for key in pd_frame_dict:
                sample.append(pd_frame_dict[key][i])
            samples.append(sample)
        return samples, parameters


class DimReduction(ClusterBaseData):
    """
    Receives multidimensional data in pd_frame from ClusterBaseData.base_data
    Transforms the pd_frame into a 2D table and a 2D plot via self.make_pca and self.make_plot and respectively
    Those methods will be called in self.project_in_2D and store the 2D table and 2D plot in the database as a ProjectionIn2D object
    Depending on the parameter classified either base_data or kmeans id projected into 2D and plotted.
    Returns Plot
    """

    def make_plot(self, original_data, pca_table, classified=False):
        hover = dict()
        for col in original_data.columns:
            hover[col] = original_data[col]
        if classified == False:
            fig = px.scatter(pca_table, x="C1", y="C2", hover_data=hover)
        elif classified == True:
            fig = px.scatter(
                pca_table, x="C1", y="C2", color="classification", hover_data=hover
            )
        fig.update_layout(showlegend=False)
        pca_plot = plot(fig, output_type="div")
        return pca_plot

    def make_pca(self, pd_frame, classified=False):
        pd_frame_std = StandardScaler().fit_transform(pd_frame)
        # Project multidimensional data to 2D via Principal Component Analysis
        if classified == False:
            components = PCA(n_components=2).fit_transform(pd_frame_std)
            pca_table = pd.DataFrame(data=components, columns=["C1", "C2"])
        elif classified == True:
            values, classification = self.split(pd_frame_std)
            components = PCA(n_components=2).fit_transform(values, classification)
            pca_table = pd.DataFrame(data=components, columns=["C1", "C2"])
            pca_table = pd.concat([pca_table, pd_frame[["classification"]]], axis=1)
        return pca_table

    def split(self, pd_frame):
        features = [col for col in pd_frame.columns]
        features.remove("classification")
        X = pd_frame.loc[:, features].values
        y = pd_frame["classification"]
        return X, y

    def project_in_2D(
        self,
        form,
        kmeans=pd.DataFrame(columns=["C1", "C2", "classification"]),
        classified=False,
    ):
        url = form.cleaned_data["base_data"]
        try:
            # Check whether the projection (identified by url and the kmeans analysis) already exist in the database
            PI2D = ProjectionIn2D.objects.get(url=url, kmeans=kmeans)
            pca_plot = PI2D.plot
            if classified == False:
                pca_table = PI2D.data
            else:
                pca_table = PI2D.kmeans
        except:

            base_data_table = BaseData.objects.get(url=url)
            PI2D = ProjectionIn2D()
            original_data = self.base_data(url)
            pca_table = self.make_pca(original_data)
            if classified == False:
                pca_plot = self.make_plot(original_data, pca_table)
            else:
                pca_plot = self.make_plot(original_data, kmeans, classified=True)
            PI2D.kmeans = kmeans

            # Create an object and save it to in database
            PI2D.url, PI2D.plot, PI2D.data, PI2D.base_data = (
                url,
                pca_plot,
                pca_table,
                base_data_table,
            )
            PI2D.save()
        if classified == False:
            return pca_plot, pca_table
        else:
            return pca_plot, kmeans


class Cluster(DimReduction):
    """
    self.kmeans_analysis receives url and expected clusters from the form
    It loads the bsae_data projects it in 2D and calculates the classification via sklearn.cluster.Kmeans
    """

    def kmeans_analysis(self, form, number_of_expected_clusters):
        url = form.cleaned_data["base_data"]
        pd_frame = self.base_data(url)
        pca_table = self.make_pca(pd_frame, classified=False)

        km = KMeans(
            n_clusters=number_of_expected_clusters,
            init="random",
            max_iter=300,
            tol=1e-04,
            random_state=0,
        )
        classification = km.fit_predict(pca_table)
        classification = pd.DataFrame(classification, columns=["classification"])
        km_table = pd.concat([pca_table, classification], axis=1)
        return km_table

    def plot_clusters(self, form, number_of_expected_clusters):
        km_table = self.kmeans_analysis(form, number_of_expected_clusters)
        return self.project_in_2D(form, km_table, classified=True)



#############################################################################################################################
#############################################################################################################################
# Part 2 : The actual views
#############################################################################################################################
#############################################################################################################################

class IndexView(TemplateView, FormView, Cluster):
    """
    Uses BaseDataInputForm to create the object form, which contains the url
    Applies the url to ClusterBaseData.loadData, from which it receives two lists: samples and parameters
    Sends samples, parameters to index.html with which the templete data_table.html is supplied to display the head of the data
    Applies DimReduction.project_in_2D to receive the projection_plot.
    """

    template_name = "index.html"
    form_class = BaseDataInputForm

    def form_valid(self, form):
        context = self.get_context_data()
        (samples, parameters) = self.load_data(form)
        projection_plot, projection_data_table = self.project_in_2D(form)

        url = form.cleaned_data["base_data"]

        context["projection_plot"] = projection_plot
        context["projection_data_table"] = projection_data_table
        context["samples"] = samples
        context["parameters"] = parameters

        # preserve url for ResultsView
        context["url"] = url

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["error"] = None
        return context


class ResultsView(IndexView):
    """
    Uses BaseDataInputForm to create the object form, which contains the url and the number_of_expected_clusters
    Applies the both parameters to make a kmeams_analysis via Cluster.plot_clusters, which provides the  kmeans_plot, kmeans_data_table
    Sends samples, parameters to index.html with which the templete data_table.html is supplied to display the head of the original_data with the classification
    Saves the rsult as csv
    """

    def form_valid(self, form):
        context = self.get_context_data()

        number_of_expected_clusters = form.cleaned_data["number_of_expected_clusters"]
        kmeans_plot, kmeans_data_table = self.plot_clusters(
            form, number_of_expected_clusters
        )

        # Supply original datatable with classification
        url = form.cleaned_data["base_data"]
        original_data = self.base_data(url)
        classification = kmeans_data_table["classification"]
        original_data_classified = pd.concat([original_data, classification], axis=1)
        samples, parameters = self.data_table(original_data_classified)

        context["kmeans_plot"] = kmeans_plot
        context["kmeans_data_table"] = kmeans_data_table
        context["samples"] = samples
        context["parameters"] = parameters
        context["url"] = url

        # Save the classified original data as csv
        original_data_classified.to_csv("./data/clustered data.csv")

        return self.render_to_response(context)
