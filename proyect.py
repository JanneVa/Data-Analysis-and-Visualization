#!/usr/bin/env python3
"""
Video Streaming Platform Performance Analysis
Comprehensive analysis tool for streaming platform data
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Data Science Libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class VideoStreamingAnalyzer:
    """Main class for video streaming platform analysis"""
    
    def __init__(self, data_dir="."):
        self.data_dir = data_dir
        self.users_df = None
        self.sessions_df = None
        self.content_df = None
        self.merged_df = None
        
    def load_data(self):
        """Load all datasets"""
        print("Loading datasets...")
        
        # Load users data
        self.users_df = pd.read_csv(os.path.join(self.data_dir, 'users.csv'))
        print(f"Loaded {len(self.users_df)} users")
        
        # Load sessions data
        self.sessions_df = pd.read_csv(os.path.join(self.data_dir, 'viewing_sessions.csv'))
        print(f"Loaded {len(self.sessions_df)} viewing sessions")
        
        # Load content data
        with open(os.path.join(self.data_dir, 'content.json'), 'r') as f:
            content_data = json.load(f)
        self.content_df = pd.DataFrame(content_data['movies'])
        print(f"Loaded {len(self.content_df)} content items")
        
        # Convert date columns
        self.users_df['registration_date'] = pd.to_datetime(self.users_df['registration_date'])
        self.sessions_df['watch_date'] = pd.to_datetime(self.sessions_df['watch_date'])
        
        print("Data loading completed!")
        
    def create_merged_dataset(self):
        """Create comprehensive merged dataset for analysis"""
        print("Creating merged dataset...")
        
        # Merge sessions with users
        sessions_users = self.sessions_df.merge(
            self.users_df[['user_id', 'age', 'country', 'subscription_type', 'registration_date']], 
            on='user_id', 
            how='left'
        )
        
        # Merge with content
        self.merged_df = sessions_users.merge(
            self.content_df[['content_id', 'title', 'genre', 'duration_minutes', 'release_year', 'rating']], 
            on='content_id', 
            how='left'
        )
        
        # Create additional features
        self.merged_df['engagement_rate'] = self.merged_df['watch_duration_minutes'] / self.merged_df['duration_minutes']
        self.merged_df['is_high_quality'] = self.merged_df['quality_level'].isin(['HD', '4K'])
        self.merged_df['is_mobile'] = self.merged_df['device_type'] == 'Mobile'
        self.merged_df['user_age_group'] = pd.cut(self.merged_df['age'], 
                                                 bins=[0, 25, 35, 50, 100], 
                                                 labels=['18-25', '26-35', '36-50', '50+'])
        
        print(f"Merged dataset created with {len(self.merged_df)} records")
        
    def descriptive_statistics(self):
        """Generate comprehensive descriptive statistics"""
        print("\n" + "="*50)
        print("DESCRIPTIVE STATISTICS")
        print("="*50)
        
        # User statistics
        print("\nUSER STATISTICS:")
        print(f"Total Users: {self.users_df['user_id'].nunique():,}")
        print(f"Average Age: {self.users_df['age'].mean():.1f} years")
        print(f"Countries: {self.users_df['country'].nunique()}")
        print("\nSubscription Distribution:")
        print(self.users_df['subscription_type'].value_counts())
        
        # Session statistics
        print("\nSESSION STATISTICS:")
        print(f"Total Sessions: {len(self.sessions_df):,}")
        print(f"Average Session Duration: {self.sessions_df['watch_duration_minutes'].mean():.1f} minutes")
        print(f"Average Completion Rate: {self.sessions_df['completion_percentage'].mean():.1f}%")
        
        # Content statistics
        print("\nCONTENT STATISTICS:")
        print(f"Total Content Items: {len(self.content_df):,}")
        print(f"Average Duration: {self.content_df['duration_minutes'].mean():.1f} minutes")
        print(f"Average Rating: {self.content_df['rating'].mean():.2f}")
        
        # Quality and device distribution
        print("\nQUALITY LEVEL DISTRIBUTION:")
        print(self.sessions_df['quality_level'].value_counts())
        print("\nDEVICE TYPE DISTRIBUTION:")
        print(self.sessions_df['device_type'].value_counts())
        
    def hypothesis_testing(self):
        """Perform hypothesis tests"""
        print("\n" + "="*50)
        print("HYPOTHESIS TESTING")
        print("="*50)
        
        # Test 1: Subscription type vs completion rate
        print("\n1. SUBSCRIPTION TYPE vs COMPLETION RATE")
        subscription_groups = []
        for sub_type in self.merged_df['subscription_type'].unique():
            group_data = self.merged_df[self.merged_df['subscription_type'] == sub_type]['completion_percentage']
            subscription_groups.append(group_data)
        
        f_stat, p_value = stats.f_oneway(*subscription_groups)
        print(f"ANOVA F-statistic: {f_stat:.4f}")
        print(f"P-value: {p_value:.6f}")
        print(f"Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'}")
        
        # Test 2: Device type vs watch duration
        print("\n2. DEVICE TYPE vs WATCH DURATION")
        device_groups = []
        for device in self.merged_df['device_type'].unique():
            group_data = self.merged_df[self.merged_df['device_type'] == device]['watch_duration_minutes']
            device_groups.append(group_data)
        
        f_stat, p_value = stats.f_oneway(*device_groups)
        print(f"ANOVA F-statistic: {f_stat:.4f}")
        print(f"P-value: {p_value:.6f}")
        print(f"Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'}")
        
        # Test 3: Quality level vs completion rate (t-test)
        print("\n3. HIGH QUALITY vs COMPLETION RATE")
        high_quality = self.merged_df[self.merged_df['is_high_quality'] == True]['completion_percentage']
        low_quality = self.merged_df[self.merged_df['is_high_quality'] == False]['completion_percentage']
        
        t_stat, p_value = stats.ttest_ind(high_quality, low_quality)
        print(f"T-statistic: {t_stat:.4f}")
        print(f"P-value: {p_value:.6f}")
        print(f"Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'}")
        
    def user_clustering(self):
        """Perform user clustering analysis"""
        print("\n" + "="*50)
        print("USER CLUSTERING ANALYSIS")
        print("="*50)
        
        # Prepare features for clustering
        user_features = self.merged_df.groupby('user_id').agg({
            'session_id': 'count',
            'watch_duration_minutes': 'sum',
            'completion_percentage': 'mean',
            'content_id': 'nunique',
            'is_high_quality': 'mean',
            'age': 'first'
        }).reset_index()
        
        user_features.columns = ['user_id', 'total_sessions', 'total_watch_time', 
                               'avg_completion', 'unique_content', 'quality_preference', 'age']
        
        # Scale features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(user_features[['total_sessions', 'total_watch_time', 
                                                            'avg_completion', 'unique_content', 'quality_preference']])
        
        # Find optimal number of clusters
        inertias = []
        silhouette_scores = []
        K_range = range(2, 8)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(features_scaled)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(features_scaled, kmeans.labels_))
        
        # Use 3 clusters (you can adjust this)
        optimal_k = 3
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        user_features['cluster'] = kmeans.fit_predict(features_scaled)
        
        # Analyze clusters
        print(f"\nClustering with {optimal_k} clusters:")
        cluster_summary = user_features.groupby('cluster').agg({
            'total_sessions': 'mean',
            'total_watch_time': 'mean',
            'avg_completion': 'mean',
            'unique_content': 'mean',
            'quality_preference': 'mean',
            'user_id': 'count'
        }).round(2)
        
        cluster_summary.columns = ['Avg Sessions', 'Avg Watch Time', 'Avg Completion', 
                                 'Avg Unique Content', 'Quality Preference', 'User Count']
        print(cluster_summary)
        
        return user_features
        
    def predictive_modeling(self):
        """Build predictive models"""
        print("\n" + "="*50)
        print("PREDICTIVE MODELING")
        print("="*50)
        
        # Prepare features for prediction
        features = self.merged_df[['age', 'watch_duration_minutes', 'is_high_quality', 
                                 'is_mobile', 'duration_minutes', 'rating']].fillna(0)
        
        # Target: High completion rate (>70%)
        target = (self.merged_df['completion_percentage'] > 70).astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Logistic Regression
        lr_model = LogisticRegression(random_state=42)
        lr_model.fit(X_train_scaled, y_train)
        lr_pred = lr_model.predict(X_test_scaled)
        lr_prob = lr_model.predict_proba(X_test_scaled)[:, 1]
        
        print("\nLOGISTIC REGRESSION RESULTS:")
        print(f"AUC Score: {roc_auc_score(y_test, lr_prob):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, lr_pred))
        
        # Random Forest
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        rf_pred = rf_model.predict(X_test)
        rf_prob = rf_model.predict_proba(X_test)[:, 1]
        
        print("\nRANDOM FOREST RESULTS:")
        print(f"AUC Score: {roc_auc_score(y_test, rf_prob):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, rf_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': features.columns,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFEATURE IMPORTANCE (Random Forest):")
        print(feature_importance)
        
        return lr_model, rf_model, scaler
        
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("\n" + "="*50)
        print("CREATING VISUALIZATIONS")
        print("="*50)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Subscription type distribution
        plt.subplot(3, 3, 1)
        self.users_df['subscription_type'].value_counts().plot(kind='bar')
        plt.title('Subscription Type Distribution')
        plt.xticks(rotation=45)
        
        # 2. Completion rate by subscription
        plt.subplot(3, 3, 2)
        self.merged_df.boxplot(column='completion_percentage', by='subscription_type', ax=plt.gca())
        plt.title('Completion Rate by Subscription Type')
        plt.suptitle('')
        
        # 3. Watch duration by device
        plt.subplot(3, 3, 3)
        self.merged_df.boxplot(column='watch_duration_minutes', by='device_type', ax=plt.gca())
        plt.title('Watch Duration by Device Type')
        plt.suptitle('')
        
        # 4. Quality level distribution
        plt.subplot(3, 3, 4)
        self.sessions_df['quality_level'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Quality Level Distribution')
        
        # 5. Age distribution
        plt.subplot(3, 3, 5)
        self.users_df['age'].hist(bins=20, alpha=0.7)
        plt.title('User Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Count')
        
        # 6. Sessions by country (top 10)
        plt.subplot(3, 3, 6)
        country_sessions = self.merged_df['country'].value_counts().head(10)
        country_sessions.plot(kind='bar')
        plt.title('Sessions by Country (Top 10)')
        plt.xticks(rotation=45)
        
        # 7. Completion rate distribution
        plt.subplot(3, 3, 7)
        self.sessions_df['completion_percentage'].hist(bins=30, alpha=0.7)
        plt.title('Completion Rate Distribution')
        plt.xlabel('Completion %')
        plt.ylabel('Count')
        
        # 8. Watch duration vs completion rate
        plt.subplot(3, 3, 8)
        plt.scatter(self.sessions_df['watch_duration_minutes'], 
                   self.sessions_df['completion_percentage'], alpha=0.5)
        plt.xlabel('Watch Duration (minutes)')
        plt.ylabel('Completion %')
        plt.title('Watch Duration vs Completion Rate')
        
        # 9. Monthly trend
        plt.subplot(3, 3, 9)
        monthly_sessions = self.sessions_df.groupby(self.sessions_df['watch_date'].dt.to_period('M')).size()
        monthly_sessions.plot(kind='line', marker='o')
        plt.title('Monthly Session Trend')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('streaming_analysis_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Visualizations saved as 'streaming_analysis_dashboard.png'")
        
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*50)
        print("GENERATING ANALYSIS REPORT")
        print("="*50)
        
        report = f"""
