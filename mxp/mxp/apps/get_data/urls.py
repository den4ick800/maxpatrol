from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('/get_data',views.index1, name='index1')
]