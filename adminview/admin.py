from django.contrib import admin
from .models import CompanyDownloads, CompanyNews, CompanyGallery, CompanyBanner, BannerImage, CompanyBOD, CompanyEmployee

# ----------------- Company Downloads -----------------
@admin.register(CompanyDownloads)
class CompanyDownloadsAdmin(admin.ModelAdmin):
    list_display = ('download_title', 'created_at')
    prepopulated_fields = {'slug': ('download_title',)}
    readonly_fields = ('created_at',)
    search_fields = ('download_title',)


# ----------------- Company News -----------------
@admin.register(CompanyNews)
class CompanyNewsAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'created_at')
    prepopulated_fields = {'slug': ('news_title',)}
    readonly_fields = ('created_at',)
    search_fields = ('news_title',)


# ----------------- Company Gallery -----------------
@admin.register(CompanyGallery)
class CompanyGalleryAdmin(admin.ModelAdmin):
    list_display = ('gallery_title', 'created_at')
    prepopulated_fields = {'slug': ('gallery_title',)}
    readonly_fields = ('created_at',)
    search_fields = ('gallery_title',)


# ----------------- Banner Image Inline -----------------
class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 5
    fields = ('banner_image',)


# ----------------- Company Banner -----------------
@admin.register(CompanyBanner)
class CompanyBannerAdmin(admin.ModelAdmin):
    list_display = ('banner_name', 'is_active', 'created_at')
    inlines = [BannerImageInline]
    readonly_fields = ('created_at',)
    prepopulated_fields = {'slug': ('banner_name',)}
    search_fields = ('banner_name',)


# ----------------- Company BOD -----------------
@admin.register(CompanyBOD)
class CompanyBODAdmin(admin.ModelAdmin):
    list_display = ('bod_name', 'bod_designation', 'created_at')
    prepopulated_fields = {'slug': ('bod_name',)}
    readonly_fields = ('created_at',)
    search_fields = ('bod_name', 'bod_designation')


# ----------------- Company Employee -----------------
@admin.register(CompanyEmployee)
class CompanyEmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'employee_designation', 'created_at')
    prepopulated_fields = {'slug': ('employee_name',)}
    readonly_fields = ('created_at',)
    search_fields = ('employee_name', 'employee_designation', 'employee_mobile_no')    