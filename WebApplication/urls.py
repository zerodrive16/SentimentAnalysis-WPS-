from django.urls import path
from . import views

urlpatterns = [
    # Web Application
    path('', views.home, name='home'),
    # Execute Machine Learning
    #path('regex', views.regex, name='regex'),
    path('backend', views.runMLScript, name='runMLScript')
]

