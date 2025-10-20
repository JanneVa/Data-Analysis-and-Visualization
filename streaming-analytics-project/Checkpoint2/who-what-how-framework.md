# Who-What-How Framework
## Audience, Action, and Data Strategy

### WHO - Target Audience

#### Primary Audience: Marco Antonelli - CEO of Terra Cotta Foods (TCF)
- **Background:** Chief Executive Officer of Europe's largest distributor of premium food products and raw materials
- **Company:** Terra Cotta Foods (TCF) - Giant food and beverage company, major distributor of basic products
- **Goals:** Evaluate economic viability and potential reach of TCF's supply chain in new markets (Latin America and Asia)
- **Pain Points:** Needs complex global data distilled into clear business metrics for strategic expansion decisions
- **Technical Level:** High at operational and financial levels, but needs complex data simplified into actionable business insights
- **Decision Context:** "Do we invest in Continent/Country X or Y?" and "What business line needs to be adjusted internally?"

#### Secondary Audience: TCF Strategic Planning Team
- **Background:** Business analysts and strategic planners supporting Marco's expansion decisions
- **Goals:** Provide data-driven recommendations for market entry and supply chain optimization
- **Pain Points:** Need to translate complex hierarchical data into strategic recommendations
- **Technical Level:** Intermediate analytical skills, focus on business outcomes

#### Tertiary Audience: TCF Board of Directors
- **Background:** Executive board members reviewing expansion strategy
- **Goals:** Understand market potential and risk assessment for investment decisions
- **Pain Points:** Need high-level insights without technical complexity
- **Technical Level:** Non-technical, focus on strategic implications

### WHAT - Data and Insights

#### Core Datasets
1. **Global Country Data (193 UN Member Countries)**
   - Population distribution across continents
   - GDP per capita and total GDP
   - Economic development patterns
   - Geographic hierarchy (Continent → Country)

2. **Tech Company Organizational Structure**
   - Employee distribution across departments
   - Budget allocation by teams
   - Organizational hierarchy (Company → Department → Team)
   - Resource efficiency metrics

#### Key Insights to Communicate
1. **Market Evaluation for TCF Expansion**
   - **Purchasing Power Hierarchy:** Which regions and countries show highest GDP (purchasing capacity) for TCF's premium food products
   - **Supply Risk Assessment:** How population (labor force/consumer base) correlates with economic potential in target markets
   - **Strategic Market Prioritization:** Clear ranking of countries/regions for TCF's Latin America and Asia expansion

2. **Supply Chain Optimization Insights**
   - **Distribution Center Placement:** Optimal locations based on economic potential and population density
   - **Supplier Diversification:** Geographic spread to mitigate geopolitical risks
   - **Market Penetration Strategy:** Population vs. purchasing power analysis for different product lines

3. **Business Decision Support**
   - **Investment Prioritization:** Which markets offer best ROI for TCF's expansion
   - **Risk Mitigation:** Understanding economic stability and market maturity
   - **Competitive Positioning:** Market size and economic development for strategic planning

#### Success Metrics
- **Strategic Clarity:** Marco can make "invest in X or Y" decisions within 5 minutes of viewing
- **Business Actionability:** Clear recommendations for TCF's expansion strategy
- **Risk Assessment:** Comprehensive understanding of market potential and supply chain risks
- **Executive Confidence:** Visualization conveys control and confidence over complex global supply chain decisions

### HOW - Data Strategy and Implementation

#### Data Collection Strategy
1. **Primary Data Sources**
   - World Bank API for country economic data
   - Rest Countries API for geographic information
   - Synthetic organizational data for tech company structure

2. **Data Quality Assurance**
   - Validation of UN member country list
   - Cross-referencing economic indicators
   - Consistency checks for organizational hierarchy

#### Data Processing Pipeline
1. **Extraction**
   - API calls to external data sources
   - CSV file imports for organizational data
   - Data validation and error handling

2. **Transformation**
   - Standardization of country names and regions
   - Calculation of derived metrics (GDP total, budget per employee)
   - Hierarchical structure creation

3. **Loading**
   - Clean CSV files for analysis
   - Structured data formats for visualization
   - Metadata documentation

#### Visualization Strategy
1. **Static Visualizations**
   - High-quality figures for reports and presentations
   - Consistent styling and color schemes
   - Clear annotations and labels

2. **Interactive Visualizations**
   - Plotly-based interactive charts
   - Hover information and tooltips
   - Zoom and filter capabilities

3. **Dashboard Integration**
   - Streamlit application for comprehensive view
   - Multiple visualization techniques in single interface
   - Export capabilities for further analysis

#### Communication Strategy
1. **Executive Presentation for Marco Antonelli**
   - **Strategic Dashboard:** High-level view of market opportunities and risks
   - **Investment Decision Framework:** Clear "go/no-go" criteria for market entry
   - **Supply Chain Optimization:** Distribution center placement and supplier diversification insights
   - **Time-Efficient:** 15-minute presentation with 30-minute Q&A for strategic decisions

2. **TCF Strategic Planning Team Documentation**
   - Detailed market analysis methodology
   - Country-specific recommendations and risk assessments
   - Implementation roadmap for expansion strategy
   - Technical details for follow-up analysis

3. **Board of Directors Summary**
   - Executive summary with key investment recommendations
   - Risk assessment and mitigation strategies
   - ROI projections and market potential analysis
   - Visual highlights for non-technical audience

#### Technology Stack
- **Data Processing:** pandas, numpy
- **Visualization:** matplotlib, seaborn, plotly, squarify
- **Clustering:** scipy, sklearn
- **Dashboard:** Streamlit
- **Documentation:** Jupyter notebooks, Markdown

#### Quality Assurance
1. **Code Quality**
   - Modular, reusable functions
   - Error handling and validation
   - Performance optimization

2. **Visualization Quality**
   - Consistent color schemes and styling
   - Clear, readable labels and annotations
   - Responsive design for different screen sizes

3. **Data Quality**
   - Validation of data accuracy
   - Handling of missing values
   - Cross-validation of results

#### Deployment Strategy
1. **Development Environment**
   - Jupyter notebooks for exploration and analysis
   - Version control with Git
   - Virtual environment for dependency management

2. **Production Environment**
   - Streamlit dashboard for interactive access
   - Static HTML exports for sharing
   - PDF reports for formal presentations

3. **Maintenance and Updates**
   - Regular data updates from APIs
   - Version control for code changes
   - Documentation updates for new features
