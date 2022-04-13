from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('create/',views.createproject, name="create-project"),
    path('project/<str:pk>/', views.project1, name="project"),
    path('update-project/<str:pk>/', views.updateproject, name="update-project"),
    path('delete-project/<str:pk>/', views.deleteproject, name="delete-project"),
] 