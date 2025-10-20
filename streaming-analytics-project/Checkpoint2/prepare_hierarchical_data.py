#!/usr/bin/env python3
"""
Prepare Hierarchical Data Script
================================

This script prepares hierarchical data for visualization by creating
derived datasets, calculating metrics, and structuring data for
different visualization techniques.

Author: Hierarchical Data Visualization Project
Date: 2024
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
import sys
import json
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_preparation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class HierarchicalDataPreparer:
    """Class for preparing hierarchical data for visualization."""
    
    def __init__(self, data_dir="."):
        """Initialize the data preparer with data directory."""
        self.data_dir = Path(data_dir)
        self.country_data = None
        self.org_data = None
        self.prepared_datasets = {}
        
    def load_cleaned_data(self):
        """Load cleaned data files."""
        logger.info("Loading cleaned data files...")
        
        try:
            # Try to load cleaned data first
            cleaned_country_file = self.data_dir / "country_gdp_population_cleaned.csv"
            cleaned_org_file = self.data_dir / "org_structure_cleaned.csv"
            
            if cleaned_country_file.exists():
                self.country_data = pd.read_csv(cleaned_country_file)
                logger.info(f"Loaded cleaned country data: {len(self.country_data)} records")
            else:
                # Fall back to original data
                country_file = self.data_dir / "country_gdp_population.csv"
                if country_file.exists():
                    self.country_data = pd.read_csv(country_file)
                    logger.info(f"Loaded original country data: {len(self.country_data)} records")
                else:
                    logger.error("No country data file found")
                    return False
            
            if cleaned_org_file.exists():
                self.org_data = pd.read_csv(cleaned_org_file)
                logger.info(f"Loaded cleaned organizational data: {len(self.org_data)} records")
            else:
                # Fall back to original data
                org_file = self.data_dir / "org_structure.csv"
                if org_file.exists():
                    self.org_data = pd.read_csv(org_file)
                    logger.info(f"Loaded original organizational data: {len(self.org_data)} records")
                else:
                    logger.error("No organizational data file found")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def prepare_country_data(self):
        """Prepare country data for different visualization techniques."""
        logger.info("Preparing country data for visualization...")
        
        if self.country_data is None:
            logger.error("Country data not loaded")
            return False
        
        # Create a copy for preparation
        country_prep = self.country_data.copy()
        
        # Ensure required columns exist
        if 'Gdp_total' not in country_prep.columns:
            country_prep['Gdp_total'] = (
                country_prep['Population'] * country_prep['Gdp_per_capita']
            )
        
        # Create continent-level aggregations
        continent_data = country_prep.groupby('Continent').agg({
            'Population': 'sum',
            'Gdp_total': 'sum',
            'Gdp_per_capita': 'mean',
            'Country': 'count'
        }).reset_index()
        
        continent_data.columns = [
            'Continent', 'Total_Population', 'Total_GDP', 
            'Avg_GDP_per_capita', 'Country_Count'
        ]
        
        # Calculate percentages
        total_population = continent_data['Total_Population'].sum()
        total_gdp = continent_data['Total_GDP'].sum()
        
        continent_data['Population_Percentage'] = (
            continent_data['Total_Population'] / total_population * 100
        )
        continent_data['GDP_Percentage'] = (
            continent_data['Total_GDP'] / total_gdp * 100
        )
        
        # Sort by population
        continent_data = continent_data.sort_values('Total_Population', ascending=False)
        
        # Create country-level metrics
        country_prep['Population_Rank'] = country_prep['Population'].rank(ascending=False)
        country_prep['GDP_Rank'] = country_prep['Gdp_total'].rank(ascending=False)
        country_prep['GDP_per_capita_Rank'] = country_prep['Gdp_per_capita'].rank(ascending=False)
        
        # Create development categories
        gdp_per_capita_quartiles = country_prep['Gdp_per_capita'].quantile([0.25, 0.5, 0.75])
        
        def categorize_development(gdp_per_capita):
            if gdp_per_capita <= gdp_per_capita_quartiles[0.25]:
                return 'Low Income'
            elif gdp_per_capita <= gdp_per_capita_quartiles[0.5]:
                return 'Lower Middle Income'
            elif gdp_per_capita <= gdp_per_capita_quartiles[0.75]:
                return 'Upper Middle Income'
            else:
                return 'High Income'
        
        country_prep['Development_Category'] = country_prep['Gdp_per_capita'].apply(categorize_development)
        
        # Store prepared datasets
        self.prepared_datasets['country_detailed'] = country_prep
        self.prepared_datasets['continent_summary'] = continent_data
        
        logger.info("Country data preparation completed")
        return True
    
    def prepare_org_data(self):
        """Prepare organizational data for different visualization techniques."""
        logger.info("Preparing organizational data for visualization...")
        
        if self.org_data is None:
            logger.error("Organizational data not loaded")
            return False
        
        # Create a copy for preparation
        org_prep = self.org_data.copy()
        
        # Create budget data
        budget_data = org_prep.copy()
        base_budget_per_employee = 100000
        budget_data['budget'] = budget_data['values'] * base_budget_per_employee
        
        # Apply budget multipliers for different departments
        budget_multipliers = {
            'Engineering': 1.2,  # 20% more budget
            'Product': 1.1,      # 10% more budget
            'Sales': 1.3,        # 30% more budget
            'Operations': 0.9,   # 10% less budget
            'Company': 1.0       # No adjustment
        }
        
        for dept, multiplier in budget_multipliers.items():
            mask = budget_data['labels'].str.contains(dept, na=False) | (budget_data['parents'] == dept)
            budget_data.loc[mask, 'budget'] *= multiplier
        
        # Calculate hierarchy levels
        def calculate_level(label, parents_dict, level=0):
            if label == '' or label not in parents_dict:
                return level
            parent = parents_dict[label]
            if parent == '':
                return level + 1
            return calculate_level(parent, parents_dict, level + 1)
        
        parents_dict = dict(zip(org_prep['labels'], org_prep['parents']))
        org_prep['hierarchy_level'] = org_prep['labels'].apply(
            lambda x: calculate_level(x, parents_dict)
        )
        budget_data['hierarchy_level'] = org_prep['hierarchy_level']
        
        # Create department-level aggregations
        dept_data = org_prep[org_prep['parents'] == 'Company'].copy()
        dept_data = dept_data.merge(
            budget_data[['labels', 'budget']], 
            on='labels', 
            how='left'
        )
        
        # Calculate metrics
        total_employees = org_prep['values'].sum()
        total_budget = budget_data['budget'].sum()
        
        dept_data['employee_percentage'] = (dept_data['values'] / total_employees * 100)
        dept_data['budget_percentage'] = (dept_data['budget'] / total_budget * 100)
        dept_data['budget_per_employee'] = (dept_data['budget'] / dept_data['values'])
        
        # Create team-level data
        team_data = org_prep[org_prep['parents'] != 'Company'].copy()
        team_data = team_data.merge(
            budget_data[['labels', 'budget']], 
            on='labels', 
            how='left'
        )
        
        # Calculate team metrics
        team_data['budget_per_employee'] = (team_data['budget'] / team_data['values'])
        team_data['efficiency_score'] = (
            team_data['values'] / team_data['budget_per_employee'] * 1000
        )  # Higher is more efficient
        
        # Store prepared datasets
        self.prepared_datasets['org_detailed'] = org_prep
        self.prepared_datasets['budget_detailed'] = budget_data
        self.prepared_datasets['dept_summary'] = dept_data
        self.prepared_datasets['team_summary'] = team_data
        
        logger.info("Organizational data preparation completed")
        return True
    
    def create_clustering_data(self):
        """Create data specifically for clustering analysis."""
        logger.info("Creating clustering data...")
        
        if self.country_data is None:
            logger.error("Country data not loaded")
            return False
        
        # Prepare features for clustering
        clustering_data = self.country_data[['Country', 'Population', 'Gdp_per_capita']].copy()
        
        # Remove any missing values
        clustering_data = clustering_data.dropna()
        
        # Log transform population to reduce skewness
        clustering_data['Population_log'] = np.log10(clustering_data['Population'] + 1)
        
        # Create normalized features
        from sklearn.preprocessing import StandardScaler
        
        features = clustering_data[['Population_log', 'Gdp_per_capita']].values
        scaler = StandardScaler()
        features_normalized = scaler.fit_transform(features)
        
        clustering_data['Population_normalized'] = features_normalized[:, 0]
        clustering_data['GDP_per_capita_normalized'] = features_normalized[:, 1]
        
        # Store clustering data
        self.prepared_datasets['clustering_data'] = clustering_data
        self.prepared_datasets['clustering_scaler'] = scaler
        
        logger.info("Clustering data creation completed")
        return True
    
    def create_visualization_metadata(self):
        """Create metadata for visualization configuration."""
        logger.info("Creating visualization metadata...")
        
        metadata = {
            'country_data': {
                'total_countries': len(self.country_data) if self.country_data is not None else 0,
                'continents': list(self.country_data['Continent'].unique()) if self.country_data is not None else [],
                'population_range': {
                    'min': float(self.country_data['Population'].min()) if self.country_data is not None else 0,
                    'max': float(self.country_data['Population'].max()) if self.country_data is not None else 0
                },
                'gdp_per_capita_range': {
                    'min': float(self.country_data['Gdp_per_capita'].min()) if self.country_data is not None else 0,
                    'max': float(self.country_data['Gdp_per_capita'].max()) if self.country_data is not None else 0
                }
            },
            'org_data': {
                'total_units': len(self.org_data) if self.org_data is not None else 0,
                'total_employees': int(self.org_data['values'].sum()) if self.org_data is not None else 0,
                'departments': list(self.org_data[self.org_data['parents'] == 'Company']['labels']) if self.org_data is not None else [],
                'hierarchy_levels': max(self.prepared_datasets.get('org_detailed', pd.DataFrame())['hierarchy_level']) if 'org_detailed' in self.prepared_datasets else 0
            },
            'visualization_config': {
                'color_schemes': {
                    'geographic': 'Blues',
                    'economic': 'Reds',
                    'organizational': 'Viridis',
                    'budget': 'Greens'
                },
                'figure_sizes': {
                    'static': [12, 8],
                    'interactive': [900, 900],
                    'dashboard': [1000, 600]
                }
            }
        }
        
        self.prepared_datasets['metadata'] = metadata
        
        logger.info("Visualization metadata creation completed")
        return True
    
    def generate_insights(self):
        """Generate key insights from prepared data."""
        logger.info("Generating insights...")
        
        insights = {}
        
        # Country insights
        if 'continent_summary' in self.prepared_datasets:
            continent_data = self.prepared_datasets['continent_summary']
            
            # Find top continent by population
            top_continent_pop = continent_data.loc[continent_data['Total_Population'].idxmax()]
            
            # Find top continent by GDP
            top_continent_gdp = continent_data.loc[continent_data['Total_GDP'].idxmax()]
            
            insights['geographic'] = {
                'most_populous_continent': top_continent_pop['Continent'],
                'population_percentage': float(top_continent_pop['Population_Percentage']),
                'richest_continent': top_continent_gdp['Continent'],
                'gdp_percentage': float(top_continent_gdp['GDP_Percentage']),
                'total_continents': len(continent_data)
            }
        
        # Organizational insights
        if 'dept_summary' in self.prepared_datasets:
            dept_data = self.prepared_datasets['dept_summary']
            
            # Find largest department
            largest_dept = dept_data.loc[dept_data['values'].idxmax()]
            
            # Find department with highest budget
            highest_budget_dept = dept_data.loc[dept_data['budget'].idxmax()]
            
            # Find most efficient department
            most_efficient_dept = dept_data.loc[dept_data['budget_per_employee'].idxmin()]
            
            insights['organizational'] = {
                'largest_department': largest_dept['labels'],
                'largest_dept_employees': int(largest_dept['values']),
                'highest_budget_department': highest_budget_dept['labels'],
                'highest_budget_amount': float(highest_budget_dept['budget']),
                'most_efficient_department': most_efficient_dept['labels'],
                'efficiency_score': float(most_efficient_dept['budget_per_employee'])
            }
        
        # Clustering insights
        if 'clustering_data' in self.prepared_datasets:
            clustering_data = self.prepared_datasets['clustering_data']
            
            # Calculate correlation
            correlation = clustering_data['Population'].corr(clustering_data['Gdp_per_capita'])
            
            insights['clustering'] = {
                'population_gdp_correlation': float(correlation),
                'correlation_interpretation': 'negative' if correlation < 0 else 'positive',
                'countries_analyzed': len(clustering_data)
            }
        
        self.prepared_datasets['insights'] = insights
        
        logger.info("Insights generation completed")
        return True
    
    def save_prepared_data(self, output_dir="."):
        """Save all prepared datasets to files."""
        logger.info("Saving prepared data...")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save datasets
        for name, dataset in self.prepared_datasets.items():
            if isinstance(dataset, pd.DataFrame):
                output_file = output_path / f"{name}.csv"
                dataset.to_csv(output_file, index=False)
                logger.info(f"Saved {name} to: {output_file}")
            elif isinstance(dataset, dict):
                output_file = output_path / f"{name}.json"
                with open(output_file, 'w') as f:
                    json.dump(dataset, f, indent=2)
                logger.info(f"Saved {name} to: {output_file}")
        
        # Save summary report
        self._save_preparation_report(output_path)
        
        logger.info("Data preparation completed successfully")
    
    def _save_preparation_report(self, output_path):
        """Save a summary report of data preparation."""
        report_file = output_path / "data_preparation_report.txt"
        
        with open(report_file, 'w') as f:
            f.write("Data Preparation Report\n")
            f.write("======================\n\n")
            
            f.write("Prepared Datasets:\n")
            for name, dataset in self.prepared_datasets.items():
                if isinstance(dataset, pd.DataFrame):
                    f.write(f"  {name}: {len(dataset)} records, {len(dataset.columns)} columns\n")
                elif isinstance(dataset, dict):
                    f.write(f"  {name}: {len(dataset)} items\n")
            
            f.write("\nKey Insights:\n")
            if 'insights' in self.prepared_datasets:
                insights = self.prepared_datasets['insights']
                for category, data in insights.items():
                    f.write(f"\n{category.title()}:\n")
                    for key, value in data.items():
                        f.write(f"  {key}: {value}\n")
        
        logger.info(f"Saved preparation report to: {report_file}")
    
    def run_preparation_pipeline(self):
        """Run the complete data preparation pipeline."""
        logger.info("Starting data preparation pipeline...")
        
        # Load data
        if not self.load_cleaned_data():
            logger.error("Failed to load data")
            return False
        
        # Prepare country data
        if not self.prepare_country_data():
            logger.error("Country data preparation failed")
            return False
        
        # Prepare organizational data
        if not self.prepare_org_data():
            logger.error("Organizational data preparation failed")
            return False
        
        # Create clustering data
        if not self.create_clustering_data():
            logger.error("Clustering data creation failed")
            return False
        
        # Create metadata
        if not self.create_visualization_metadata():
            logger.error("Metadata creation failed")
            return False
        
        # Generate insights
        if not self.generate_insights():
            logger.error("Insights generation failed")
            return False
        
        # Save prepared data
        self.save_prepared_data()
        
        logger.info("Data preparation pipeline completed successfully")
        return True

def main():
    """Main function to run the data preparation script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Prepare hierarchical data for visualization')
    parser.add_argument('--input-dir', default='.', help='Input directory containing data files')
    parser.add_argument('--output-dir', default='.', help='Output directory for prepared data')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create preparer instance
    preparer = HierarchicalDataPreparer(args.input_dir)
    
    # Run preparation pipeline
    success = preparer.run_preparation_pipeline()
    
    if success:
        print("✅ Data preparation completed successfully!")
        return 0
    else:
        print("❌ Data preparation failed!")
        return 1

if __name__ == "__main__":
    exit(main())
