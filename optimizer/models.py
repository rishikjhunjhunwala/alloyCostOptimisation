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

class OverwriteStorage(FileSystemStorage):
    """
    Storage class that overwrites existing files with the same name.
    """
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

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
    result_data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    
    # Tracking results
    total_cost = models.FloatField(null=True, blank=True)
    total_products = models.IntegerField(null=True, blank=True)
    
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

class BatchProduct(models.Model):
    """
    Model for storing products in a batch with their required amounts.
    """
    batch = models.ForeignKey(OptimizationBatch, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    amount = models.FloatField()
    
    def __str__(self):
        return f"{self.product_name} - {self.amount}"