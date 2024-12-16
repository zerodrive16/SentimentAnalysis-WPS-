from django.urls import path
from . import views
from .views import PostAcceptance

urlpatterns = [
    # Web Application
    path('', views.home, name='home'),
    # Retrieval dataset from Python to JavaScript
    path('dataset/', views.dataset, name='dataset'),
    # Send JavaScript Post request (data) back to Python Script
    path("api/", PostAcceptance.as_view(), name='post-comment'),
]

