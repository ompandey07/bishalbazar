from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import (
    CompanyDownloads, CompanyNews, CompanyGallery,
    CompanyBanner, BannerImage, CompanyBOD, CompanyEmployee
)

# ─── Admin Credentials ──────────────────────────────────────────────────────
ADMIN_CREDENTIALS = {
    'full_name': 'Bishal Bazar',
    'email': 'bishalbazar@admin.com',
    'password': 'admin@1200'
}


def admin_required(view_func):
    """Decorator: redirect to login if not authenticated."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401) \
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' \
                else redirect('admin_login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def _admin_context(request):
    return {'admin_name': request.session.get('admin_full_name', 'Admin')}


# ─── Auth ───────────────────────────────────────────────────────────────────

def admin_login(request):
    if request.session.get('admin_logged_in'):
        return redirect('admin_dashboard')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if email == ADMIN_CREDENTIALS['email'] and password == ADMIN_CREDENTIALS['password']:
            request.session['admin_logged_in'] = True
            request.session['admin_full_name'] = ADMIN_CREDENTIALS['full_name']
            request.session['admin_email'] = ADMIN_CREDENTIALS['email']
            return JsonResponse({'success': True, 'redirect': '/admin/dashboard/'}) \
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' \
                else redirect('admin_dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'इमेल वा पासवर्ड गलत छ!'})
            messages.error(request, 'इमेल वा पासवर्ड गलत छ!')
    return render(request, 'admin/login.html')


def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


@admin_required
def admin_dashboard(request):
    downloads_count = CompanyDownloads.objects.count()
    news_count = CompanyNews.objects.count()
    gallery_count = CompanyGallery.objects.count()
    banners_count = CompanyBanner.objects.count()
    bod_count = CompanyBOD.objects.count()
    employee_count = CompanyEmployee.objects.count()
    total_records = downloads_count + news_count + gallery_count + banners_count + bod_count + employee_count
    context = {
        **_admin_context(request),
        'admin_email': request.session.get('admin_email', ''),
        'downloads_count': downloads_count,
        'news_count': news_count,
        'gallery_count': gallery_count,
        'banners_count': banners_count,
        'bod_count': bod_count,
        'employee_count': employee_count,
        'total_records': total_records,
    }
    return render(request, 'admin/dashboard.html', context)


# ─── Downloads ──────────────────────────────────────────────────────────────

@admin_required
def downloads_list(request):
    items = CompanyDownloads.objects.all().order_by('-created_at')
    return render(request, 'admin/downloads.html', {'items': items, **_admin_context(request)})


@admin_required
@require_POST
def downloads_create(request):
    try:
        title = request.POST.get('download_title', '').strip()
        file = request.FILES.get('download_file')
        if not title:
            return JsonResponse({'success': False, 'message': 'शीर्षक आवश्यक छ!'})
        if not file:
            return JsonResponse({'success': False, 'message': 'फाइल आवश्यक छ!'})
        obj = CompanyDownloads(download_title=title, download_file=file)
        obj.save()
        return JsonResponse({'success': True, 'message': 'डाउनलोड सफलतापूर्वक थपियो!',
                             'id': obj.id, 'title': obj.download_title,
                             'file_url': obj.download_file.url,
                             'created_at': obj.created_at.strftime('%Y %b %d, %H:%M')})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def downloads_update(request, pk):
    try:
        obj = get_object_or_404(CompanyDownloads, pk=pk)
        title = request.POST.get('download_title', '').strip()
        file = request.FILES.get('download_file')
        if not title:
            return JsonResponse({'success': False, 'message': 'शीर्षक आवश्यक छ!'})
        obj.download_title = title
        if file:
            obj.download_file = file
        obj.save()
        return JsonResponse({'success': True, 'message': 'डाउनलोड अपडेट भयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def downloads_delete(request, pk):
    try:
        obj = get_object_or_404(CompanyDownloads, pk=pk)
        obj.download_file.delete(save=False)
        obj.delete()
        return JsonResponse({'success': True, 'message': 'डाउनलोड मेटाइयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ─── News ───────────────────────────────────────────────────────────────────

@admin_required
def news_list(request):
    items = CompanyNews.objects.all().order_by('-created_at')
    return render(request, 'admin/news.html', {'items': items, **_admin_context(request)})


@admin_required
@require_POST
def news_create(request):
    try:
        title = request.POST.get('news_title', '').strip()
        desc = request.POST.get('news_descriptions', '').strip()
        image = request.FILES.get('news_image')
        attachment = request.FILES.get('attachments')
        if not title:
            return JsonResponse({'success': False, 'message': 'शीर्षक आवश्यक छ!'})
        obj = CompanyNews(news_title=title, news_descriptions=desc)
        if image:
            obj.news_image = image
        if attachment:
            obj.attachments = attachment
        obj.save()
        return JsonResponse({'success': True, 'message': 'समाचार सफलतापूर्वक थपियो!',
                             'id': obj.id, 'title': obj.news_title,
                             'created_at': obj.created_at.strftime('%Y %b %d')})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def news_update(request, pk):
    try:
        obj = get_object_or_404(CompanyNews, pk=pk)
        title = request.POST.get('news_title', '').strip()
        desc = request.POST.get('news_descriptions', '').strip()
        image = request.FILES.get('news_image')
        attachment = request.FILES.get('attachments')
        if not title:
            return JsonResponse({'success': False, 'message': 'शीर्षक आवश्यक छ!'})
        obj.news_title = title
        obj.news_descriptions = desc
        if image:
            obj.news_image = image
        if attachment:
            obj.attachments = attachment
        obj.save()
        return JsonResponse({'success': True, 'message': 'समाचार अपडेट भयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def news_delete(request, pk):
    try:
        obj = get_object_or_404(CompanyNews, pk=pk)
        if obj.news_image:
            obj.news_image.delete(save=False)
        if obj.attachments:
            obj.attachments.delete(save=False)
        obj.delete()
        return JsonResponse({'success': True, 'message': 'समाचार मेटाइयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ─── Gallery ────────────────────────────────────────────────────────────────

@admin_required
def gallery_list(request):
    items = CompanyGallery.objects.all().order_by('-created_at')
    return render(request, 'admin/gallery.html', {'items': items, **_admin_context(request)})


@admin_required
@require_POST
def gallery_create(request):
    try:
        title = request.POST.get('gallery_title', '').strip()
        image = request.FILES.get('gallery_image')
        if not title:
            return JsonResponse({'success': False, 'message': 'शीर्षक आवश्यक छ!'})
        if not image:
            return JsonResponse({'success': False, 'message': 'तस्वीर आवश्यक छ!'})
        obj = CompanyGallery(gallery_title=title, gallery_image=image)
        obj.save()
        return JsonResponse({'success': True, 'message': 'ग्यालेरी सफलतापूर्वक थपियो!',
                             'id': obj.id, 'title': obj.gallery_title,
                             'image_url': obj.gallery_image.url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def gallery_update(request, pk):
    try:
        obj = get_object_or_404(CompanyGallery, pk=pk)
        title = request.POST.get('gallery_title', '').strip()
        image = request.FILES.get('gallery_image')
        if not title:
            return JsonResponse({'success': False, 'message': 'शीर्षक आवश्यक छ!'})
        obj.gallery_title = title
        if image:
            obj.gallery_image = image
        obj.save()
        return JsonResponse({'success': True, 'message': 'ग्यालेरी अपडेट भयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def gallery_delete(request, pk):
    try:
        obj = get_object_or_404(CompanyGallery, pk=pk)
        if obj.gallery_image:
            obj.gallery_image.delete(save=False)
        obj.delete()
        return JsonResponse({'success': True, 'message': 'ग्यालेरी मेटाइयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ─── Banner ─────────────────────────────────────────────────────────────────

@admin_required
def banner_list(request):
    banners = CompanyBanner.objects.prefetch_related('images').all().order_by('-created_at')
    return render(request, 'admin/banner.html', {'banners': banners, **_admin_context(request)})


@admin_required
@require_POST
def banner_create(request):
    try:
        name = request.POST.get('banner_name', '').strip()
        link_url = request.POST.get('banner_link_url', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        if not name:
            return JsonResponse({'success': False, 'message': 'ब्यानरको नाम आवश्यक छ!'})
        obj = CompanyBanner(banner_name=name, banner_link_url=link_url or None, is_active=is_active)
        obj.save()
        return JsonResponse({'success': True, 'message': 'ब्यानर सफलतापूर्वक थपियो!',
                             'id': obj.id, 'name': obj.banner_name})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def banner_update(request, pk):
    try:
        obj = get_object_or_404(CompanyBanner, pk=pk)
        name = request.POST.get('banner_name', '').strip()
        link_url = request.POST.get('banner_link_url', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        if not name:
            return JsonResponse({'success': False, 'message': 'ब्यानरको नाम आवश्यक छ!'})
        obj.banner_name = name
        obj.banner_link_url = link_url or None
        obj.is_active = is_active
        obj.save()
        return JsonResponse({'success': True, 'message': 'ब्यानर अपडेट भयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def banner_delete(request, pk):
    try:
        obj = get_object_or_404(CompanyBanner, pk=pk)
        for img in obj.images.all():
            if img.banner_image:
                img.banner_image.delete(save=False)
        obj.delete()
        return JsonResponse({'success': True, 'message': 'ब्यानर मेटाइयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def banner_image_create(request):
    """Add image to a banner. banner id comes from POST body field 'banner'."""
    try:
        banner_id = request.POST.get('banner')
        banner = get_object_or_404(CompanyBanner, pk=banner_id)
        image = request.FILES.get('banner_image')
        if not image:
            return JsonResponse({'success': False, 'message': 'तस्वीर आवश्यक छ!'})
        img_obj = BannerImage(banner=banner, banner_image=image)
        img_obj.save()
        return JsonResponse({'success': True, 'message': 'ब्यानर तस्वीर थपियो!',
                             'id': img_obj.id,
                             'image_url': img_obj.banner_image.url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def banner_image_delete(request, pk):
    try:
        obj = get_object_or_404(BannerImage, pk=pk)
        if obj.banner_image:
            obj.banner_image.delete(save=False)
        obj.delete()
        return JsonResponse({'success': True, 'message': 'ब्यानर तस्वीर मेटाइयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ─── BOD ────────────────────────────────────────────────────────────────────

@admin_required
def bod_list(request):
    items = CompanyBOD.objects.all().order_by('-created_at')
    return render(request, 'admin/bod.html', {'items': items, **_admin_context(request)})


@admin_required
@require_POST
def bod_create(request):
    try:
        name = request.POST.get('bod_name', '').strip()
        designation = request.POST.get('bod_designation', '').strip()
        image = request.FILES.get('bod_image')
        if not name or not designation:
            return JsonResponse({'success': False, 'message': 'नाम र पद आवश्यक छ!'})
        obj = CompanyBOD(bod_name=name, bod_designation=designation)
        if image:
            obj.bod_image = image
        obj.save()
        return JsonResponse({'success': True, 'message': 'सञ्चालक समिति सफलतापूर्वक थपियो!',
                             'id': obj.id, 'name': obj.bod_name,
                             'designation': obj.bod_designation})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def bod_update(request, pk):
    try:
        obj = get_object_or_404(CompanyBOD, pk=pk)
        name = request.POST.get('bod_name', '').strip()
        designation = request.POST.get('bod_designation', '').strip()
        image = request.FILES.get('bod_image')
        if not name or not designation:
            return JsonResponse({'success': False, 'message': 'नाम र पद आवश्यक छ!'})
        obj.bod_name = name
        obj.bod_designation = designation
        if image:
            obj.bod_image = image
        obj.save()
        return JsonResponse({'success': True, 'message': 'सञ्चालक समिति अपडेट भयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def bod_delete(request, pk):
    try:
        obj = get_object_or_404(CompanyBOD, pk=pk)
        if obj.bod_image:
            obj.bod_image.delete(save=False)
        obj.delete()
        return JsonResponse({'success': True, 'message': 'सञ्चालक समिति मेटाइयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ─── Employee ───────────────────────────────────────────────────────────────

@admin_required
def employee_list(request):
    items = CompanyEmployee.objects.all().order_by('-created_at')
    return render(request, 'admin/employee.html', {'items': items, **_admin_context(request)})


@admin_required
@require_POST
def employee_create(request):
    try:
        name = request.POST.get('employee_name', '').strip()
        designation = request.POST.get('employee_designation', '').strip()
        address = request.POST.get('employee_address', '').strip()
        mobile = request.POST.get('employee_mobile_no', '').strip()
        image = request.FILES.get('employee_image')
        if not name or not designation:
            return JsonResponse({'success': False, 'message': 'नाम र पद आवश्यक छ!'})
        obj = CompanyEmployee(
            employee_name=name,
            employee_designation=designation,
            employee_address=address or None,
            employee_mobile_no=mobile or None,
        )
        if image:
            obj.employee_image = image
        obj.save()
        return JsonResponse({'success': True, 'message': 'कर्मचारी सफलतापूर्वक थपियो!',
                             'id': obj.id, 'name': obj.employee_name,
                             'designation': obj.employee_designation})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def employee_update(request, pk):
    try:
        obj = get_object_or_404(CompanyEmployee, pk=pk)
        name = request.POST.get('employee_name', '').strip()
        designation = request.POST.get('employee_designation', '').strip()
        address = request.POST.get('employee_address', '').strip()
        mobile = request.POST.get('employee_mobile_no', '').strip()
        image = request.FILES.get('employee_image')
        if not name or not designation:
            return JsonResponse({'success': False, 'message': 'नाम र पद आवश्यक छ!'})
        obj.employee_name = name
        obj.employee_designation = designation
        obj.employee_address = address or None
        obj.employee_mobile_no = mobile or None
        if image:
            obj.employee_image = image
        obj.save()
        return JsonResponse({'success': True, 'message': 'कर्मचारी अपडेट भयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_required
@require_POST
def employee_delete(request, pk):
    try:
        obj = get_object_or_404(CompanyEmployee, pk=pk)
        if obj.employee_image:
            obj.employee_image.delete(save=False)
        obj.delete()
        return JsonResponse({'success': True, 'message': 'कर्मचारी मेटाइयो!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})