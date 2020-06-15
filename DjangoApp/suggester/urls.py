from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='suggester-home'),
    path('ajax/query_suggestion/', views.query_suggestion, name = 'query_suggestion'),
    path('ajax/save_suggestion/', views.save_suggestion, name = 'save_suggestion'),
]
