from django.db import models
from django.utils import timezone
from slugify import slugify  

# All created_at will use Django TIME_ZONE from settings (Asia/Kathmandu)
def get_current_time():
    return timezone.now()


# ----------------- Company Downloads -----------------
class CompanyDownloads(models.Model):
    download_title = models.CharField(max_length=1000)
    download_file = models.FileField(upload_to='downloads/')
    created_at = models.DateTimeField(default=get_current_time)
    slug = models.SlugField(max_length=1200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.download_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.download_title


# ----------------- Company News -----------------
class CompanyNews(models.Model):
    news_title = models.CharField(max_length=1000)
    news_descriptions = models.TextField(null=True, blank=True)
    attachments = models.FileField(upload_to='news/attachments/', null=True, blank=True)
    news_image = models.ImageField(upload_to='admin/NewsImages/', null=True, blank=True)
    created_at = models.DateTimeField(default=get_current_time)
    slug = models.SlugField(max_length=1200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.news_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.news_title


# ----------------- Company Gallery -----------------
class CompanyGallery(models.Model):
    gallery_title = models.CharField(max_length=1000)
    gallery_image = models.ImageField(upload_to='admin/GalleryImages/')
    created_at = models.DateTimeField(default=get_current_time)
    slug = models.SlugField(max_length=1200, blank=True) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.gallery_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.gallery_title


# ----------------- Company Banner -----------------
class CompanyBanner(models.Model):
    banner_name = models.CharField(max_length=1000)
    banner_link_url = models.URLField(max_length=2000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=get_current_time)
    slug = models.SlugField(max_length=1200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.banner_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.banner_name


class BannerImage(models.Model):
    banner = models.ForeignKey(CompanyBanner, related_name='images', on_delete=models.CASCADE)
    banner_image = models.ImageField(upload_to='banners/')
    created_at = models.DateTimeField(default=get_current_time)

    def __str__(self):
        return f"Image for {self.banner.banner_name}"


# ----------------- Company BOD -----------------
class CompanyBOD(models.Model):
    bod_name = models.CharField(max_length=500)
    bod_designation = models.CharField(max_length=500)
    bod_image = models.ImageField(upload_to='admin/BODImages/', null=True, blank=True)
    created_at = models.DateTimeField(default=get_current_time)
    slug = models.SlugField(max_length=600, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.bod_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.bod_name
    


# ----------------- Company Employee -----------------
class CompanyEmployee(models.Model):
    employee_name = models.CharField(max_length=500)
    employee_designation = models.CharField(max_length=500)
    employee_address = models.TextField(null=True, blank=True)
    employee_mobile_no = models.CharField(max_length=20, null=True, blank=True)
    employee_image = models.ImageField(upload_to='admin/EmployeeImages/', null=True, blank=True)
    created_at = models.DateTimeField(default=get_current_time)
    slug = models.SlugField(max_length=600, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.employee_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee_name