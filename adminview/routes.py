from django.urls import path
from . import views

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────
    path('login/',     views.admin_login,     name='admin_login'),
    path('logout/',    views.admin_logout,    name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # ── Downloads ─────────────────────────────────────────────
    path('downloads/',              views.downloads_list,   name='admin_downloads'),
    path('downloads/create/',       views.downloads_create, name='admin_downloads_create'),
    path('downloads/<int:pk>/update/', views.downloads_update, name='admin_downloads_update'),
    path('downloads/<int:pk>/delete/', views.downloads_delete, name='admin_downloads_delete'),

    # ── News ──────────────────────────────────────────────────
    path('news/',              views.news_list,   name='admin_news'),
    path('news/create/',       views.news_create, name='admin_news_create'),
    path('news/<int:pk>/update/', views.news_update, name='admin_news_update'),
    path('news/<int:pk>/delete/', views.news_delete, name='admin_news_delete'),

    # ── Gallery ───────────────────────────────────────────────
    path('gallery/',              views.gallery_list,   name='admin_gallery'),
    path('gallery/create/',       views.gallery_create, name='admin_gallery_create'),
    path('gallery/<int:pk>/update/', views.gallery_update, name='admin_gallery_update'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='admin_gallery_delete'),

    # ── Banner ────────────────────────────────────────────────
    path('banner/',              views.banner_list,   name='admin_banner'),
    path('banner/create/',       views.banner_create, name='admin_banner_create'),
    path('banner/<int:pk>/update/', views.banner_update, name='admin_banner_update'),
    path('banner/<int:pk>/delete/', views.banner_delete, name='admin_banner_delete'),
    path('banner/image/create/', views.banner_image_create, name='admin_banner_image_create'),
    path('banner/image/<int:pk>/delete/',        views.banner_image_delete, name='admin_banner_image_delete'),

    # ── BOD ───────────────────────────────────────────────────
    path('bod/',              views.bod_list,   name='admin_bod'),
    path('bod/create/',       views.bod_create, name='admin_bod_create'),
    path('bod/<int:pk>/update/', views.bod_update, name='admin_bod_update'),
    path('bod/<int:pk>/delete/', views.bod_delete, name='admin_bod_delete'),

    # ── Employee ──────────────────────────────────────────────
    path('employee/',              views.employee_list,   name='admin_employee'),
    path('employee/create/',       views.employee_create, name='admin_employee_create'),
    path('employee/<int:pk>/update/', views.employee_update, name='admin_employee_update'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='admin_employee_delete'),
]