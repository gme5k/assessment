#!/usr/bin/env python3
from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


from . import views

# urlpatterns = [
#     path('post/', views.post_view, name='post'),
#     path('get/',  views.get_view, name='get

geo_list = views.GeoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = format_suffix_patterns([
    path('/', views.APIRoot.as_view(), name=views.APIRoot.name),
    path('/geo/', geo_list, name='geo-list'
    ),
])
