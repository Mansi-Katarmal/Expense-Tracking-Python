import streamlit as st
from datetime import datetime
import requests
import pandas as pd

backend_api_url = 'http://127.0.0.1:8000'

def prepare_analytics_tab():
    col1,col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date',datetime(2024,8,1))
    with col2:
        end_date = st.date_input('End Date',datetime(2024,8,1))
    if st.button('Get Analytics'):
        params = {
        'start_date' : start_date.strftime('%Y-%m-%d'),
        'end_date' : end_date.strftime('%Y-%m-%d')
        }
        response = requests.post(f'{backend_api_url}/analytics_by_category',json=params)
        response = response.json()
        # st.write(response)
        breakdown = pd.DataFrame({
            'Category' : list(response.keys()),
            'Total' : [response[category]['total'] for category in response],
            'Percentage' : [response[category]['percentage'] for category in response]
        })
        breakdown_sorted = breakdown.sort_values(by='Percentage',ascending=False)
        st.bar_chart(breakdown_sorted,x='Category',y='Percentage')
        
        breakdown_sorted['Total'] = breakdown_sorted['Total'].map('{:.2f}'.format)
        breakdown_sorted['Percentage'] = breakdown_sorted['Percentage'].map('{:.2f}'.format)
        st.table(breakdown_sorted)