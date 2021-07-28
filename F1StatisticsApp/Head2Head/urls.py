from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('Viewdrivers', views.drivers),
    path('', views.comparedrivers),
    path('drivers', views.comparedrivers),
    path('teams',views.compareteams),
    path('Load',views.Load),
    path('LoaddataIntoDatabase', views.LoadAllNewData),
]