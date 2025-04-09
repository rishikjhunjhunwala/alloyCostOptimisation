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