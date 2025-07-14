<<<<<<< HEAD
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.utils import timezone


=======
# Copyright 2025 RISHIK JHUNJHUNWALA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.utils import timezone

>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
class OverwriteStorage(FileSystemStorage):
    """
    Storage class that overwrites existing files with the same name.
    """
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

<<<<<<< HEAD
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
=======
class ScrapData(models.Model):
    """
    Model for storing uploaded scrap data files.
    """
    file = models.FileField(upload_to='scrap_data/', storage=OverwriteStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Scrap Data - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

class CompositionRequirements(models.Model):
    """
    Model for storing uploaded composition requirements files.
    """
    file = models.FileField(upload_to='composition_requirements/', storage=OverwriteStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Composition Requirements - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

class OptimizationResult(models.Model):
    """
    Model for storing optimization results.
    """
    scrap_data = models.ForeignKey(ScrapData, on_delete=models.CASCADE)
    composition_requirements = models.ForeignKey(CompositionRequirements, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    result_data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    
    # Tracking results
    total_cost = models.FloatField(null=True, blank=True)
    total_products = models.IntegerField(null=True, blank=True)
    
<<<<<<< HEAD
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
=======
    def __str__(self):
        return f"Optimization Result - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class OptimizationBatch(models.Model):
    """
    Model for tracking batch optimization jobs.
    """
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    result = models.ForeignKey(OptimizationResult, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Batch: {self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078

class BatchProduct(models.Model):
    """
    Model for storing products in a batch with their required amounts.
    """
    batch = models.ForeignKey(OptimizationBatch, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    amount = models.FloatField()
    
    def __str__(self):
        return f"{self.product_name} - {self.amount}"