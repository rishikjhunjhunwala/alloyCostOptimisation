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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings
<<<<<<< HEAD
from django.contrib.auth import login
from django.db.models import Q
=======
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078

from .models import (
    ScrapData, CompositionRequirements, 
    OptimizationResult, OptimizationBatch, 
<<<<<<< HEAD
    BatchProduct, Organization, UserProfile
)
from .forms import (
    ScrapDataForm, CompositionRequirementsForm, 
    BatchForm, BatchProductForm, UploadBatchForm,
    UserRegistrationForm, OrganizationForm
=======
    BatchProduct
)
from .forms import (
    ScrapDataForm, CompositionRequirementsForm, 
    BatchForm, BatchProductForm, UploadBatchForm
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
)

import pandas as pd
import numpy as np
import csv
import json
import os
import io
from datetime import datetime

from optimization.solver import (
    AlloyOptimizer, preprocess_scrap_data, 
    preprocess_composition_requirements
)

<<<<<<< HEAD
def register(request):
    """
    User registration view with organization selection.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to {user.profile.organization.name}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'optimizer/register.html', {'form': form})

@login_required
def dashboard(request):
    """
    Main dashboard view showing recent batches and uploads for user's organization.
    """
    org = request.organization
    
    batches = OptimizationBatch.objects.filter(organization=org).order_by('-created_at')[:5]
    results = OptimizationResult.objects.filter(organization=org).order_by('-created_at')[:5]
    scrap_data = ScrapData.objects.filter(organization=org).order_by('-uploaded_at')[:5]
    comp_requirements = CompositionRequirements.objects.filter(organization=org).order_by('-uploaded_at')[:5]
=======
@login_required
def dashboard(request):
    """
    Main dashboard view showing recent batches and uploads.
    """
    batches = OptimizationBatch.objects.all().order_by('-created_at')[:5]
    results = OptimizationResult.objects.all().order_by('-created_at')[:5]
    scrap_data = ScrapData.objects.all().order_by('-uploaded_at')[:5]
    comp_requirements = CompositionRequirements.objects.all().order_by('-uploaded_at')[:5]
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    context = {
        'batches': batches,
        'results': results,
        'scrap_data': scrap_data,
        'comp_requirements': comp_requirements,
    }
    
    return render(request, 'optimizer/dashboard.html', context)

@login_required
def upload_scrap_data(request):
    """
    View for uploading scrap data files.
    """
    if request.method == 'POST':
        form = ScrapDataForm(request.POST, request.FILES)
        if form.is_valid():
<<<<<<< HEAD
            instance = form.save(commit=False)
            instance.organization = request.organization
            instance.uploaded_by = request.user
            instance.save()
=======
            instance = form.save()
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
            messages.success(request, 'Scrap data uploaded successfully.')
            return redirect('dashboard')
    else:
        form = ScrapDataForm()
    
    context = {
        'form': form,
        'title': 'Upload Scrap Data',
    }
    
    return render(request, 'optimizer/upload.html', context)

@login_required
def upload_composition_requirements(request):
    """
    View for uploading composition requirements files.
    """
    if request.method == 'POST':
        form = CompositionRequirementsForm(request.POST, request.FILES)
        if form.is_valid():
<<<<<<< HEAD
            instance = form.save(commit=False)
            instance.organization = request.organization
            instance.uploaded_by = request.user
            instance.save()
=======
            instance = form.save()
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
            messages.success(request, 'Composition requirements uploaded successfully.')
            return redirect('dashboard')
    else:
        form = CompositionRequirementsForm()
    
    context = {
        'form': form,
        'title': 'Upload Composition Requirements',
    }
    
    return render(request, 'optimizer/upload.html', context)

@login_required
def view_scrap_data(request, pk=None):
    """
