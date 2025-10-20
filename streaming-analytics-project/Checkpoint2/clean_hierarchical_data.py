#!/usr/bin/env python3
"""
Clean Hierarchical Data Script
==============================

This script cleans and prepares hierarchical data for visualization analysis.
It handles data validation, cleaning, and preprocessing for both country
and organizational datasets.

Author: Hierarchical Data Visualization Project
Date: 2024
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_cleaning.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class HierarchicalDataCleaner:
    """Class for cleaning and preparing hierarchical data."""
    
    def __init__(self, data_dir="."):
        """Initialize the data cleaner with data directory."""
        self.data_dir = Path(data_dir)
        self.country_data = None
        self.org_data = None
        self.cleaned_country_data = None
        self.cleaned_org_data = None
        
    def load_data(self):
        """Load raw data files."""
        logger.info("Loading raw data files...")
        
        try:
            # Load country data
            country_file = self.data_dir / "country_gdp_population.csv"
            if country_file.exists():
                self.country_data = pd.read_csv(country_file)
                logger.info(f"Loaded country data: {len(self.country_data)} records")
            else:
                logger.error(f"Country data file not found: {country_file}")
                return False
            
            # Load organizational data
            org_file = self.data_dir / "org_structure.csv"
            if org_file.exists():
                self.org_data = pd.read_csv(org_file)
                logger.info(f"Loaded organizational data: {len(self.org_data)} records")
            else:
                logger.error(f"Organizational data file not found: {org_file}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def validate_country_data(self):
        """Validate country data structure and content."""
        logger.info("Validating country data...")
        
        required_columns = ['Continent', 'Country', 'Population', 'Gdp_per_capita']
        missing_columns = [col for col in required_columns if col not in self.country_data.columns]
        
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        # Check for duplicate countries
        duplicates = self.country_data['Country'].duplicated().sum()
        if duplicates > 0:
            logger.warning(f"Found {duplicates} duplicate countries")
        
        # Check data types
        numeric_columns = ['Population', 'Gdp_per_capita']
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(self.country_data[col]):
                logger.warning(f"Column {col} is not numeric, attempting conversion...")
                self.country_data[col] = pd.to_numeric(self.country_data[col], errors='coerce')
        
        logger.info("Country data validation completed")
        return True
    
    def validate_org_data(self):
        """Validate organizational data structure and content."""
        logger.info("Validating organizational data...")
        
        required_columns = ['labels', 'parents', 'values']
        missing_columns = [col for col in required_columns if col not in self.org_data.columns]
        
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        # Check for duplicate labels
        duplicates = self.org_data['labels'].duplicated().sum()
        if duplicates > 0:
            logger.warning(f"Found {duplicates} duplicate labels")
        
        # Check data types
        if not pd.api.types.is_numeric_dtype(self.org_data['values']):
            logger.warning("Values column is not numeric, attempting conversion...")
            self.org_data['values'] = pd.to_numeric(self.org_data['values'], errors='coerce')
        
        # Validate hierarchy structure
        root_nodes = self.org_data[self.org_data['parents'] == '']
        if len(root_nodes) != 1:
            logger.warning(f"Expected 1 root node, found {len(root_nodes)}")
        
        logger.info("Organizational data validation completed")
        return True
    
    def clean_country_data(self):
        """Clean and preprocess country data."""
        logger.info("Cleaning country data...")
        
        # Create a copy for cleaning
        self.cleaned_country_data = self.country_data.copy()
        
        # Remove rows with missing critical data
        initial_count = len(self.cleaned_country_data)
        self.cleaned_country_data = self.cleaned_country_data.dropna(
            subset=['Population', 'Gdp_per_capita']
        )
        removed_count = initial_count - len(self.cleaned_country_data)
        
        if removed_count > 0:
            logger.info(f"Removed {removed_count} rows with missing data")
        
        # Handle outliers using IQR method
        for column in ['Population', 'Gdp_per_capita']:
            Q1 = self.cleaned_country_data[column].quantile(0.25)
            Q3 = self.cleaned_country_data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((self.cleaned_country_data[column] < lower_bound) | 
                       (self.cleaned_country_data[column] > upper_bound)).sum()
            
            if outliers > 0:
                logger.info(f"Found {outliers} outliers in {column}")
                # Cap outliers instead of removing them
                self.cleaned_country_data[column] = self.cleaned_country_data[column].clip(
                    lower_bound, upper_bound
                )
        
        # Create derived columns
        self.cleaned_country_data['Gdp_total'] = (
            self.cleaned_country_data['Population'] * 
            self.cleaned_country_data['Gdp_per_capita']
        )
        
        # Standardize country names
        self.cleaned_country_data['Country'] = self.cleaned_country_data['Country'].str.strip()
        self.cleaned_country_data['Continent'] = self.cleaned_country_data['Continent'].str.strip()
        
        # Sort by population for consistent ordering
        self.cleaned_country_data = self.cleaned_country_data.sort_values('Population', ascending=False)
        
        logger.info(f"Country data cleaning completed: {len(self.cleaned_country_data)} records")
        return True
    
    def clean_org_data(self):
        """Clean and preprocess organizational data."""
        logger.info("Cleaning organizational data...")
        
        # Create a copy for cleaning
        self.cleaned_org_data = self.org_data.copy()
        
        # Remove rows with missing data
        initial_count = len(self.cleaned_org_data)
        self.cleaned_org_data = self.cleaned_org_data.dropna(subset=['labels', 'values'])
        removed_count = initial_count - len(self.cleaned_org_data)
        
        if removed_count > 0:
            logger.info(f"Removed {removed_count} rows with missing data")
        
        # Standardize text fields
        self.cleaned_org_data['labels'] = self.cleaned_org_data['labels'].str.strip()
        self.cleaned_org_data['parents'] = self.cleaned_org_data['parents'].str.strip()
        
        # Ensure values are positive
        negative_values = (self.cleaned_org_data['values'] < 0).sum()
        if negative_values > 0:
            logger.warning(f"Found {negative_values} negative values, setting to 0")
            self.cleaned_org_data['values'] = self.cleaned_org_data['values'].clip(lower=0)
        
        # Validate hierarchy integrity
        self._validate_hierarchy()
        
        logger.info(f"Organizational data cleaning completed: {len(self.cleaned_org_data)} records")
        return True
    
    def _validate_hierarchy(self):
        """Validate organizational hierarchy integrity."""
        logger.info("Validating organizational hierarchy...")
        
        # Check that all parent references exist
        all_labels = set(self.cleaned_org_data['labels'])
        parent_references = set(self.cleaned_org_data['parents'])
        parent_references.discard('')  # Remove empty string (root node)
        
        missing_parents = parent_references - all_labels
        if missing_parents:
            logger.warning(f"Found orphaned parent references: {missing_parents}")
        
        # Check for circular references (basic check)
        for _, row in self.cleaned_org_data.iterrows():
            if row['parents'] != '':
                # Check if parent is a descendant of current node
                if self._is_circular_reference(row['labels'], row['parents']):
                    logger.warning(f"Potential circular reference: {row['labels']} -> {row['parents']}")
    
    def _is_circular_reference(self, node, parent):
        """Check for circular references in hierarchy."""
        visited = set()
        current = parent
        
        while current != '' and current not in visited:
            visited.add(current)
            parent_row = self.cleaned_org_data[self.cleaned_org_data['labels'] == current]
            if len(parent_row) > 0:
                current = parent_row.iloc[0]['parents']
            else:
                break
        
        return current == node
    
    def generate_summary_statistics(self):
        """Generate summary statistics for cleaned data."""
        logger.info("Generating summary statistics...")
        
        summary = {}
        
        if self.cleaned_country_data is not None:
            country_stats = {
                'total_countries': len(self.cleaned_country_data),
                'total_population': self.cleaned_country_data['Population'].sum(),
                'total_gdp': self.cleaned_country_data['Gdp_total'].sum(),
                'avg_gdp_per_capita': self.cleaned_country_data['Gdp_per_capita'].mean(),
                'continents': self.cleaned_country_data['Continent'].nunique(),
                'population_range': (
                    self.cleaned_country_data['Population'].min(),
                    self.cleaned_country_data['Population'].max()
                ),
                'gdp_per_capita_range': (
                    self.cleaned_country_data['Gdp_per_capita'].min(),
                    self.cleaned_country_data['Gdp_per_capita'].max()
                )
            }
            summary['country_data'] = country_stats
        
        if self.cleaned_org_data is not None:
            org_stats = {
                'total_units': len(self.cleaned_org_data),
                'total_employees': self.cleaned_org_data['values'].sum(),
                'hierarchy_levels': self._count_hierarchy_levels(),
                'departments': len(self.cleaned_org_data[self.cleaned_org_data['parents'] == 'Company']),
                'teams': len(self.cleaned_org_data[self.cleaned_org_data['parents'] != 'Company']),
                'employee_range': (
                    self.cleaned_org_data['values'].min(),
                    self.cleaned_org_data['values'].max()
                )
            }
            summary['org_data'] = org_stats
        
        return summary
    
    def _count_hierarchy_levels(self):
        """Count the number of hierarchy levels in organizational data."""
        levels = 0
        current_level = set([''])
        
        while current_level:
            next_level = set()
            for parent in current_level:
                children = self.cleaned_org_data[self.cleaned_org_data['parents'] == parent]['labels']
                next_level.update(children)
            if next_level:
                levels += 1
            current_level = next_level
        
        return levels
    
    def save_cleaned_data(self, output_dir="."):
        """Save cleaned data to files."""
        logger.info("Saving cleaned data...")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        if self.cleaned_country_data is not None:
            country_output = output_path / "country_gdp_population_cleaned.csv"
            self.cleaned_country_data.to_csv(country_output, index=False)
            logger.info(f"Saved cleaned country data to: {country_output}")
        
        if self.cleaned_org_data is not None:
            org_output = output_path / "org_structure_cleaned.csv"
            self.cleaned_org_data.to_csv(org_output, index=False)
            logger.info(f"Saved cleaned organizational data to: {org_output}")
        
        # Save summary statistics
        summary = self.generate_summary_statistics()
        summary_file = output_path / "data_cleaning_summary.txt"
        
        with open(summary_file, 'w') as f:
            f.write("Data Cleaning Summary\n")
            f.write("====================\n\n")
            
            if 'country_data' in summary:
                f.write("Country Data:\n")
                for key, value in summary['country_data'].items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
            
            if 'org_data' in summary:
                f.write("Organizational Data:\n")
                for key, value in summary['org_data'].items():
                    f.write(f"  {key}: {value}\n")
        
        logger.info(f"Saved summary statistics to: {summary_file}")
    
    def run_cleaning_pipeline(self):
        """Run the complete data cleaning pipeline."""
        logger.info("Starting data cleaning pipeline...")
        
        # Load data
        if not self.load_data():
            logger.error("Failed to load data")
            return False
        
        # Validate data
        if not self.validate_country_data():
            logger.error("Country data validation failed")
            return False
        
        if not self.validate_org_data():
            logger.error("Organizational data validation failed")
            return False
        
        # Clean data
        if not self.clean_country_data():
            logger.error("Country data cleaning failed")
            return False
        
        if not self.clean_org_data():
            logger.error("Organizational data cleaning failed")
            return False
        
        # Save cleaned data
        self.save_cleaned_data()
        
        logger.info("Data cleaning pipeline completed successfully")
        return True

def main():
    """Main function to run the data cleaning script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean hierarchical data for visualization')
    parser.add_argument('--input-dir', default='.', help='Input directory containing data files')
    parser.add_argument('--output-dir', default='.', help='Output directory for cleaned data')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create cleaner instance
    cleaner = HierarchicalDataCleaner(args.input_dir)
    
    # Run cleaning pipeline
    success = cleaner.run_cleaning_pipeline()
    
    if success:
        print("✅ Data cleaning completed successfully!")
        return 0
    else:
        print("❌ Data cleaning failed!")
        return 1

if __name__ == "__main__":
    exit(main())