VIDEO STREAMING PLATFORM ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY:
- Total Users: {self.users_df['user_id'].nunique():,}
- Total Sessions: {len(self.sessions_df):,}
- Total Content: {len(self.content_df):,}
- Average Completion Rate: {self.sessions_df['completion_percentage'].mean():.1f}%

KEY INSIGHTS:
1. Most popular subscription type: {self.users_df['subscription_type'].mode().iloc[0]}
2. Most used device: {self.sessions_df['device_type'].mode().iloc[0]}
3. Most common quality: {self.sessions_df['quality_level'].mode().iloc[0]}
4. Top country by sessions: {self.merged_df['country'].value_counts().index[0]}

RECOMMENDATIONS:
1. Focus on improving completion rates for {self.merged_df.groupby('subscription_type')['completion_percentage'].mean().idxmin()} subscribers
2. Optimize streaming quality for {self.sessions_df['device_type'].mode().iloc[0]} devices
3. Expand content library in {self.merged_df['country'].value_counts().index[0]} market
4. Implement personalized recommendations based on user clustering analysis

TECHNICAL METRICS:
- Data quality: {((1 - self.merged_df.isnull().sum().sum() / (len(self.merged_df) * len(self.merged_df.columns))) * 100):.1f}%
- Analysis completion: 100%
- Models trained: 2 (Logistic Regression, Random Forest)
        """
        
        with open('analysis_report.txt', 'w') as f:
            f.write(report)
        
        print("Report saved as 'analysis_report.txt'")
        print(report)

def main():
    """Main execution function"""
    print("VIDEO STREAMING PLATFORM PERFORMANCE ANALYSIS")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = VideoStreamingAnalyzer()
    
    # Load data
    analyzer.load_data()
    
    # Create merged dataset
    analyzer.create_merged_dataset()
    
    # Run analysis
    analyzer.descriptive_statistics()
    analyzer.hypothesis_testing()
    user_clusters = analyzer.user_clustering()
    models = analyzer.predictive_modeling()
    analyzer.create_visualizations()
    analyzer.generate_report()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("Check the following files:")
    print("- streaming_analysis_dashboard.png (visualizations)")
    print("- analysis_report.txt (summary report)")
    print("="*60)

if __name__ == "__main__":
    main()
