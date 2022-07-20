from django.db import models
import os
# Create your models here.
from django.contrib.auth.models import AbstractUser 

def content_file_user(instance, filename):
    return 'profile/{1}'.format(instance, filename)

def content_file_products_picture(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'product/{1}'.format(instance, file_save_name)

def content_file_banner_picture(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'banner/{1}'.format(instance, file_save_name)

def content_file_product_pdf(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'product/pdf/{1}'.format(instance, file_save_name)

class User(AbstractUser):
    picture = models.ImageField(upload_to=content_file_user, blank=True)
    telephone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username
    class Meta:
        permissions = (("admin_user","Can use modules admin"),("guest_user","Can use modules guest"))

class AboutUs(models.Model):
    description = models.TextField(max_length=800)
    language = models.ForeignKey('LanguageCampaign', on_delete=models.SET_NULL, blank=True, null=True) 
    def __str__(self):
        return self.description

class Category(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=400, blank=True)
    position = models.IntegerField(null=True, blank=True, default=10000)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='children')
    language = models.ForeignKey('LanguageCampaign', on_delete=models.SET_NULL, blank=True, null=True) 
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position', '-date', 'id']

class LanguageCampaign(models.Model):
    name_language = models.CharField(max_length=250)
    value_language = models.CharField(max_length=15)

    def __str__(self):
        return self.name_language

class Product(models.Model):
    price = models.DecimalField(max_digits=100, default='0', decimal_places=2, blank=True, null=True)
    name = models.CharField(max_length=150)
    picture1 = models.ImageField(upload_to=content_file_products_picture, blank=True)
    picture2 = models.ImageField(upload_to=content_file_products_picture, blank=True)
    picture3 = models.ImageField(upload_to=content_file_products_picture, blank=True)
    picture4 = models.ImageField(upload_to=content_file_products_picture, blank=True)
    description = models.TextField( blank=True)
    reference = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    pdf = models.FileField(upload_to=content_file_product_pdf, blank=True)
    approved = models.BooleanField(default=True, blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
    flag = models.CharField(max_length=500, blank=True, null=True)
    flagbackcolor = models.CharField(max_length=30, blank=True, null=True)
    indexed = models.BooleanField(default=False, blank=True)
    position = models.IntegerField(null=True, blank=True, default=10000)
    min_order = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.name
    
    def filename(self):
        return os.path.basename(self.pdf.name)

class Banner(models.Model):
    name = models.CharField(max_length=150)
    picture = models.ImageField(upload_to=content_file_banner_picture, blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
    position = models.IntegerField(null=True, blank=True, default=10000)
    def __str__(self):
        return self.name