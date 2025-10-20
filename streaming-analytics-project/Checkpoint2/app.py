import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster, set_link_color_palette
from scipy.spatial.distance import pdist
from sklearn.preprocessing import StandardScaler

# Page configuration
st.set_page_config(
    page_title="Hierarchical Data Visualization Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📊 Hierarchical Data Visualization Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Comprehensive Analysis of Global Population, Economic Data, and Organizational Structures")

# Sidebar
st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Data loading
@st.cache_data
def load_data():
    """Load and cache the datasets"""
    try:
        country_data = pd.read_csv("country_gdp_population.csv")
        org_data = pd.read_csv("org_structure.csv")
        
        # Clean country data
        country_data_clean = country_data.dropna(subset=['Population', 'Gdp_per_capita'])
        country_data_clean['Gdp_total'] = country_data_clean['Population'] * country_data_clean['Gdp_per_capita']
        
        # Prepare budget data
        budget_data = org_data.copy()
        base_budget_per_employee = 100000
        budget_data['budget'] = budget_data['values'] * base_budget_per_employee
        
        # Apply budget multipliers
        budget_multipliers = {
            'Engineering': 1.2,
            'Product': 1.1,
            'Sales': 1.3,
            'Operations': 0.9,
            'Company': 1.0
        }
        
        for dept, multiplier in budget_multipliers.items():
            mask = budget_data['labels'].str.contains(dept, na=False) | (budget_data['parents'] == dept)
            budget_data.loc[mask, 'budget'] *= multiplier
        
        return country_data_clean, org_data, budget_data
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        return None, None, None

# Load data
country_data, org_data, budget_data = load_data()

