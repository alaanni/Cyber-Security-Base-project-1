from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("signin/", views.SignIn.as_view(), name="signin"),
    
]