from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.global_search, name='global_search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('trending/', views.trending_content, name='trending'),
    path('recommendations/<str:content_type_str>/<int:object_id>/', views.recommendations, name='recommendations'),
    path('api/stats/', views.quick_stats, name='quick_stats'),
]
