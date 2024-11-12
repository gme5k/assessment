from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
from .models import GeoModel
import json
import logging
# from shapely.geometry import Point

class GeoSerializer(serializers.ModelSerializer):

    def create(self, data):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
        logger.info(f'DATA: {data}')
        # data = self.validate(data)

        location=GEOSGeometry(f'SRID=4326;POINT({data["lon"]}  {data["lat"]})')
        geo = GeoModel(location=location)
        geo.save()
        return geo



    class Meta:
        model = GeoModel
        fields = ['location', 'timestamp']
