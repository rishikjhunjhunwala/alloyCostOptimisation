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
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Organization, UserProfile, ScrapData, CompositionRequirements, 
    OptimizationResult, OptimizationBatch, BatchProduct
)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at', 'user_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)
    
    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Users'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'employee_id', 'department', 'created_at')
    list_filter = ('organization', 'department', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')

class BatchProductInline(admin.TabularInline):
    model = BatchProduct
    extra = 1

@admin.register(OptimizationBatch)
class OptimizationBatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'created_by', 'created_at', 'status')
    list_filter = ('organization', 'status', 'created_at')
    search_fields = ('name', 'organization__name')
    inlines = [BatchProductInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile'):
            return qs.filter(organization=request.user.profile.organization)
        return qs.none()

@admin.register(OptimizationResult)
class OptimizationResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'created_by', 'created_at', 'status', 'total_cost', 'total_products')
    list_filter = ('organization', 'status', 'created_at')
    search_fields = ('organization__name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile'):
            return qs.filter(organization=request.user.profile.organization)
        return qs.none()

@admin.register(ScrapData)
class ScrapDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'uploaded_by', 'uploaded_at', 'processed')
    list_filter = ('organization', 'processed', 'uploaded_at')
    search_fields = ('organization__name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile'):
            return qs.filter(organization=request.user.profile.organization)
        return qs.none()

@admin.register(CompositionRequirements)
class CompositionRequirementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'uploaded_by', 'uploaded_at', 'processed')
    list_filter = ('organization', 'processed', 'uploaded_at')
    search_fields = ('organization__name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile'):
            return qs.filter(organization=request.user.profile.organization)
        return qs.none()

@admin.register(BatchProduct)
class BatchProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'amount', 'batch', 'organization')
    list_filter = ('batch__organization',)
    search_fields = ('product_name', 'batch__name')
    
    def organization(self, obj):
        return obj.batch.organization
    organization.short_description = 'Organization'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile'):
            return qs.filter(batch__organization=request.user.profile.organization)
        return qs.none()
