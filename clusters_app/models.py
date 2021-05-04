from django.db import models

from django.db import models
from django.conf import settings
from picklefield.fields import PickledObjectField
import numpy


class BaseData(models.Model):
    url = models.CharField(max_length=30, default="baseData")
    data = PickledObjectField(default="SOME STRING")


class ProjectionIn2D(models.Model):
    url = models.CharField(max_length=30, default="URL")
    plot = PickledObjectField()
    data = PickledObjectField(default="SOME STRING")
    kmeans = PickledObjectField(default="SOME STRING", null=True, blank=True)
    base_data = models.ForeignKey(
        BaseData, on_delete=models.CASCADE, related_name="ProjectionIn2D"
    )
