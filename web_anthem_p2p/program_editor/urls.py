from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='editor-home'),
    path('verify/', views.verify)
]


