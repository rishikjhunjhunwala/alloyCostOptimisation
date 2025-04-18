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

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Data upload and view
    path('upload/scrap-data/', views.upload_scrap_data, name='upload_scrap_data'),
    path('upload/composition/', views.upload_composition_requirements, name='upload_composition_requirements'),
    path('view/scrap-data/<int:pk>/', views.view_scrap_data, name='view_scrap_data'),
    path('view/scrap-data/', views.view_scrap_data, name='view_scrap_data_latest'),
    path('view/composition/<int:pk>/', views.view_composition_requirements, name='view_composition_requirements'),
    path('view/composition/', views.view_composition_requirements, name='view_composition_requirements_latest'),
    
    # Batch management
    path('batch/create/', views.create_batch, name='create_batch'),
    path('batch/edit/<int:pk>/', views.edit_batch, name='edit_batch'),
    path('batch/list/', views.batch_list, name='batch_list'),
    path('batch/<int:batch_pk>/product/<int:product_pk>/remove/', views.remove_batch_product, name='remove_batch_product'),
    path('batch/<int:pk>/upload-products/', views.upload_batch_products, name='upload_batch_products'),
    
    # Optimization
    path('batch/<int:pk>/optimize/', views.run_optimization, name='run_optimization'),
    path('results/<int:pk>/', views.view_optimization_result, name='view_optimization_result'),
    path('results/<int:pk>/download/', views.download_optimization_result, name='download_optimization_result'),
    path('results/', views.result_list, name='result_list'),
]