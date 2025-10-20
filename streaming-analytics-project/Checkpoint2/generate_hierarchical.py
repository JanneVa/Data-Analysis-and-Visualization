#!/usr/bin/env python3
"""
Generate Hierarchical Visualizations Script
==========================================

This script automatically generates all hierarchical visualizations
from prepared data, creating both static and interactive versions.

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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('visualization_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class HierarchicalVisualizationGenerator:
    """Class for generating hierarchical visualizations."""
    
    def __init__(self, data_dir="."):
        """Initialize the visualization generator with data directory."""
        self.data_dir = Path(data_dir)
        self.output_dir = Path("generated_visualizations")
        self.output_dir.mkdir(exist_ok=True)
        
        # Load prepared data
        self.country_data = None
        self.org_data = None
        self.budget_data = None
        self.metadata = None
        self.insights = None
        
    def load_prepared_data(self):
        """Load prepared datasets."""
        logger.info("Loading prepared data...")
        
        try:
            # Load country data
            country_file = self.data_dir / "country_detailed.csv"
            if country_file.exists():
                self.country_data = pd.read_csv(country_file)
                logger.info(f"Loaded country data: {len(self.country_data)} records")
            else:
                logger.error(f"Country data file not found: {country_file}")
                return False
            
            # Load organizational data
            org_file = self.data_dir / "org_detailed.csv"
            if org_file.exists():
                self.org_data = pd.read_csv(org_file)
                logger.info(f"Loaded organizational data: {len(self.org_data)} records")
            else:
                logger.error(f"Organizational data file not found: {org_file}")
                return False
            
            # Load budget data
            budget_file = self.data_dir / "budget_detailed.csv"
            if budget_file.exists():
                self.budget_data = pd.read_csv(budget_file)
                logger.info(f"Loaded budget data: {len(self.budget_data)} records")
            else:
                logger.error(f"Budget data file not found: {budget_file}")
                return False
            
            # Load metadata
            metadata_file = self.data_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    self.metadata = json.load(f)
                logger.info("Loaded visualization metadata")
            
            # Load insights
            insights_file = self.data_dir / "insights.json"
            if insights_file.exists():
                with open(insights_file, 'r') as f:
                    self.insights = json.load(f)
                logger.info("Loaded insights data")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading prepared data: {e}")
            return False
    
    def generate_treemap_static(self):
        """Generate static treemap visualization."""
        logger.info("Generating static treemap...")
        
        # Prepare data
        continent_pop = self.country_data.groupby('Continent')['Population'].sum().reset_index()
        continent_pop = continent_pop.sort_values('Population', ascending=False)
        
        # Create figure
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Generate treemap
        squarify.plot(sizes=continent_pop['Population'], 
                     label=continent_pop['Continent'],
                     alpha=0.8,
                     color=plt.cm.Set3.colors)
        
        plt.title('Static Treemap: Population Distribution by Continent', 
                 fontsize=16, weight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        
        # Save figure
        output_file = self.output_dir / "treemap_static.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Static treemap saved to: {output_file}")
        return True
    
    def generate_treemap_interactive(self):
        """Generate interactive treemap visualization."""
        logger.info("Generating interactive treemap...")
        
        # Create interactive treemap
        fig = px.treemap(self.country_data,
                        path=['Continent', 'Country'],
                        values='Population',
                        color='Gdp_per_capita',
                        color_continuous_scale='Blues',
                        title='Interactive Treemap: Population vs GDP per Capita')
        
        fig.update_layout(width=1000, height=600)
        
        # Save as HTML
        output_file = self.output_dir / "treemap_interactive.html"
        fig.write_html(output_file)
        
        logger.info(f"Interactive treemap saved to: {output_file}")
        return True
    
    def generate_dendrogram(self):
        """Generate dendrogram visualization."""
        logger.info("Generating dendrogram...")
        
        # Prepare data for clustering
        features = self.country_data[['Population', 'Gdp_per_capita']].values
        scaler = StandardScaler()
        features_normalized = scaler.fit_transform(features)
        
        # Calculate linkage
        distances = pdist(features_normalized, metric='euclidean')
        linkage_matrix = linkage(distances, method='ward')
        
        # Create dendrogram
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(20, 10))
        
        # Set color palette
        set_link_color_palette(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#96CEB4', '#DDA0DD'])
        
        # Generate dendrogram
        dendro = dendrogram(linkage_matrix,
                           labels=self.country_data['Country'].values,
                           leaf_font_size=8,
                           color_threshold=2.0,
                           above_threshold_color='#888888',
                           ax=ax)
        
        plt.title('Hierarchical Clustering Dendrogram\nCountries grouped by Population and GDP per capita',
                 fontsize=16, weight='bold', pad=20)
        plt.xlabel('Countries', fontsize=12, weight='bold')
        plt.ylabel('Euclidean Distance', fontsize=12, weight='bold')
        plt.xticks(rotation=90, fontsize=8)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add threshold line
        plt.axhline(y=2.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Threshold')
        plt.legend()
        plt.tight_layout()
        
        # Save figure
        output_file = self.output_dir / "dendrogram.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Dendrogram saved to: {output_file}")
        return True
    
    def generate_sunburst_geographic(self):
        """Generate geographic sunburst chart."""
        logger.info("Generating geographic sunburst chart...")
        
        # Create sunburst chart
        fig = px.sunburst(self.country_data,
                         path=['Continent', 'Country'],
                         values='Population',
                         color='Gdp_per_capita',
                         color_continuous_scale='Blues',
                         title='Geographic Sunburst: Population Distribution by Continent and Country')
        
        fig.update_layout(width=900, height=900)
        
        # Save as HTML
        output_file = self.output_dir / "sunburst_geographic.html"
        fig.write_html(output_file)
        
        logger.info(f"Geographic sunburst saved to: {output_file}")
        return True
    
    def generate_sunburst_organizational(self):
        """Generate organizational sunburst chart."""
        logger.info("Generating organizational sunburst chart...")
        
        # Create organizational sunburst
        fig = go.Figure(go.Sunburst(
            labels=self.org_data['labels'],
            parents=self.org_data['parents'],
            values=self.org_data['values'],
            branchvalues="total",
            marker=dict(
                colorscale='Viridis',
                cmid=50,
                line=dict(color='white', width=2)
            ),
            hovertemplate='<b>%{label}</b><br>Employees: %{value}<br>Percentage: %{percentParent:.1%}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Organizational Sunburst: Employee Distribution by Department and Team',
            width=900,
            height=900
        )
        
        # Save as HTML
        output_file = self.output_dir / "sunburst_organizational.html"
        fig.write_html(output_file)
        
        logger.info(f"Organizational sunburst saved to: {output_file}")
        return True
    
    def generate_circular_treemap_economic(self):
        """Generate economic circular treemap."""
        logger.info("Generating economic circular treemap...")
        
        # Create circular treemap
        fig = px.icicle(self.country_data,
                       path=['Continent', 'Country'],
                       values='Gdp_total',
                       color='Gdp_per_capita',
                       color_continuous_scale='Reds',
                       title='Economic Circular Treemap: GDP Total Distribution')
        
        fig.update_layout(width=1000, height=700)
        
        # Save as HTML
        output_file = self.output_dir / "circular_treemap_economic.html"
        fig.write_html(output_file)
        
        logger.info(f"Economic circular treemap saved to: {output_file}")
        return True
    
    def generate_circular_treemap_budget(self):
        """Generate budget circular treemap."""
        logger.info("Generating budget circular treemap...")
        
        # Create budget circular treemap
        fig = px.icicle(self.budget_data,
                       path=['parents', 'labels'],
                       values='budget',
                       color='budget',
                       color_continuous_scale='Greens',
                       title='Budget Circular Treemap: Budget Distribution by Department and Team')
        
        fig.update_layout(width=1000, height=700)
        
        # Save as HTML
        output_file = self.output_dir / "circular_treemap_budget.html"
        fig.write_html(output_file)
        
        logger.info(f"Budget circular treemap saved to: {output_file}")
        return True
    
    def generate_comparative_analysis(self):
        """Generate comparative analysis visualization."""
        logger.info("Generating comparative analysis...")
        
        # Create side-by-side comparison
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Comparative Analysis: Different Visualization Techniques', 
                    fontsize=16, weight='bold')
        
        # 1. Population distribution (bar chart)
        continent_pop = self.country_data.groupby('Continent')['Population'].sum().reset_index()
        continent_pop = continent_pop.sort_values('Population', ascending=False)
        
        axes[0, 0].bar(continent_pop['Continent'], continent_pop['Population'])
        axes[0, 0].set_title('Population by Continent (Bar Chart)')
        axes[0, 0].set_ylabel('Population')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. GDP per capita distribution (box plot)
        axes[0, 1].boxplot([self.country_data[self.country_data['Continent'] == continent]['Gdp_per_capita'].values 
                           for continent in continent_pop['Continent']],
                          labels=continent_pop['Continent'])
        axes[0, 1].set_title('GDP per Capita Distribution by Continent')
        axes[0, 1].set_ylabel('GDP per Capita')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Organizational structure (pie chart)
        dept_data = self.org_data[self.org_data['parents'] == 'Company']
        axes[1, 0].pie(dept_data['values'], labels=dept_data['labels'], autopct='%1.1f%%')
        axes[1, 0].set_title('Employee Distribution by Department')
        
        # 4. Budget efficiency (scatter plot)
        dept_budget = self.budget_data[self.budget_data['parents'] == 'Company']
        axes[1, 1].scatter(dept_budget['values'], dept_budget['budget'])
        for i, dept in enumerate(dept_budget['labels']):
            axes[1, 1].annotate(dept, (dept_budget.iloc[i]['values'], dept_budget.iloc[i]['budget']))
        axes[1, 1].set_xlabel('Number of Employees')
        axes[1, 1].set_ylabel('Budget')
        axes[1, 1].set_title('Budget vs Employees by Department')
        
        plt.tight_layout()
        
        # Save figure
        output_file = self.output_dir / "comparative_analysis.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Comparative analysis saved to: {output_file}")
        return True
    
    def generate_insights_dashboard(self):
        """Generate insights dashboard visualization."""
        logger.info("Generating insights dashboard...")
        
        if self.insights is None:
            logger.warning("No insights data available, skipping insights dashboard")
            return True
        
        # Create insights summary
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Key Insights Dashboard', fontsize=16, weight='bold')
        
        # 1. Geographic insights
        if 'geographic' in self.insights:
            geo_insights = self.insights['geographic']
            axes[0, 0].text(0.1, 0.8, f"Most Populous Continent: {geo_insights['most_populous_continent']}", 
                           fontsize=12, weight='bold')
            axes[0, 0].text(0.1, 0.6, f"Population Share: {geo_insights['population_percentage']:.1f}%", 
                           fontsize=10)
            axes[0, 0].text(0.1, 0.4, f"Richest Continent: {geo_insights['richest_continent']}", 
                           fontsize=12, weight='bold')
            axes[0, 0].text(0.1, 0.2, f"GDP Share: {geo_insights['gdp_percentage']:.1f}%", 
                           fontsize=10)
            axes[0, 0].set_title('Geographic Insights')
            axes[0, 0].set_xlim(0, 1)
            axes[0, 0].set_ylim(0, 1)
            axes[0, 0].axis('off')
        
        # 2. Organizational insights
        if 'organizational' in self.insights:
            org_insights = self.insights['organizational']
            axes[0, 1].text(0.1, 0.8, f"Largest Department: {org_insights['largest_department']}", 
                           fontsize=12, weight='bold')
            axes[0, 1].text(0.1, 0.6, f"Employees: {org_insights['largest_dept_employees']}", 
                           fontsize=10)
            axes[0, 1].text(0.1, 0.4, f"Highest Budget: {org_insights['highest_budget_department']}", 
                           fontsize=12, weight='bold')
            axes[0, 1].text(0.1, 0.2, f"Budget: ${org_insights['highest_budget_amount']:,.0f}", 
                           fontsize=10)
            axes[0, 1].set_title('Organizational Insights')
            axes[0, 1].set_xlim(0, 1)
            axes[0, 1].set_ylim(0, 1)
            axes[0, 1].axis('off')
        
        # 3. Clustering insights
        if 'clustering' in self.insights:
            cluster_insights = self.insights['clustering']
            axes[1, 0].text(0.1, 0.8, f"Population-GDP Correlation: {cluster_insights['population_gdp_correlation']:.3f}", 
                           fontsize=12, weight='bold')
            axes[1, 0].text(0.1, 0.6, f"Interpretation: {cluster_insights['correlation_interpretation']}", 
                           fontsize=10)
            axes[1, 0].text(0.1, 0.4, f"Countries Analyzed: {cluster_insights['countries_analyzed']}", 
                           fontsize=10)
            axes[1, 0].set_title('Clustering Insights')
            axes[1, 0].set_xlim(0, 1)
            axes[1, 0].set_ylim(0, 1)
            axes[1, 0].axis('off')
        
        # 4. Summary metrics
        if self.metadata:
            country_meta = self.metadata.get('country_data', {})
            org_meta = self.metadata.get('org_data', {})
            
            axes[1, 1].text(0.1, 0.8, f"Total Countries: {country_meta.get('total_countries', 0)}", 
                           fontsize=12, weight='bold')
            axes[1, 1].text(0.1, 0.6, f"Total Employees: {org_meta.get('total_employees', 0)}", 
                           fontsize=10)
            axes[1, 1].text(0.1, 0.4, f"Continents: {len(country_meta.get('continents', []))}", 
                           fontsize=10)
            axes[1, 1].text(0.1, 0.2, f"Departments: {len(org_meta.get('departments', []))}", 
                           fontsize=10)
            axes[1, 1].set_title('Summary Metrics')
            axes[1, 1].set_xlim(0, 1)
            axes[1, 1].set_ylim(0, 1)
            axes[1, 1].axis('off')
        
        plt.tight_layout()
        
        # Save figure
        output_file = self.output_dir / "insights_dashboard.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Insights dashboard saved to: {output_file}")
        return True
    
    def generate_all_visualizations(self):
        """Generate all hierarchical visualizations."""
        logger.info("Generating all hierarchical visualizations...")
        
        # Load data
        if not self.load_prepared_data():
            logger.error("Failed to load prepared data")
            return False
        
        # Generate visualizations
        visualizations = [
            self.generate_treemap_static,
            self.generate_treemap_interactive,
            self.generate_dendrogram,
            self.generate_sunburst_geographic,
            self.generate_sunburst_organizational,
            self.generate_circular_treemap_economic,
            self.generate_circular_treemap_budget,
            self.generate_comparative_analysis,
            self.generate_insights_dashboard
        ]
        
        success_count = 0
        for viz_func in visualizations:
            try:
                if viz_func():
                    success_count += 1
            except Exception as e:
                logger.error(f"Error generating visualization {viz_func.__name__}: {e}")
        
        logger.info(f"Generated {success_count}/{len(visualizations)} visualizations successfully")
        
        # Create index file
        self._create_visualization_index()
        
        return success_count == len(visualizations)
    
    def _create_visualization_index(self):
        """Create an index file listing all generated visualizations."""
        index_file = self.output_dir / "index.html"
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hierarchical Data Visualizations</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #1f77b4; }
                h2 { color: #ff7f0e; }
                .visualization { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
                .visualization a { color: #1f77b4; text-decoration: none; font-weight: bold; }
                .visualization a:hover { text-decoration: underline; }
                .description { color: #666; margin-top: 10px; }
            </style>
        </head>
        <body>
            <h1>📊 Hierarchical Data Visualizations</h1>
            <p>Generated visualizations for hierarchical data analysis project.</p>
            
            <h2>Static Visualizations</h2>
            <div class="visualization">
                <a href="treemap_static.png">Static Treemap</a>
                <div class="description">Population distribution by continent using squarify</div>
            </div>
            
            <div class="visualization">
                <a href="dendrogram.png">Dendrogram</a>
                <div class="description">Hierarchical clustering of countries by population and GDP</div>
            </div>
            
            <div class="visualization">
                <a href="comparative_analysis.png">Comparative Analysis</a>
                <div class="description">Side-by-side comparison of different visualization techniques</div>
            </div>
            
            <div class="visualization">
                <a href="insights_dashboard.png">Insights Dashboard</a>
                <div class="description">Key insights and summary metrics</div>
            </div>
            
            <h2>Interactive Visualizations</h2>
            <div class="visualization">
                <a href="treemap_interactive.html">Interactive Treemap</a>
                <div class="description">Interactive population and GDP visualization with Plotly</div>
            </div>
            
            <div class="visualization">
                <a href="sunburst_geographic.html">Geographic Sunburst</a>
                <div class="description">Hierarchical navigation from continents to countries</div>
            </div>
            
            <div class="visualization">
                <a href="sunburst_organizational.html">Organizational Sunburst</a>
                <div class="description">Company structure from departments to teams</div>
            </div>
            
            <div class="visualization">
                <a href="circular_treemap_economic.html">Economic Circular Treemap</a>
                <div class="description">GDP distribution across continents and countries</div>
            </div>
            
            <div class="visualization">
                <a href="circular_treemap_budget.html">Budget Circular Treemap</a>
                <div class="description">Budget allocation across departments and teams</div>
            </div>
            
            <hr>
            <p><em>Generated by Hierarchical Data Visualization Project</em></p>
        </body>
        </html>
        """
        
        with open(index_file, 'w') as f:
            f.write(html_content)
        
        logger.info(f"Visualization index created: {index_file}")

def main():
    """Main function to run the visualization generation script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate hierarchical visualizations')
    parser.add_argument('--input-dir', default='.', help='Input directory containing prepared data')
    parser.add_argument('--output-dir', default='generated_visualizations', help='Output directory for visualizations')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create generator instance
    generator = HierarchicalVisualizationGenerator(args.input_dir)
    generator.output_dir = Path(args.output_dir)
    generator.output_dir.mkdir(exist_ok=True)
    
    # Generate all visualizations
    success = generator.generate_all_visualizations()
    
    if success:
        print("✅ All visualizations generated successfully!")
        print(f"📁 Visualizations saved to: {generator.output_dir}")
        return 0
    else:
        print("❌ Some visualizations failed to generate!")
        return 1

if __name__ == "__main__":
    exit(main())
