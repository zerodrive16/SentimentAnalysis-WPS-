from django.urls import path
from . import views

urlpatterns = [
    # Web Application
    path('', views.home, name='home'),
    # Execute Machine Learning
    path('backend', views.runMLScript, name='runMLScript')
]

