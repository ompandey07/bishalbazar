from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from adminview.models import *

def index_view(request):
    banners = CompanyBanner.objects.prefetch_related('images').first()
    news = CompanyNews.objects.all().order_by('-created_at')[:5]
    downloads = CompanyDownloads.objects.all().order_by('-created_at')[:5]
    gallery = CompanyGallery.objects.all().order_by('-created_at')[:6]
    bod_members = CompanyBOD.objects.all().order_by('-created_at')[:2]
    
    context = {
        'banners': banners,
        'news': news,
        'downloads': downloads,
        'gallery': gallery,
        'bod_members': bod_members,
    }
    return render(request, 'core/index.html', context)

def news_list_view(request):
    news = CompanyNews.objects.all().order_by('-created_at')
    context = {
        'news': news,
    }
    return render(request, 'core/news.html', context)

def news_detail_view(request, slug):
    news = get_object_or_404(CompanyNews, slug=slug)
    related_news = CompanyNews.objects.exclude(slug=slug).order_by('-created_at')[:3]
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'core/news_detail.html', context)

def bod_view(request):
    bod_members = CompanyBOD.objects.all().order_by('-created_at')
    context = {
        'bod_members': bod_members,
    }
    return render(request, 'core/bod.html', context)

def gallery_view(request):
    gallery_items = CompanyGallery.objects.all().order_by('-created_at')
    context = {
        'gallery_items': gallery_items,
    }
    return render(request, 'core/gallery.html', context)

def report_view(request):
    downloads = CompanyDownloads.objects.all().order_by('-created_at')
    context = {
        'downloads': downloads,
    }
    return render(request, 'core/report.html', context)

def contact_view(request):
    return render(request, 'core/contact.html')



def staff_view(request):
    employees = CompanyEmployee.objects.all().order_by('-created_at')
    context = {
        'employees': employees,
        'total_employees': employees.count(),
    }
    return render(request, 'core/staff.html', context)