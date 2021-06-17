from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns=[
	path('', views.panel, name='panel'),
	path('logs/', views.logs, name='logs'),
	path('reports/', views.reports, name='reports'),
	path('suggestions/', views.suggestions, name='suggestions')
]
