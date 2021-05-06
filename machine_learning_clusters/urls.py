
from django.contrib import admin
from django.urls import path
import clusters_app.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", clusters_app.views.IndexView.as_view(), name="index"),
    path("results", clusters_app.views.ResultsView.as_view(), name="results"),
]