<<<<<<< HEAD
    View for displaying scrap data for user's organization.
    """
    org = request.organization
    
    if pk:
        scrap_data = get_object_or_404(ScrapData, pk=pk, organization=org)
    else:
        scrap_data = ScrapData.objects.filter(organization=org).order_by('-uploaded_at').first()
=======
    View for displaying scrap data.
    """
    if pk:
        scrap_data = get_object_or_404(ScrapData, pk=pk)
    else:
        scrap_data = ScrapData.objects.latest('uploaded_at') if ScrapData.objects.exists() else None
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    if not scrap_data:
        messages.error(request, 'No scrap data found. Please upload a file first.')
        return redirect('upload_scrap_data')
    
    try:
        df = pd.read_csv(scrap_data.file.path)
        context = {
            'scrap_data': scrap_data,
            'columns': df.columns.tolist(),
            'data': df.to_dict('records'),
        }
        return render(request, 'optimizer/view_scrap_data.html', context)
    except Exception as e:
        messages.error(request, f'Error reading scrap data: {str(e)}')
        return redirect('dashboard')

@login_required
def view_composition_requirements(request, pk=None):
    """
<<<<<<< HEAD
    View for displaying composition requirements for user's organization.
    """
    org = request.organization
    
    if pk:
        comp_req = get_object_or_404(CompositionRequirements, pk=pk, organization=org)
    else:
        comp_req = CompositionRequirements.objects.filter(organization=org).order_by('-uploaded_at').first()
