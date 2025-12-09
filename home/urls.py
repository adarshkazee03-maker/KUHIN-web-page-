from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('events/', views.events, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('resources/', views.resources, name='resources'),
    path('contact/', views.contact, name='contact'),
]
