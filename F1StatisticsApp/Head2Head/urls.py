from django.urls import path,re_path
from django.contrib import admin
from . import views
from Head2Head.views import GetGraphData
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index', views.index, name='index'),
    path('x', views.drivers),
    path('', views.comparedrivers),
    path('drivers', views.comparedrivers,name='drivers'),
    path('teams',views.compareteams),
    path('load',views.Load, name='load'),
    path('LoadData', views.LoadAllNewData),
    path('DelSpec', views.DeleteSpecifiedData),
    path('admin/', views.FakeAdmin),
    path('graph', views.Graphs),
    re_path(r'^api/$', GetGraphData, name='api-data'),


    #Gango auth 
    path('login', auth_views.LoginView.as_view(template_name="Head2Head/login.html"),name='login'),
    path('logout', auth_views.LogoutView.as_view(),name='logout'),




]