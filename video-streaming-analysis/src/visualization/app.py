import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
USERS_CSV = os.path.join(BASE_DIR, 'users.csv')
SESSIONS_CSV = os.path.join(BASE_DIR, 'viewing_sessions.csv')

st.set_page_config(page_title='Streaming Performance Dashboard', layout='wide')

@st.cache_data
def load_data():
	users = pd.read_csv(USERS_CSV)
	sessions = pd.read_csv(SESSIONS_CSV)
	return users, sessions

users, sessions = load_data()

st.title('Video Streaming Platform Performance')

num_users = users['user_id'].nunique()
num_sessions = sessions['session_id'].nunique()
total_watch_hours = users['total_watch_time_hours'].sum()
avg_session_minutes = sessions['watch_duration_minutes'].mean()

col1, col2, col3, col4 = st.columns(4)
with col1:
	st.metric('Users', str(num_users))
with col2:
	st.metric('Sessions', str(num_sessions))
with col3:
	st.metric('Total Watch Hours', str(int(total_watch_hours)))
with col4:
	st.metric('Avg Session Minutes', str(round(float(avg_session_minutes), 1)))

st.subheader('Engagement by Subscription Type')
engagement = sessions.merge(users[['user_id','subscription_type','country']], on='user_id', how='left')
agg = engagement.groupby('subscription_type').agg(
	sessions=('session_id','nunique'),
	avg_completion=('completion_percentage','mean'),
	avg_minutes=('watch_duration_minutes','mean')
).reset_index()
st.dataframe(agg)

st.subheader('Sessions by Country')
sessions_by_country = engagement.groupby('country').size().sort_values(ascending=False).head(20)
st.bar_chart(sessions_by_country)

st.subheader('Quality Level Distribution')
quality_counts = sessions['quality_level'].value_counts()
st.bar_chart(quality_counts)

st.subheader('Device Type Breakdown')
device_counts = sessions['device_type'].value_counts()
st.bar_chart(device_counts)
