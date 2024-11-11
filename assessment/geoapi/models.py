from django.contrib.gis.db import models

class GeoModel(models.Model):
    location = models.PointField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