if country_data is not None:
    # Sidebar controls
    st.sidebar.subheader(" Global Data Overview")
    
    total_population = country_data['Population'].sum()
    total_gdp = country_data['Gdp_total'].sum()
    avg_gdp_per_capita = country_data['Gdp_per_capita'].mean()
    num_countries = len(country_data)
    
    st.sidebar.metric("Total Population", f"{total_population:,.0f}")
    st.sidebar.metric("Total GDP", f"${total_gdp:,.0f}")
    st.sidebar.metric("Avg GDP per Capita", f"${avg_gdp_per_capita:,.0f}")
    st.sidebar.metric("Number of Countries", num_countries)
    
    if org_data is not None:
        st.sidebar.subheader(" Organizational Data")
        total_employees = org_data[org_data['parents'] == '']['values'].sum()
        total_budget = budget_data[budget_data['parents'] == '']['budget'].sum()
        
        st.sidebar.metric("Total Employees", total_employees)
        st.sidebar.metric("Total Budget", f"${total_budget:,.0f}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        " Global Analysis", 
        " Organizational Analysis", 
        " Comparative Analysis", 
        " Interactive Exploration",
        " Insights & Recommendations"
    ])
    
    with tab1:
        st.markdown('<h2 class="section-header">🌍 Global Population & Economic Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(" Population Distribution by Continent")
            
            # Static treemap
            continent_pop = country_data.groupby('Continent')['Population'].sum().reset_index()
            continent_pop = continent_pop.sort_values('Population', ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            squarify.plot(sizes=continent_pop['Population'], 
                         label=continent_pop['Continent'],
                         alpha=0.8,
                         color=plt.cm.Set3.colors)
            plt.title('Population Distribution by Continent', fontsize=14, weight='bold')
            plt.axis('off')
            st.pyplot(fig)
        
        with col2:
            st.subheader(" Interactive Global Treemap")
            
            # Interactive treemap
            fig = px.treemap(country_data,
                           path=['Continent', 'Country'],
                           values='Population',
                           color='Gdp_per_capita',
                           color_continuous_scale='Blues',
                           title='Population vs GDP per Capita')
            
            fig.update_layout(width=500, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Dendrogram
        st.subheader(" Country Clustering Analysis")
        
        # Prepare data for clustering
        features = country_data[['Population', 'Gdp_per_capita']].values
        scaler = StandardScaler()
        features_normalized = scaler.fit_transform(features)
        
        # Calculate linkage
        distances = pdist(features_normalized, metric='euclidean')
        linkage_matrix = linkage(distances, method='ward')
        
        # Create dendrogram
        fig, ax = plt.subplots(figsize=(15, 8))
        set_link_color_palette(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
        
        dendro = dendrogram(linkage_matrix,
                           labels=country_data['Country'].values,
                           leaf_font_size=8,
                           color_threshold=2.0,
                           above_threshold_color='#888888',
                           ax=ax)
        
        plt.title('Hierarchical Clustering of Countries by Population and GDP per Capita', 
                 fontsize=14, weight='bold')
        plt.xlabel('Countries', fontsize=12)
        plt.ylabel('Distance', fontsize=12)
        plt.xticks(rotation=90, fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab2:
        st.markdown('<h2 class="section-header">🏢 Organizational Structure Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(" Organizational Structure")
            
            # Sunburst for organizational structure
            fig = go.Figure(go.Sunburst(
                labels=org_data['labels'],
                parents=org_data['parents'],
                values=org_data['values'],
                branchvalues="total",
                marker=dict(
                    colorscale='Viridis',
                    cmid=50,
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>%{label}</b><br>Employees: %{value}<br>Percentage: %{percentParent:.1%}<extra></extra>'
            ))
            
            fig.update_layout(
                title='Organizational Structure - Employee Distribution',
                width=500,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💰 Budget Distribution")
            
            # Circular treemap for budget
            fig = px.icicle(budget_data,
                          path=['parents', 'labels'],
                          values='budget',
                          color='budget',
                          color_continuous_scale='Greens',
                          title='Budget Distribution by Department and Team')
            
            fig.update_layout(width=500, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Organizational metrics
        st.subheader(" Organizational Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dept_dist = org_data[org_data['parents'] == 'Company'][['labels', 'values']]
            st.write("**Department Distribution:**")
            for _, row in dept_dist.iterrows():
                percentage = (row['values'] / total_employees) * 100
                st.write(f"- {row['labels']}: {row['values']} ({percentage:.1f}%)")
        
        with col2:
            budget_analysis = budget_data.groupby('parents').agg({
                'budget': 'sum',
                'values': 'sum'
            }).round(0)
            budget_analysis = budget_analysis.sort_values('budget', ascending=False)
            st.write("**Budget by Department:**")
            for dept, row in budget_analysis.iterrows():
                if dept != '':
                    budget_percentage = (row['budget'] / total_budget) * 100
                    st.write(f"- {dept}: ${row['budget']:,.0f} ({budget_percentage:.1f}%)")
        
        with col3:
            st.write("**Key Insights:**")
            st.write("• Engineering has highest budget allocation")
            st.write("• Sales receives premium budget for growth")
            st.write("• Operations maintains efficient cost structure")
    
    with tab3:
        st.markdown('<h2 class="section-header">📊 Comparative Analysis</h2>', unsafe_allow_html=True)
        
        # Comparison table
        comparison_data = {
            'Technique': ['Treemap', 'Dendrogram', 'Sunburst', 'Circular Treemap'],
            'Best For': [
                'Proportional comparisons, space efficiency',
                'Pattern discovery, clustering analysis',
                'Hierarchical navigation, multi-level display',
                'Resource allocation, flow visualization'
            ],
            'Limitations': [
                'Limited depth, label overlap',
                'No magnitude display, complex interpretation',
                'Space constraints, readability issues',
                'Complexity with many levels'
            ],
            'Use Case': [
                'Executive presentations, quick comparisons',
                'Data exploration, pattern identification',
                'Organizational charts, geographic navigation',
                'Budget analysis, resource planning'
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Visualization comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(" Geographic Hierarchy")
            fig = px.sunburst(country_data,
                            path=['Continent', 'Country'],
                            values='Population',
                            color='Gdp_per_capita',
                            color_continuous_scale='Blues',
                            title='Geographic Hierarchy - Population Distribution')
            fig.update_layout(width=400, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader(" Economic Distribution")
            fig = px.icicle(country_data,
                          path=['Continent', 'Country'],
                          values='Gdp_total',
                          color='Gdp_per_capita',
                          color_continuous_scale='Reds',
                          title='Economic Distribution - GDP Total')
            fig.update_layout(width=400, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown('<h2 class="section-header">🔍 Interactive Exploration</h2>', unsafe_allow_html=True)
        
        # Interactive filters
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(" Country Filter")
            selected_continents = st.multiselect(
                "Select Continents:",
                options=country_data['Continent'].unique(),
                default=country_data['Continent'].unique()
            )
            
            filtered_data = country_data[country_data['Continent'].isin(selected_continents)]
        
        with col2:
            st.subheader(" Metric Selection")
            metric = st.selectbox(
                "Choose Metric:",
                options=['Population', 'Gdp_per_capita', 'Gdp_total'],
                index=0
            )
        
        # Dynamic visualization
        if len(filtered_data) > 0:
            fig = px.treemap(filtered_data,
                           path=['Continent', 'Country'],
                           values=metric,
                           color=metric,
                           color_continuous_scale='Viridis',
                           title=f'{metric} Distribution - Filtered View')
            
            fig.update_layout(width=800, height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Countries", len(filtered_data))
            with col2:
                st.metric(f"Total {metric}", f"{filtered_data[metric].sum():,.0f}")
            with col3:
                st.metric(f"Average {metric}", f"{filtered_data[metric].mean():,.0f}")
        
        # Top countries table
        st.subheader("🏆 Top Countries")
        top_countries = filtered_data.nlargest(10, metric)[['Country', 'Continent', metric]]
        st.dataframe(top_countries, use_container_width=True)
    
    with tab5:
        st.markdown('<h2 class="section-header">📈 Insights & Recommendations</h2>', unsafe_allow_html=True)
        
        # Key insights
        st.subheader("🔍 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🌍 Global Patterns:**
            - Asia dominates global population (60%+)
            - Economic power concentrated in specific regions
            - Negative correlation between population and GDP per capita
            - Countries cluster by development patterns, not geography
            """)
        
        with col2:
            st.markdown("""
            **🏢 Organizational Insights:**
            - Engineering and Sales receive highest budget allocation
            - Resource distribution reflects strategic priorities
            - Employee-to-budget ratios vary significantly
            - Hierarchical structure enables efficient resource management
            """)
        
        # Recommendations
        st.subheader(" Strategic Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **For Global Organizations:**
            1. Focus on high-population, emerging markets
            2. Consider economic efficiency, not just market size
            3. Use development clustering for market entry
            4. Optimize resource allocation based on patterns
            """)
        
        with col2:
            st.markdown("""
            **For Data Analysts:**
            1. Use multiple visualization techniques
            2. Always consider hierarchical relationships
            3. Compare results across different methods
            4. Select techniques based on analytical goals
            """)
        
        # Technical recommendations
        st.subheader("🛠️ Technical Recommendations")
        
        st.markdown("""
        **Visualization Best Practices:**
        - Use consistent color schemes across related visualizations
        - Provide interactive elements for detailed exploration
        - Ensure responsive design for different screen sizes
        - Implement accessibility features for all users
        
        **Data Quality:**
        - Validate data completeness and accuracy
        - Handle missing values appropriately
        - Cross-reference multiple data sources
        - Document data processing steps
        """)
        
        # Future enhancements
        st.subheader(" Future Enhancements")
        
        st.markdown("""
        **Potential Improvements:**
        - Add temporal analysis for trend identification
        - Implement 3D visualizations for complex hierarchies
        - Integrate machine learning for pattern detection
        - Add collaboration features for team analysis
        - Develop mobile-optimized interfaces
        """)

else:
    st.error(" Unable to load data files. Please ensure 'country_gdp_population.csv' and 'org_structure.csv' are in the same directory as this app.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p> Hierarchical Data Visualization Dashboard | Built with Streamlit & Plotly</p>
    <p>CheckPoint 2 - Hierarchical Data Visualization Analysis</p>
</div>
""", unsafe_allow_html=True)
