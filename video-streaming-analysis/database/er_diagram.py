"""
ER Diagram Generator for Video Streaming Platform
Creates a visual Entity-Relationship diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_er_diagram():
    """Create ER diagram for video streaming platform"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors
    entity_color = '#E8F4FD'
    attribute_color = '#F0F8FF'
    pk_color = '#FFE4E1'
    fk_color = '#E6E6FA'
    
    # Users Entity
    users_box = FancyBboxPatch((1, 7), 2, 2.5, boxstyle="round,pad=0.1", 
                              facecolor=entity_color, edgecolor='black', linewidth=2)
    ax.add_patch(users_box)
    ax.text(2, 8.5, 'USERS', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Users attributes
    users_attrs = ['user_id (PK)', 'age', 'country', 'subscription_type', 
                   'registration_date', 'total_watch_time_hours']
    for i, attr in enumerate(users_attrs):
        y_pos = 8.2 - i * 0.3
        color = pk_color if 'PK' in attr else attribute_color
        attr_box = FancyBboxPatch((0.7, y_pos-0.1), 1.6, 0.2, boxstyle="round,pad=0.02",
                                 facecolor=color, edgecolor='gray', linewidth=1)
        ax.add_patch(attr_box)
        ax.text(1.5, y_pos, attr, ha='center', va='center', fontsize=9)
    
    # Content Entity
    content_box = FancyBboxPatch((6, 7), 2, 2.5, boxstyle="round,pad=0.1",
                                facecolor=entity_color, edgecolor='black', linewidth=2)
    ax.add_patch(content_box)
    ax.text(7, 8.5, 'CONTENT', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Content attributes
    content_attrs = ['content_id (PK)', 'title', 'genre', 'duration_minutes',
                     'release_year', 'rating', 'views_count', 'production_budget']
    for i, attr in enumerate(content_attrs):
        y_pos = 8.2 - i * 0.3
        color = pk_color if 'PK' in attr else attribute_color
        attr_box = FancyBboxPatch((5.7, y_pos-0.1), 1.6, 0.2, boxstyle="round,pad=0.02",
                                 facecolor=color, edgecolor='gray', linewidth=1)
        ax.add_patch(attr_box)
        ax.text(6.5, y_pos, attr, ha='center', va='center', fontsize=9)
    
    # Viewing Sessions Entity
    sessions_box = FancyBboxPatch((3.5, 4), 3, 2.5, boxstyle="round,pad=0.1",
                                 facecolor=entity_color, edgecolor='black', linewidth=2)
    ax.add_patch(sessions_box)
    ax.text(5, 5.5, 'VIEWING_SESSIONS', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Sessions attributes
    sessions_attrs = ['session_id (PK)', 'user_id (FK)', 'content_id (FK)',
                      'watch_date', 'watch_duration_minutes', 'completion_percentage',
                      'device_type', 'quality_level']
    for i, attr in enumerate(sessions_attrs):
        y_pos = 5.2 - i * 0.3
        if 'PK' in attr:
            color = pk_color
        elif 'FK' in attr:
            color = fk_color
        else:
            color = attribute_color
        attr_box = FancyBboxPatch((3.2, y_pos-0.1), 2.6, 0.2, boxstyle="round,pad=0.02",
                                 facecolor=color, edgecolor='gray', linewidth=1)
        ax.add_patch(attr_box)
        ax.text(4.5, y_pos, attr, ha='center', va='center', fontsize=9)
    
    # User Ratings Entity
    ratings_box = FancyBboxPatch((1, 1), 2, 2, boxstyle="round,pad=0.1",
                                facecolor=entity_color, edgecolor='black', linewidth=2)
    ax.add_patch(ratings_box)
    ax.text(2, 2.5, 'USER_RATINGS', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Ratings attributes
    ratings_attrs = ['rating_id (PK)', 'user_id (FK)', 'content_id (FK)',
                     'rating', 'review_text', 'created_at']
    for i, attr in enumerate(ratings_attrs):
        y_pos = 2.2 - i * 0.25
        if 'PK' in attr:
            color = pk_color
        elif 'FK' in attr:
            color = fk_color
        else:
            color = attribute_color
        attr_box = FancyBboxPatch((0.7, y_pos-0.1), 1.6, 0.2, boxstyle="round,pad=0.02",
                                 facecolor=color, edgecolor='gray', linewidth=1)
        ax.add_patch(attr_box)
        ax.text(1.5, y_pos, attr, ha='center', va='center', fontsize=9)
    
    # Performance Metrics Entity
    metrics_box = FancyBboxPatch((6, 1), 2, 2, boxstyle="round,pad=0.1",
                                facecolor=entity_color, edgecolor='black', linewidth=2)
    ax.add_patch(metrics_box)
    ax.text(7, 2.5, 'PERFORMANCE_METRICS', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Metrics attributes
    metrics_attrs = ['metric_id (PK)', 'session_id (FK)', 'timestamp',
                     'metric_type', 'metric_value', 'metric_unit']
    for i, attr in enumerate(metrics_attrs):
        y_pos = 2.2 - i * 0.25
        if 'PK' in attr:
            color = pk_color
        elif 'FK' in attr:
            color = fk_color
        else:
            color = attribute_color
        attr_box = FancyBboxPatch((5.7, y_pos-0.1), 1.6, 0.2, boxstyle="round,pad=0.02",
                                 facecolor=color, edgecolor='gray', linewidth=1)
        ax.add_patch(attr_box)
        ax.text(6.5, y_pos, attr, ha='center', va='center', fontsize=9)
    
    # Relationships
    # Users to Viewing Sessions (1:N)
    connection1 = ConnectionPatch((2, 7), (4.5, 6.5), "data", "data",
                                 arrowstyle="->", shrinkA=5, shrinkB=5,
                                 mutation_scale=20, fc="black")
    ax.add_patch(connection1)
    ax.text(3, 6.8, '1', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(3.2, 6.6, 'N', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Content to Viewing Sessions (1:N)
    connection2 = ConnectionPatch((7, 7), (5.5, 6.5), "data", "data",
                                 arrowstyle="->", shrinkA=5, shrinkB=5,
                                 mutation_scale=20, fc="black")
    ax.add_patch(connection2)
    ax.text(6.2, 6.8, '1', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 6.6, 'N', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Users to User Ratings (1:N)
    connection3 = ConnectionPatch((2, 7), (2, 3), "data", "data",
                                 arrowstyle="->", shrinkA=5, shrinkB=5,
                                 mutation_scale=20, fc="black")
    ax.add_patch(connection3)
    ax.text(1.8, 5, '1', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(1.6, 4.8, 'N', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Content to User Ratings (1:N)
    connection4 = ConnectionPatch((7, 7), (7, 3), "data", "data",
                                 arrowstyle="->", shrinkA=5, shrinkB=5,
                                 mutation_scale=20, fc="black")
    ax.add_patch(connection4)
    ax.text(6.8, 5, '1', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6.6, 4.8, 'N', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Viewing Sessions to Performance Metrics (1:N)
    connection5 = ConnectionPatch((5, 4), (7, 3), "data", "data",
                                 arrowstyle="->", shrinkA=5, shrinkB=5,
                                 mutation_scale=20, fc="black")
    ax.add_patch(connection5)
    ax.text(5.8, 3.5, '1', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 3.3, 'N', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Legend
    legend_elements = [
        patches.Patch(color=entity_color, label='Entity'),
        patches.Patch(color=pk_color, label='Primary Key'),
        patches.Patch(color=fk_color, label='Foreign Key'),
        patches.Patch(color=attribute_color, label='Attribute')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Title
    ax.text(5, 9.5, 'Video Streaming Platform - Entity Relationship Diagram', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('video_streaming_er_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("ER Diagram saved as 'video_streaming_er_diagram.png'")

if __name__ == "__main__":
    create_er_diagram()
