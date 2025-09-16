# Video Streaming Platform Performance Analysis

## Project Overview
A comprehensive data science project analyzing video streaming platform performance using synthetic datasets. This project demonstrates end-to-end data engineering, statistical analysis, and visualization capabilities.

## Team Structure (5 Members)
- **Data Engineer**: Database design, ETL pipeline development, data infrastructure
- **Data Analyst**: Statistical analysis, hypothesis testing, predictive modeling
- **Visualization Specialist**: Interactive dashboards, executive presentations, data storytelling
- **Backend Developer**: API development, database optimization, system integration
- **Project Manager**: Coordination, documentation, presentation preparation

## Key Technologies
- **Languages**: Python, R, SQL
- **Databases**: PostgreSQL (Relational), MongoDB (NoSQL)
- **Visualization**: Tableau, Power BI, Plotly, Streamlit
- **Tools**: Git, Docker, Apache Airflow, Jupyter Notebooks

## Project Structure
```
video-streaming-analysis/
├── database/           # Database schemas and models
│   ├── sql/           # PostgreSQL schemas and queries
│   └── mongodb/       # MongoDB collections and queries
├── data/              # Data storage
│   ├── raw/           # Original synthetic datasets
│   ├── processed/     # Cleaned and transformed data
│   └── external/      # External reference data
├── src/               # Source code
│   ├── etl/           # ETL pipeline scripts
│   ├── analysis/      # Statistical analysis modules
│   └── visualization/ # Dashboard and visualization code
├── notebooks/         # Jupyter notebooks for exploration
├── dashboards/        # Interactive dashboards
├── docs/              # Documentation and presentations
├── scripts/           # Utility scripts
└── tests/             # Unit and integration tests
```

## Datasets
- **Users**: Demographics, subscription plans, preferences
- **Content**: Video metadata, categories, ratings, duration
- **Viewing Sessions**: Watch time, engagement metrics, device info
- **Performance**: Streaming quality, buffering events, error logs

## Deliverables
1. **Complete GitHub Repository** with all code and documentation
2. **15-minute Oral Presentation** with live demo
3. **Peer Review** documentation and feedback system

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- MongoDB 4.4+
- Git

### Installation
```bash
git clone <repository-url>
cd video-streaming-analysis
pip install -r requirements.txt
```

### Running the Project
```bash
# Generate synthetic data
python scripts/generate_data.py

# Run ETL pipeline
python src/etl/main.py

# Start analysis
jupyter notebook notebooks/
```

## Key Features
- **Database Design**: Both relational and NoSQL models with ER diagrams
- **Statistical Analysis**: Descriptive statistics, hypothesis testing, clustering, predictive modeling
- **Data Visualization**: Interactive dashboards and executive presentations
- **ETL Pipeline**: Automated data transformation with validation and monitoring
- **Performance Monitoring**: Real-time streaming quality analysis

## License
MIT License - see LICENSE file for details
