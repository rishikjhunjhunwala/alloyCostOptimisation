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

from django import forms
from .models import ScrapData, CompositionRequirements, OptimizationBatch, BatchProduct, Organization, UserProfile
import csv
import io
import pandas as pd
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class ScrapDataForm(forms.ModelForm):
    """
    Form for uploading scrap data files.
    """
    class Meta:
        model = ScrapData
        fields = ('file',)
        
    def clean_file(self):
        """
        Validate the uploaded file format and content.
        """
        file = self.cleaned_data.get('file')
        
        # Check file extension
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file.')
        
        # Check file content
        try:
            # Read file content
            content = file.read().decode('utf-8')
            file.seek(0) # Reset file pointer
            
            # Parse CSV
            df = pd.read_csv(io.StringIO(content))
            
            # Check required columns
            required_columns = ['Scrap_Type', 'COST', 'SI', 'FE', 'CU', 'MN', 'MG', 'Available_Amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise forms.ValidationError(f'Missing required columns: {", ".join(missing_columns)}')
            
            # Check data types
            for col in ['COST', 'SI', 'FE', 'CU', 'MN', 'MG', 'Available_Amount']:
                try:
                    df[col] = pd.to_numeric(df[col], errors='raise')
                except:
                    raise forms.ValidationError(f'Column {col} must contain numeric values only.')
            
        except pd.errors.EmptyDataError:
            raise forms.ValidationError('The uploaded file is empty.')
        except pd.errors.ParserError:
            raise forms.ValidationError('The uploaded file could not be parsed as a CSV file.')
        except Exception as e:
            raise forms.ValidationError(f'Error processing file: {str(e)}')
            
        return file

class CompositionRequirementsForm(forms.ModelForm):
    """
    Form for uploading composition requirements files.
    """
    class Meta:
        model = CompositionRequirements
        fields = ('file',)
        
    def clean_file(self):
        """
        Validate the uploaded file format and content.
        """
        file = self.cleaned_data.get('file')
        
        # Check file extension
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file.')
        
        try:
            # Read file content
            content = file.read().decode('utf-8')
            file.seek(0) # Reset file pointer
            
            # Parse CSV
            df = pd.read_csv(io.StringIO(content))
            
            # Check for required product and elements columns
            required_prefixes = ['Product', 'Amount', 'SI_', 'FE_', 'CU_', 'MN_', 'MG_']
            
            for prefix in required_prefixes:
                if prefix in ['Product', 'Amount']:
                    if prefix not in df.columns:
                        raise forms.ValidationError(f'Missing required column: {prefix}')
                else:
                    min_col = f"{prefix}MIN"
                    max_col = f"{prefix}MAX"
                    if min_col not in df.columns or max_col not in df.columns:
                        raise forms.ValidationError(f'Missing required columns: {min_col} and/or {max_col}')
            
            # Check data types
            try:
                df['Amount'] = pd.to_numeric(df['Amount'], errors='raise')
            except:
                raise forms.ValidationError('Column Amount must contain numeric values only.')
                
            for prefix in ['SI_', 'FE_', 'CU_', 'MN_', 'MG_']:
                min_col = f"{prefix}MIN"
                max_col = f"{prefix}MAX"
                try:
                    df[min_col] = pd.to_numeric(df[min_col], errors='raise')
                    df[max_col] = pd.to_numeric(df[max_col], errors='raise')
                except:
                    raise forms.ValidationError(f'Columns {min_col} and {max_col} must contain numeric values only.')
                
                # Check min <= max
                if (df[min_col] > df[max_col]).any():
                    raise forms.ValidationError(f'Minimum values in {min_col} must be less than or equal to maximum values in {max_col}.')
            
        except pd.errors.EmptyDataError:
            raise forms.ValidationError('The uploaded file is empty.')
        except pd.errors.ParserError:
            raise forms.ValidationError('The uploaded file could not be parsed as a CSV file.')
        except Exception as e:
            raise forms.ValidationError(f'Error processing file: {str(e)}')
            
        return file

class BatchProductForm(forms.ModelForm):
    """
    Form for adding a product to a batch.
    """
    class Meta:
        model = BatchProduct
        fields = ('product_name', 'amount')
        
    def __init__(self, *args, **kwargs):
        # Get available products from composition requirements
        self.product_choices = kwargs.pop('product_choices', [])
        super().__init__(*args, **kwargs)
        
        if self.product_choices:
            self.fields['product_name'] = forms.ChoiceField(
                choices=[(p, p) for p in self.product_choices]
            )

class BatchForm(forms.ModelForm):
    """
    Form for creating a batch optimization job.
    """
    class Meta:
        model = OptimizationBatch
        fields = ('name',)

class UploadBatchForm(forms.Form):
    """
    Form for uploading a batch of products from a CSV file.
    """
    file = forms.FileField()
    
    def clean_file(self):
        """
        Validate the uploaded batch file format and content.
        """
        file = self.cleaned_data.get('file')
        
        # Check file extension
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file.')
        
        try:
            # Read file content
            content = file.read().decode('utf-8')
            file.seek(0) # Reset file pointer
            
            # Parse CSV
            df = pd.read_csv(io.StringIO(content))
            
            # Check required columns
            required_columns = ['Product', 'Amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise forms.ValidationError(f'Missing required columns: {", ".join(missing_columns)}')
            
            # Check data types
            try:
                df['Amount'] = pd.to_numeric(df['Amount'], errors='raise')
            except:
                raise forms.ValidationError('Column Amount must contain numeric values only.')
            
            # Check for non-negative amounts
            if (df['Amount'] < 0).any():
                raise forms.ValidationError('Amounts must be non-negative.')
            
        except pd.errors.EmptyDataError:
            raise forms.ValidationError('The uploaded file is empty.')
        except pd.errors.ParserError:
            raise forms.ValidationError('The uploaded file could not be parsed as a CSV file.')
        except Exception as e:
            raise forms.ValidationError(f'Error processing file: {str(e)}')
            
        return file

class UserRegistrationForm(UserCreationForm):
    """
    Extended user registration form with organization selection.
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.filter(is_active=True),
        required=True,
        help_text="Select your organization"
    )
    employee_id = forms.CharField(
        max_length=50, 
        required=False,
        help_text="Optional employee ID"
    )
    department = forms.CharField(
        max_length=100, 
        required=False,
        help_text="Optional department name"
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        """
        Save user and create associated profile.
        """
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                organization=self.cleaned_data['organization'],
                employee_id=self.cleaned_data['employee_id'],
                department=self.cleaned_data['department']
            )
        
        return user

class OrganizationForm(forms.ModelForm):
    """
    Form for creating/editing organizations.
    """
    class Meta:
        model = Organization
        fields = ('name', 'code', 'description', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_code(self):
        """
        Validate organization code format.
        """
        code = self.cleaned_data['code'].upper()
        
        # Check format
        if not code.isalnum():
            raise forms.ValidationError('Organization code must contain only letters and numbers.')
        
        if len(code) < 2 or len(code) > 10:
            raise forms.ValidationError('Organization code must be between 2 and 10 characters.')
        
        return code
