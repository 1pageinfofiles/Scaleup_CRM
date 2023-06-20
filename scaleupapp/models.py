from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group
# Create your models here.
STATUS_CHOICES = (
        ('A', 'Active'),
        ('P', 'Pending'),
        ('I', 'Inactive'),
        ('D', 'Deleted')
    )
class CatalogueStatus(models.Model):
    title = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(max_length=250, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    def __str__(self):
        return self.title

class CompanyDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    catalogue_status = models.ForeignKey(CatalogueStatus, on_delete=models.CASCADE, null=True)
    business_name = models.CharField(max_length=250, blank=True)
    customer_name = models.CharField(max_length=250, blank=True)
    mobile = models.CharField(max_length=250, blank=True)
    alt_mobile = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    links = models.CharField(max_length=250, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.business_name} ({self.customer_name})"
    
class CompanyDetailsRemarkPivot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    catalogue_status = models.ForeignKey(CatalogueStatus, on_delete=models.CASCADE)
    company_details = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, null=True)
    remarks = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


