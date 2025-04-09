import pandas as pd
import numpy as np
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus

class AlloyOptimizer:
    """
    A class for optimizing alloy formulations using linear programming.
    
    This optimizer determines the most economical mix of scrap materials
    that meets the composition requirements for specified alloy products.
    """
    
    def __init__(self, scrap_data, composition_requirements):
        """
        Initialize the optimizer with scrap data and composition requirements.
        
        Args:
            scrap_data (pandas.DataFrame): DataFrame containing available scrap materials,
                                          their compositions, costs, and available amounts.
            composition_requirements (pandas.DataFrame): DataFrame containing product
                                                        specifications with min/max percentages
                                                        for different elements.
        """
        self.scrap_data = scrap_data
        self.composition_requirements = composition_requirements
        self.elements = ['SI', 'FE', 'CU', 'MN', 'MG']
        self.results = {}
        
    def optimize_single_product(self, product_name, amount_needed):
        """
        Optimize the formulation for a single product.
        
        Args:
            product_name (str): Name of the product to optimize.
            amount_needed (float): Amount of the product needed (in weight units).
            
        Returns:
            dict: Dictionary containing optimization results including:
                - status: Optimization status
                - scrap_mix: Optimal mix of scrap materials
                - total_cost: Total cost of the formulation
                - resulting_composition: Composition of the resulting alloy
        """
        # Get product requirements
        product_req = self.composition_requirements[
            self.composition_requirements['Product'] == product_name
        ]
        
        if product_req.empty:
            return {
                'status': 'error',
                'message': f'Product {product_name} not found in composition requirements.'
            }
        
        # Create optimization problem
        problem = LpProblem(f"Optimize_{product_name}", LpMinimize)
        
        # Decision variables: amount of each scrap type to use
        scrap_vars = {
            scrap: LpVariable(f"Scrap_{scrap}", lowBound=0) 
            for scrap in self.scrap_data['Scrap_Type']
        }
        
        # Objective function: minimize total cost
        problem += lpSum([
            scrap_vars[scrap] * self.scrap_data.loc[
                self.scrap_data['Scrap_Type'] == scrap, 'COST'
            ].values[0] for scrap in self.scrap_data['Scrap_Type']
        ]), "Total Cost"
        
        # Constraint: total amount must equal the required amount
        problem += lpSum([scrap_vars[scrap] for scrap in self.scrap_data['Scrap_Type']]) == amount_needed, "Total Amount"
        
        # Constraints: composition requirements for each element
        for element in self.elements:
            # Extract min and max requirements
            element_min = product_req[f'{element}_MIN'].values[0]
            element_max = product_req[f'{element}_MAX'].values[0]
            
            # Add constraint for minimum percentage
            # The sum of (amount of scrap * element percentage) should be >= min_percentage * total_amount
            problem += lpSum([
                scrap_vars[scrap] * self.scrap_data.loc[
                    self.scrap_data['Scrap_Type'] == scrap, element
                ].values[0] for scrap in self.scrap_data['Scrap_Type']
            ]) >= element_min * amount_needed, f"Min_{element}"
            
            # Add constraint for maximum percentage
            # The sum of (amount of scrap * element percentage) should be <= max_percentage * total_amount
            problem += lpSum([
                scrap_vars[scrap] * self.scrap_data.loc[
                    self.scrap_data['Scrap_Type'] == scrap, element
                ].values[0] for scrap in self.scrap_data['Scrap_Type']
            ]) <= element_max * amount_needed, f"Max_{element}"
        
        # Constraints: available amount of each scrap
        for scrap in self.scrap_data['Scrap_Type']:
            available = self.scrap_data.loc[self.scrap_data['Scrap_Type'] == scrap, 'Available_Amount'].values[0]
            problem += scrap_vars[scrap] <= available, f"Available_{scrap}"
        
        # Solve the problem
        problem.solve()
        
        # Check status
        if LpStatus[problem.status] != 'Optimal':
            error_messages = {
                'Infeasible': 'The problem has no feasible solution with the given constraints.',
                'Unbounded': 'The problem has an unbounded solution (infinitely good solutions exist).',
                'Undefined': 'The problem could not be solved (may be too complex or ill-defined).',
                'NotSolved': 'The solver did not attempt to solve the problem.'
            }
            
            status_message = error_messages.get(
                LpStatus[problem.status], 
                f'No optimal solution found. Status: {LpStatus[problem.status]}'
            )
            
            return {
                'status': 'error',
                'message': status_message
            }
        
        # Extract results
        scrap_mix = {
            scrap: scrap_vars[scrap].value() 
            for scrap in self.scrap_data['Scrap_Type']
            if scrap_vars[scrap].value() > 1e-6 # Filter out negligible amounts
        }
        
        # Calculate total cost
        total_cost = sum([
            amount * self.scrap_data.loc[self.scrap_data['Scrap_Type'] == scrap, 'COST'].values[0]
            for scrap, amount in scrap_mix.items()
        ])
        
        # Calculate resulting composition
        resulting_composition = {}
        for element in self.elements:
            element_total = sum([
                amount * self.scrap_data.loc[self.scrap_data['Scrap_Type'] == scrap, element].values[0]
                for scrap, amount in scrap_mix.items()
            ])
            resulting_composition[element] = element_total / amount_needed
        
        return {
            'status': 'optimal',
            'scrap_mix': scrap_mix,
            'total_cost': total_cost,
            'total_amount': amount_needed,
            'resulting_composition': resulting_composition,
            'cost_per_unit': total_cost / amount_needed
        }
    
    def optimize_batch(self, batch_requirements):
        """
        Optimize formulations for multiple products in a batch.
        
        Args:
            batch_requirements (dict): Dictionary mapping product names to required amounts.
            
        Returns:
            dict: Dictionary containing optimization results for each product.
        """
        results = {}
        
        # Initialize available amounts for batch processing
        available_amounts = self.scrap_data['Available_Amount'].copy()
        
        # Process each product in the batch
        for product_name, amount_needed in batch_requirements.items():
            # Create a copy of the scrap data with updated available amounts
            temp_scrap_data = self.scrap_data.copy()
            temp_scrap_data['Available_Amount'] = available_amounts
            
            # Use a temporary optimizer with updated scrap data
            temp_optimizer = AlloyOptimizer(temp_scrap_data, self.composition_requirements)
            result = temp_optimizer.optimize_single_product(product_name, amount_needed)
            
            if result['status'] == 'optimal':
                # Update available amounts for next product
                for scrap, amount in result['scrap_mix'].items():
                    scrap_idx = self.scrap_data[self.scrap_data['Scrap_Type'] == scrap].index[0]
                    available_amounts[scrap_idx] -= amount
                
                # Store result
                results[product_name] = result
            else:
                # If optimization failed for any product, return the error
                results[product_name] = result
        
        # Calculate total batch cost
        total_batch_cost = sum([result['total_cost'] for result in results.values() 
                               if result['status'] == 'optimal'])
        
        # Calculate total scrap usage
        total_scrap_usage = {}
        for product_name, result in results.items():
            if result['status'] == 'optimal':
                for scrap, amount in result['scrap_mix'].items():
                    if scrap in total_scrap_usage:
                        total_scrap_usage[scrap] += amount
                    else:
                        total_scrap_usage[scrap] = amount
        
        return {
            'product_results': results,
            'total_batch_cost': total_batch_cost,
            'total_scrap_usage': total_scrap_usage
        }

def preprocess_scrap_data(df):
    """
    Preprocess scrap data to ensure correct format.
    
    Args:
        df (pandas.DataFrame): Raw scrap data.
        
    Returns:
        pandas.DataFrame: Processed scrap data.
    """
    # Ensure all numeric columns are float
    numeric_cols = ['COST', 'SI', 'FE', 'CU', 'MN', 'MG', 'Available_Amount']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill NaN values with 0 for composition columns
    composition_cols = ['SI', 'FE', 'CU', 'MN', 'MG']
    for col in composition_cols:
        if col in df.columns:
            df[col].fillna(0, inplace=True)
    
    return df

def preprocess_composition_requirements(df):
    """
    Preprocess composition requirements to ensure correct format.
    
    Args:
        df (pandas.DataFrame): Raw composition requirements.
        
    Returns:
        pandas.DataFrame: Processed composition requirements.
    """
    # Ensure all numeric columns are float
    for col in df.columns:
        if col != 'Product' and col != 'Amount':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convert Amount to float
    if 'Amount' in df.columns:
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    return df