=======
    View for displaying composition requirements.
    """
    if pk:
        comp_req = get_object_or_404(CompositionRequirements, pk=pk)
    else:
        comp_req = CompositionRequirements.objects.latest('uploaded_at') if CompositionRequirements.objects.exists() else None
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    if not comp_req:
        messages.error(request, 'No composition requirements found. Please upload a file first.')
        return redirect('upload_composition_requirements')
    
    try:
        df = pd.read_csv(comp_req.file.path)
        context = {
            'comp_req': comp_req,
            'columns': df.columns.tolist(),
            'data': df.to_dict('records'),
        }
        return render(request, 'optimizer/view_composition_requirements.html', context)
    except Exception as e:
        messages.error(request, f'Error reading composition requirements: {str(e)}')
        return redirect('dashboard')

@login_required
def create_batch(request):
    """
    View for creating a new optimization batch.
    """
<<<<<<< HEAD
    org = request.organization
    
    if not CompositionRequirements.objects.filter(organization=org).exists():
        messages.error(request, 'No composition requirements found. Please upload a file first.')
        return redirect('upload_composition_requirements')
    
    if not ScrapData.objects.filter(organization=org).exists():
=======
    if not CompositionRequirements.objects.exists():
        messages.error(request, 'No composition requirements found. Please upload a file first.')
        return redirect('upload_composition_requirements')
    
    if not ScrapData.objects.exists():
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
        messages.error(request, 'No scrap data found. Please upload a file first.')
        return redirect('upload_scrap_data')
    
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
            batch = form.save(commit=False)
            batch.organization = org
            batch.created_by = request.user
            batch.save()
=======
            batch = form.save()
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
            messages.success(request, 'Batch created successfully.')
            return redirect('edit_batch', pk=batch.pk)
    else:
        form = BatchForm()
    
    context = {
        'form': form,
        'title': 'Create Optimization Batch',
    }
    
    return render(request, 'optimizer/create_batch.html', context)

@login_required
def edit_batch(request, pk):
    """
    View for editing a batch and adding products.
    """
<<<<<<< HEAD
    org = request.organization
    batch = get_object_or_404(OptimizationBatch, pk=pk, organization=org)
    products = batch.products.all()
    
    # Get latest composition requirements for this organization
    comp_req = CompositionRequirements.objects.filter(organization=org).order_by('-uploaded_at').first()
    
    if not comp_req:
        messages.error(request, 'No composition requirements found. Please upload a file first.')
        return redirect('upload_composition_requirements')
=======
    batch = get_object_or_404(OptimizationBatch, pk=pk)
    products = batch.products.all()
    
    # Get latest composition requirements
    comp_req = CompositionRequirements.objects.latest('uploaded_at')
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    try:
        # Read product names from composition requirements
        df = pd.read_csv(comp_req.file.path)
        available_products = df['Product'].unique().tolist()
    except Exception as e:
        messages.error(request, f'Error reading composition requirements: {str(e)}')
        available_products = []
    
    if request.method == 'POST':
        form = BatchProductForm(request.POST, product_choices=available_products)
        if form.is_valid():
            product = form.save(commit=False)
            product.batch = batch
            product.save()
            messages.success(request, f'Product {product.product_name} added to batch.')
            return redirect('edit_batch', pk=batch.pk)
    else:
        form = BatchProductForm(product_choices=available_products)
    
    upload_batch_form = UploadBatchForm()
    
    context = {
        'batch': batch,
        'products': products,
        'form': form,
        'upload_batch_form': upload_batch_form,
        'available_products': available_products,
    }
    
    return render(request, 'optimizer/edit_batch.html', context)

@login_required
@require_POST
def upload_batch_products(request, pk):
    """
    View for uploading batch products from a CSV file.
    """
<<<<<<< HEAD
    org = request.organization
    batch = get_object_or_404(OptimizationBatch, pk=pk, organization=org)
=======
    batch = get_object_or_404(OptimizationBatch, pk=pk)
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    form = UploadBatchForm(request.POST, request.FILES)
    
    if form.is_valid():
        try:
            # Read the CSV file
            file = form.cleaned_data['file']
            df = pd.read_csv(file)
            
            # Add products to batch
            for _, row in df.iterrows():
                BatchProduct.objects.create(
                    batch=batch,
                    product_name=row['Product'],
                    amount=row['Amount']
                )
            
            messages.success(request, 'Batch products uploaded successfully.')
        except Exception as e:
            messages.error(request, f'Error processing batch file: {str(e)}')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
    
    return redirect('edit_batch', pk=batch.pk)

@login_required
def remove_batch_product(request, batch_pk, product_pk):
    """
    View for removing a product from a batch.
    """
<<<<<<< HEAD
    org = request.organization
    batch = get_object_or_404(OptimizationBatch, pk=batch_pk, organization=org)
    product = get_object_or_404(BatchProduct, pk=product_pk, batch=batch)
=======
    product = get_object_or_404(BatchProduct, pk=product_pk, batch_id=batch_pk)
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    product_name = product.product_name
    product.delete()
    messages.success(request, f'Product {product_name} removed from batch.')
    return redirect('edit_batch', pk=batch_pk)

@login_required
def run_optimization(request, pk):
    """
    View for running the optimization for a batch.
    """
<<<<<<< HEAD
    org = request.organization
    batch = get_object_or_404(OptimizationBatch, pk=pk, organization=org)
=======
    batch = get_object_or_404(OptimizationBatch, pk=pk)
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    if batch.products.count() == 0:
        messages.error(request, 'Cannot run optimization: batch has no products.')
        return redirect('edit_batch', pk=batch.pk)
    
    try:
<<<<<<< HEAD
        # Get latest data files for this organization
        scrap_data_obj = ScrapData.objects.filter(organization=org).order_by('-uploaded_at').first()
        comp_req_obj = CompositionRequirements.objects.filter(organization=org).order_by('-uploaded_at').first()
        
        if not scrap_data_obj or not comp_req_obj:
            messages.error(request, 'Missing required data files. Please upload scrap data and composition requirements.')
            return redirect('edit_batch', pk=batch.pk)
=======
        # Get latest data files
        scrap_data_obj = ScrapData.objects.latest('uploaded_at')
        comp_req_obj = CompositionRequirements.objects.latest('uploaded_at')
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
        
        # Read and preprocess data
        scrap_df = pd.read_csv(scrap_data_obj.file.path)
        comp_df = pd.read_csv(comp_req_obj.file.path)
        
        scrap_df = preprocess_scrap_data(scrap_df)
        comp_df = preprocess_composition_requirements(comp_df)
        
        # Create optimizer
        optimizer = AlloyOptimizer(scrap_df, comp_df)
        
        # Prepare batch requirements
        batch_requirements = {
            product.product_name: product.amount
            for product in batch.products.all()
        }
        
        # Run optimization
        results = optimizer.optimize_batch(batch_requirements)
        
        # Save results
        opt_result = OptimizationResult.objects.create(
<<<<<<< HEAD
            organization=org,
            scrap_data=scrap_data_obj,
            composition_requirements=comp_req_obj,
            created_by=request.user,
=======
            scrap_data=scrap_data_obj,
            composition_requirements=comp_req_obj,
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
            result_data=results,
            status='completed',
            total_cost=results['total_batch_cost'],
            total_products=len(batch_requirements)
        )
        
        # Update batch
        batch.status = 'completed'
        batch.result = opt_result
        batch.save()
        
        messages.success(request, 'Optimization completed successfully.')
        return redirect('view_optimization_result', pk=opt_result.pk)
    
    except Exception as e:
        messages.error(request, f'Error running optimization: {str(e)}')
        return redirect('edit_batch', pk=batch.pk)

@login_required
def view_optimization_result(request, pk):
    """
    View for displaying optimization results.
    """
<<<<<<< HEAD
    org = request.organization
    result = get_object_or_404(OptimizationResult, pk=pk, organization=org)
=======
    result = get_object_or_404(OptimizationResult, pk=pk)
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    # Calculate scrap costs for each product
    if result.result_data and 'product_results' in result.result_data:
        for product_name, product_result in result.result_data['product_results'].items():
            if product_result['status'] == 'optimal' and 'scrap_mix' in product_result:
                # Add per-material costs to the result data
                product_result['scrap_costs'] = {}
                
                try:
                    # Read scrap data for cost information
                    scrap_df = pd.read_csv(result.scrap_data.file.path)
                    
                    for scrap, amount in product_result['scrap_mix'].items():
                        # Find cost of this scrap material
                        scrap_cost = scrap_df.loc[scrap_df['Scrap_Type'] == scrap, 'COST'].values[0]
                        product_result['scrap_costs'][scrap] = amount * scrap_cost
                except Exception as e:
                    # If there's an error, continue without the costs
                    pass
    
    context = {
        'result': result,
        'data': result.result_data,
    }
    
<<<<<<< HEAD
=======
    # Use the simple template instead
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    return render(request, 'optimizer/simple_result.html', context)

@login_required
def download_optimization_result(request, pk):
    """
    View for downloading optimization results as CSV.
    """
<<<<<<< HEAD
    org = request.organization
    result = get_object_or_404(OptimizationResult, pk=pk, organization=org)
=======
    result = get_object_or_404(OptimizationResult, pk=pk)
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="optimization_result_{pk}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    
    # Write header
    writer.writerow(['Type', 'Product', 'Scrap', 'Amount', 'Cost', 'SI', 'FE', 'CU', 'MN', 'MG'])
    
    try:
        # Load scrap data for cost calculations
        scrap_df = pd.read_csv(result.scrap_data.file.path)
        
        # Write product results
        for product_name, product_result in result.result_data['product_results'].items():
            if product_result['status'] == 'optimal':
                # Write scrap mix
                for scrap, amount in product_result['scrap_mix'].items():
                    # Get cost of this scrap material
                    try:
                        scrap_cost = scrap_df.loc[scrap_df['Scrap_Type'] == scrap, 'COST'].values[0]
                        item_cost = amount * scrap_cost
                    except:
                        item_cost = 0
                        
                    writer.writerow([
                        'Scrap', product_name, scrap, amount, item_cost,
                        '', '', '', '', ''
                    ])
                
                # Write resulting composition
                writer.writerow([
                    'Composition', product_name, '', '', product_result['total_cost'],
                    product_result['resulting_composition']['SI'],
                    product_result['resulting_composition']['FE'],
                    product_result['resulting_composition']['CU'],
                    product_result['resulting_composition']['MN'],
                    product_result['resulting_composition']['MG']
                ])
        
        # Write summary
        writer.writerow([])
        writer.writerow(['Total Cost', result.result_data['total_batch_cost']])
        
    except Exception as e:
        # Handle any errors gracefully
        writer.writerow(['Error occurred during CSV generation:', str(e)])
    
    return response

@login_required
def batch_list(request):
    """
<<<<<<< HEAD
    View for listing all batches for user's organization.
    """
    org = request.organization
    batches = OptimizationBatch.objects.filter(organization=org).order_by('-created_at')
=======
    View for listing all batches.
    """
    batches = OptimizationBatch.objects.all().order_by('-created_at')
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    context = {
        'batches': batches,
    }
    
    return render(request, 'optimizer/batch_list.html', context)

@login_required
def result_list(request):
    """
<<<<<<< HEAD
    View for listing all optimization results for user's organization.
    """
    org = request.organization
    results = OptimizationResult.objects.filter(organization=org).order_by('-created_at')
=======
    View for listing all optimization results.
    """
    results = OptimizationResult.objects.all().order_by('-created_at')
>>>>>>> 17bcccaba7fb9cd976497db44b0d4a7bc8f1d078
    
    context = {
        'results': results,
    }
    
    return render(request, 'optimizer/result_list.html', context)