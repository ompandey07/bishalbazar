from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('news/', views.news_list_view, name='news'),
    path('news/<slug:slug>/', views.news_detail_view, name='news_detail'),
    path('board-of-directors/', views.bod_view, name='bod'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('reports/', views.report_view, name='report'),
    path('contact/', views.contact_view, name='contact'),
    path('staff/', views.staff_view, name='staff'),
]