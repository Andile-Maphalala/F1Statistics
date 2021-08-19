from django.urls import path,re_path
from django.contrib import admin
from . import views
from Head2Head.views import GetGraphData

urlpatterns = [
    path('index', views.index, name='index'),
    path('x', views.drivers),
    path('', views.comparedrivers),
    path('drivers', views.comparedrivers),
    path('teams',views.compareteams),
    path('load',views.Load, name='load'),
    path('LoadData', views.LoadAllNewData),
    path('DelSpec', views.DeleteSpecifiedData),

    # path('del', views.DeleteQauly),

    path('admin/', views.FakeAdmin),
    # path('graph', views.Graphs),
    # re_path(r'^api/$', GetGraphData, name='api-data'),


]