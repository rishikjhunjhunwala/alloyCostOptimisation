from django import forms
from .models import ScrapData, CompositionRequirements, OptimizationBatch, BatchProduct
import csv
import io
import pandas as pd

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