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
from django.contrib import admin
from .models import (
    ScrapData, CompositionRequirements, 
    OptimizationResult, OptimizationBatch, 
    BatchProduct
)

class BatchProductInline(admin.TabularInline):
    model = BatchProduct
    extra = 1

@admin.register(OptimizationBatch)
class OptimizationBatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'status')
    search_fields = ('name',)
    list_filter = ('status', 'created_at')
    inlines = [BatchProductInline]

@admin.register(OptimizationResult)
class OptimizationResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', 'total_cost', 'total_products')
    list_filter = ('status', 'created_at')

@admin.register(ScrapData)
class ScrapDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at', 'processed')
    list_filter = ('processed', 'uploaded_at')

@admin.register(CompositionRequirements)
class CompositionRequirementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at', 'processed')
    list_filter = ('processed', 'uploaded_at')

@admin.register(BatchProduct)
class BatchProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'amount', 'batch')
    search_fields = ('product_name',)
    list_filter = ('batch',)