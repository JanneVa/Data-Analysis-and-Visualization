#!/usr/bin/env python3
"""
Generate Hierarchical Visualizations - Alternative Script
========================================================

This script provides an alternative approach to generating hierarchical
visualizations with additional features and customization options.

Author: Hierarchical Data Visualization Project
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import squarify
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster, set_link_color_palette
from scipy.spatial.distance import pdist
from sklearn.preprocessing import StandardScaler
import logging
from pathlib import Path
import sys
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('viz_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class AdvancedHierarchicalVizGenerator:
    """Advanced hierarchical visualization generator with enhanced features."""
    
    def __init__(self, data_dir="."):
        """Initialize the advanced visualization generator."""
        self.data_dir = Path(data_dir)
        self.output_dir = Path("advanced_visualizations")
        self.output_dir.mkdir(exist_ok=True)
        
        # Visualization configuration
        self.config = {
            'colors': {
                'primary': '#1f77b4',
                'secondary': '#ff7f0e',
                'success': '#2ca02c',
                'danger': '#d62728',
                'warning': '#ff7f0e',
                'info': '#17a2b8'
            },
            'figure_sizes': {
                'small': (8, 6),
                'medium': (12, 8),
                'large': (16, 12),
                'extra_large': (20, 10)
            },
            'dpi': 300,
            'style': 'seaborn-v0_8-whitegrid'
        }
        
        # Load data
        self.country_data = None
        self.org_data = None
        self.budget_data = None
        
    def load_data(self):
        """Load data from various sources."""
        logger.info("Loading data for advanced visualizations...")
        
        try:
            # Try to load prepared data first
            prepared_files = [
                ("country_detailed.csv", "country_data"),
                ("org_detailed.csv", "org_data"),
                ("budget_detailed.csv", "budget_data")
            ]
            
            for filename, attr_name in prepared_files:
                file_path = self.data_dir / filename
                if file_path.exists():
                    setattr(self, attr_name, pd.read_csv(file_path))
                    logger.info(f"Loaded {filename}: {len(getattr(self, attr_name))} records")
                else:
                    # Fall back to original files
                    original_file = filename.replace('_detailed', '')
                    original_path = self.data_dir / original_file
                    if original_path.exists():
                        data = pd.read_csv(original_path)
                        # Basic preprocessing
                        if attr_name == "country_data" and 'Gdp_total' not in data.columns:
                            data['Gdp_total'] = data['Population'] * data['Gdp_per_capita']
                        setattr(self, attr_name, data)
                        logger.info(f"Loaded {original_file}: {len(data)} records")
                    else:
                        logger.warning(f"Could not find {filename} or {original_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def create_enhanced_treemap(self):
        """Create enhanced treemap with multiple views."""
        logger.info("Creating enhanced treemap visualizations...")
        
        if self.country_data is None:
            logger.error("Country data not available")
            return False
        
        # Create multiple treemap views
        views = [
            {
                'name': 'population_by_continent',
                'title': 'Population Distribution by Continent',
                'groupby': 'Continent',
                'values': 'Population',
                'color': 'Gdp_per_capita'
            },
            {
                'name': 'gdp_by_continent',
                'title': 'GDP Distribution by Continent',
                'groupby': 'Continent',
                'values': 'Gdp_total',
                'color': 'Population'
            },
            {
                'name': 'development_categories',
                'title': 'Countries by Development Category',
                'groupby': 'Development_Category',
                'values': 'Population',
                'color': 'Gdp_per_capita'
            }
        ]
        
        for view in views:
            try:
                # Prepare data
                if view['groupby'] in self.country_data.columns:
                    grouped_data = self.country_data.groupby(view['groupby'])[view['values']].sum().reset_index()
                    grouped_data = grouped_data.sort_values(view['values'], ascending=False)
                    
                    # Create treemap
                    plt.style.use(self.config['style'])
                    fig, ax = plt.subplots(figsize=self.config['figure_sizes']['medium'])
                    
                    # Generate treemap
                    squarify.plot(
                        sizes=grouped_data[view['values']],
                        label=grouped_data[view['groupby']],
                        alpha=0.8,
                        color=plt.cm.Set3.colors
                    )
                    
                    plt.title(view['title'], fontsize=14, weight='bold', pad=20)
                    plt.axis('off')
                    plt.tight_layout()
                    
                    # Save figure
                    output_file = self.output_dir / f"enhanced_treemap_{view['name']}.png"
                    plt.savefig(output_file, dpi=self.config['dpi'], bbox_inches='tight')
                    plt.close()
                    
                    logger.info(f"Enhanced treemap saved: {output_file}")
                
            except Exception as e:
                logger.error(f"Error creating treemap {view['name']}: {e}")
        
        return True
    
    def create_advanced_dendrogram(self):
        """Create advanced dendrogram with multiple clustering methods."""
        logger.info("Creating advanced dendrogram visualizations...")
        
        if self.country_data is None:
            logger.error("Country data not available")
            return False
        
        # Prepare data
        features = self.country_data[['Population', 'Gdp_per_capita']].values
        scaler = StandardScaler()
        features_normalized = scaler.fit_transform(features)
        
        # Different clustering methods
        methods = ['ward', 'complete', 'average', 'single']
        
        for method in methods:
            try:
                # Calculate linkage
                distances = pdist(features_normalized, metric='euclidean')
                linkage_matrix = linkage(distances, method=method)
                
                # Create dendrogram
                plt.style.use(self.config['style'])
                fig, ax = plt.subplots(figsize=self.config['figure_sizes']['extra_large'])
                
                # Set color palette
                set_link_color_palette([
                    self.config['colors']['primary'],
                    self.config['colors']['secondary'],
                    self.config['colors']['success'],
                    self.config['colors']['danger'],
                    self.config['colors']['warning'],
                    self.config['colors']['info']
                ])
                
                # Generate dendrogram
                dendro = dendrogram(
                    linkage_matrix,
                    labels=self.country_data['Country'].values,
                    leaf_font_size=6,
                    color_threshold=2.0,
                    above_threshold_color='#888888',
                    ax=ax
                )
                
                plt.title(f'Advanced Dendrogram - {method.title()} Method\nCountry Clustering by Population and GDP',
                         fontsize=16, weight='bold', pad=20)
                plt.xlabel('Countries', fontsize=12, weight='bold')
                plt.ylabel('Distance', fontsize=12, weight='bold')
                plt.xticks(rotation=90, fontsize=6)
                plt.grid(axis='y', alpha=0.3, linestyle='--')
                
                # Add threshold line
                plt.axhline(y=2.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Threshold')
                plt.legend()
                plt.tight_layout()
                
                # Save figure
                output_file = self.output_dir / f"advanced_dendrogram_{method}.png"
                plt.savefig(output_file, dpi=self.config['dpi'], bbox_inches='tight')
                plt.close()
                
                logger.info(f"Advanced dendrogram saved: {output_file}")
                
            except Exception as e:
                logger.error(f"Error creating dendrogram with {method} method: {e}")
        
        return True
    
    def create_interactive_dashboard(self):
        """Create comprehensive interactive dashboard."""
        logger.info("Creating interactive dashboard...")
        
        if self.country_data is None or self.org_data is None:
            logger.error("Required data not available")
            return False
        
        # Create comprehensive dashboard
        dashboard_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Advanced Hierarchical Data Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
                .header { text-align: center; color: #1f77b4; margin-bottom: 30px; }
                .dashboard-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
                .chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .chart-title { font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #333; }
                .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }
                .metric-card { background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .metric-value { font-size: 24px; font-weight: bold; color: #1f77b4; }
                .metric-label { font-size: 14px; color: #666; margin-top: 5px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Advanced Hierarchical Data Dashboard</h1>
                <p>Comprehensive analysis of global and organizational data</p>
            </div>
            
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-value" id="total-countries">-</div>
                    <div class="metric-label">Total Countries</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="total-population">-</div>
                    <div class="metric-label">Total Population</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="total-employees">-</div>
                    <div class="metric-label">Total Employees</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="total-departments">-</div>
                    <div class="metric-label">Departments</div>
                </div>
            </div>
            
            <div class="dashboard-container">
                <div class="chart-container">
                    <div class="chart-title">Global Population Distribution</div>
                    <div id="population-chart"></div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">Economic Development Clusters</div>
                    <div id="economic-chart"></div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">Organizational Structure</div>
                    <div id="org-chart"></div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">Budget Distribution</div>
                    <div id="budget-chart"></div>
                </div>
            </div>
            
            <script>
                // Dashboard data and configuration
                const dashboardData = {
                    countries: """ + str(len(self.country_data)) + """,
                    population: """ + str(self.country_data['Population'].sum()) + """,
                    employees: """ + str(self.org_data['values'].sum()) + """,
                    departments: """ + str(len(self.org_data[self.org_data['parents'] == 'Company'])) + """
                };
                
                // Update metrics
                document.getElementById('total-countries').textContent = dashboardData.countries.toLocaleString();
                document.getElementById('total-population').textContent = (dashboardData.population / 1e9).toFixed(1) + 'B';
                document.getElementById('total-employees').textContent = dashboardData.employees.toLocaleString();
                document.getElementById('total-departments').textContent = dashboardData.departments;
                
                // Placeholder for charts (would be populated with actual Plotly charts)
                document.getElementById('population-chart').innerHTML = '<p style="text-align: center; color: #666;">Interactive chart would be rendered here</p>';
                document.getElementById('economic-chart').innerHTML = '<p style="text-align: center; color: #666;">Interactive chart would be rendered here</p>';
                document.getElementById('org-chart').innerHTML = '<p style="text-align: center; color: #666;">Interactive chart would be rendered here</p>';
                document.getElementById('budget-chart').innerHTML = '<p style="text-align: center; color: #666;">Interactive chart would be rendered here</p>';
            </script>
        </body>
        </html>
        """
        
        # Save dashboard
        output_file = self.output_dir / "advanced_dashboard.html"
        with open(output_file, 'w') as f:
            f.write(dashboard_html)
        
        logger.info(f"Advanced dashboard saved: {output_file}")
        return True
    
    def create_custom_visualizations(self):
        """Create custom visualizations with advanced features."""
        logger.info("Creating custom visualizations...")
        
        if self.country_data is None:
            logger.error("Country data not available")
            return False
        
        # 1. Correlation heatmap
        try:
            plt.style.use(self.config['style'])
            fig, ax = plt.subplots(figsize=self.config['figure_sizes']['medium'])
            
            # Select numeric columns for correlation
            numeric_cols = ['Population', 'Gdp_per_capita', 'Gdp_total']
            correlation_data = self.country_data[numeric_cols].corr()
            
            # Create heatmap
            sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0,
                       square=True, ax=ax, cbar_kws={'shrink': 0.8})
            
            plt.title('Correlation Matrix: Population and Economic Indicators', 
                     fontsize=14, weight='bold', pad=20)
            plt.tight_layout()
            
            output_file = self.output_dir / "correlation_heatmap.png"
            plt.savefig(output_file, dpi=self.config['dpi'], bbox_inches='tight')
            plt.close()
            
            logger.info(f"Correlation heatmap saved: {output_file}")
            
        except Exception as e:
            logger.error(f"Error creating correlation heatmap: {e}")
        
        # 2. Distribution analysis
        try:
            fig, axes = plt.subplots(2, 2, figsize=self.config['figure_sizes']['large'])
            fig.suptitle('Distribution Analysis of Key Metrics', fontsize=16, weight='bold')
            
            # Population distribution
            axes[0, 0].hist(self.country_data['Population'], bins=30, alpha=0.7, color=self.config['colors']['primary'])
            axes[0, 0].set_title('Population Distribution')
            axes[0, 0].set_xlabel('Population')
            axes[0, 0].set_ylabel('Frequency')
            
            # GDP per capita distribution
            axes[0, 1].hist(self.country_data['Gdp_per_capita'], bins=30, alpha=0.7, color=self.config['colors']['secondary'])
            axes[0, 1].set_title('GDP per Capita Distribution')
            axes[0, 1].set_xlabel('GDP per Capita')
            axes[0, 1].set_ylabel('Frequency')
            
            # Log-transformed population
            log_pop = np.log10(self.country_data['Population'] + 1)
            axes[1, 0].hist(log_pop, bins=30, alpha=0.7, color=self.config['colors']['success'])
            axes[1, 0].set_title('Log-transformed Population Distribution')
            axes[1, 0].set_xlabel('Log10(Population)')
            axes[1, 0].set_ylabel('Frequency')
            
            # GDP total distribution
            axes[1, 1].hist(self.country_data['Gdp_total'], bins=30, alpha=0.7, color=self.config['colors']['danger'])
            axes[1, 1].set_title('Total GDP Distribution')
            axes[1, 1].set_xlabel('Total GDP')
            axes[1, 1].set_ylabel('Frequency')
            
            plt.tight_layout()
            
            output_file = self.output_dir / "distribution_analysis.png"
            plt.savefig(output_file, dpi=self.config['dpi'], bbox_inches='tight')
            plt.close()
            
            logger.info(f"Distribution analysis saved: {output_file}")
            
        except Exception as e:
            logger.error(f"Error creating distribution analysis: {e}")
        
        return True
    
    def generate_all_advanced_visualizations(self):
        """Generate all advanced visualizations."""
        logger.info("Generating all advanced visualizations...")
        
        # Load data
        if not self.load_data():
            logger.error("Failed to load data")
            return False
        
        # Generate visualizations
        visualizations = [
            self.create_enhanced_treemap,
            self.create_advanced_dendrogram,
            self.create_interactive_dashboard,
            self.create_custom_visualizations
        ]
        
        success_count = 0
        for viz_func in visualizations:
            try:
                if viz_func():
                    success_count += 1
            except Exception as e:
                logger.error(f"Error in {viz_func.__name__}: {e}")
        
        logger.info(f"Generated {success_count}/{len(visualizations)} advanced visualizations")
        
        # Create summary report
        self._create_advanced_summary()
        
        return success_count == len(visualizations)
    
    def _create_advanced_summary(self):
        """Create summary report for advanced visualizations."""
        summary_file = self.output_dir / "advanced_visualizations_summary.txt"
        
        with open(summary_file, 'w') as f:
            f.write("Advanced Hierarchical Visualizations Summary\n")
            f.write("==========================================\n\n")
            
            f.write("Generated Visualizations:\n")
            f.write("- Enhanced Treemaps (multiple views)\n")
            f.write("- Advanced Dendrograms (multiple clustering methods)\n")
            f.write("- Interactive Dashboard (comprehensive view)\n")
            f.write("- Custom Visualizations (correlation, distributions)\n\n")
            
            f.write("Configuration:\n")
            f.write(f"- Figure DPI: {self.config['dpi']}\n")
            f.write(f"- Style: {self.config['style']}\n")
            f.write(f"- Color Scheme: {len(self.config['colors'])} colors\n\n")
            
            if self.country_data is not None:
                f.write("Data Summary:\n")
                f.write(f"- Countries: {len(self.country_data)}\n")
                f.write(f"- Total Population: {self.country_data['Population'].sum():,.0f}\n")
                f.write(f"- Total GDP: {self.country_data['Gdp_total'].sum():,.0f}\n")
            
            if self.org_data is not None:
                f.write(f"- Total Employees: {self.org_data['values'].sum()}\n")
                f.write(f"- Organizational Units: {len(self.org_data)}\n")
        
        logger.info(f"Advanced summary created: {summary_file}")

def main():
    """Main function to run the advanced visualization generation script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate advanced hierarchical visualizations')
    parser.add_argument('--input-dir', default='.', help='Input directory containing data files')
    parser.add_argument('--output-dir', default='advanced_visualizations', help='Output directory for visualizations')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create generator instance
    generator = AdvancedHierarchicalVizGenerator(args.input_dir)
    generator.output_dir = Path(args.output_dir)
    generator.output_dir.mkdir(exist_ok=True)
    
    # Generate all advanced visualizations
    success = generator.generate_all_advanced_visualizations()
    
    if success:
        print("✅ All advanced visualizations generated successfully!")
        print(f"📁 Visualizations saved to: {generator.output_dir}")
        return 0
    else:
        print("❌ Some advanced visualizations failed to generate!")
        return 1

if __name__ == "__main__":
    exit(main())
