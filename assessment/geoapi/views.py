from django.shortcuts import render
from .models import GeoModel
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import GeoSerializer
from shapely import wkt



def ftype_to_lookup(ftype):
    """Map field type to lookup"""
    if ftype in {
            'DateTimeField',
            'DateField',
            'FloatField',
            'IntegerField',
            'SmallIntegerField',
            'BigIntegerField',
            'DecimalField'
    }:
        return ['exact', 'gt', 'gte', 'lt', 'lte']
    elif ftype != 'PointField':
        return ['exact']
    return []


def get_lookups(model):
    return {
        f.name: ftype_to_lookup(f.get_internal_type())
        for f in model._meta.concrete_fields
    }

def get_nested_lookups(related_name, nested_model):
    return {
        f"{related_name}__{f.name}": ftype_to_lookup(f.get_internal_type())
        for f in nested_model._meta.concrete_fields
    }

# Generic filtering
def make_model_filter(model, *nested, exclude=[], **extra):
    """Generate FilterSet on-the-fly"
    Args:
    - model (object)
    - nested (list of tuples: ('related_name,' model object)):
        Creates filters for nested models fields.
    - exclude (list of str): Any fields you wish to exclude from filter
    - extra (dict): Any additional lookups
    """

    lookups = get_lookups(model)
    for nested_model in nested:
        related_name = nested_model[0]
        nested_model = nested_model[1]
        nested_model_lookups = get_nested_lookups(related_name, nested_model)
        lookups = {** lookups, ** nested_model_lookups, ** extra}
    for f in exclude:
        lookups.pop(f)
    ordering_fields = list(lookups.keys())
    ordering = OrderingFilter(fields=ordering_fields)
    meta = type('Meta', (), {'model': model, 'fields': lookups})
    filterset = type(
        f"{model._meta.object_name}Filter",
        (FilterSet,),
        {'ordering': ordering, 'Meta': meta}
    )
    return filterset



class APIRoot(APIView):
    name = 'API Root'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            'geo': reverse('geo-list', request=request),
        })



class GeoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = GeoModel.objects.all().order_by('timestamp')
    serializer_class = GeoSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filterset_class = make_model_filter(Gps , exclude=['rit'])
