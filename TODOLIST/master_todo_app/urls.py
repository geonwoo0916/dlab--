from django.urls import path
from . import views

urlpatterns = [
    path('createtodo/', views.createtodo),
    path('', views.index, name='index')
]