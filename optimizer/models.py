from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.utils import timezone


class OverwriteStorage(FileSystemStorage):
    """
    Storage class that overwrites existing files with the same name.
    """
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class Organization(models.Model):
    """
    Model for organizations to enable multi-tenant access.
    """
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="Short code for organization (e.g., ABC, XYZ)")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class UserProfile(models.Model):
    """
    Extended user profile with organization association.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['organization', 'employee_id']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.organization.name}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create/update user profile when user is created/updated.
    Note: Organization must be set manually after user creation.
    """
    if created:
        # Don't create profile automatically - will be done in registration
        pass
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

class ScrapData(models.Model):
    """
    Model for storing uploaded scrap data files with organization isolation.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='scrap_data')
    file = models.FileField(upload_to='scrap_data/', storage=OverwriteStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Scrap Data - {self.organization.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

class CompositionRequirements(models.Model):
    """
    Model for storing uploaded composition requirements files with organization isolation.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='composition_requirements')
    file = models.FileField(upload_to='composition_requirements/', storage=OverwriteStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Composition Requirements - {self.organization.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

class OptimizationResult(models.Model):
    """
    Model for storing optimization results with organization isolation.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='optimization_results')
    scrap_data = models.ForeignKey(ScrapData, on_delete=models.CASCADE)
    composition_requirements = models.ForeignKey(CompositionRequirements, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    result_data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    
    # Tracking results
    total_cost = models.FloatField(null=True, blank=True)
    total_products = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Optimization Result - {self.organization.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class OptimizationBatch(models.Model):
    """
    Model for tracking batch optimization jobs with organization isolation.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='optimization_batches')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    result = models.ForeignKey(OptimizationResult, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['organization', 'name']
    
    def __str__(self):
        return f"Batch: {self.name} - {self.organization.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class BatchProduct(models.Model):
    """
    Model for storing products in a batch with their required amounts.
    """
    batch = models.ForeignKey(OptimizationBatch, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    amount = models.FloatField()
    
    def __str__(self):
        return f"{self.product_name} - {self.amount}"