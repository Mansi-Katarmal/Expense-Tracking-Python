import streamlit as st
import requests
import pandas as pd

backend_api_url = 'http://127.0.0.1:8000'

def prepare_monthly_analytics_tab():
    response = requests.get(f'{backend_api_url}/analytics_by_month')
    if response.status_code == 200:
        response = response.json()
        # st.write(response)

        breakdown = pd.DataFrame(response)
        breakdown.rename(columns={
            'month_number' : 'Month Number',
            'month_name':'Month Name',
            'monthly_expense':'Monthly Expense'
        },inplace=True)

        breakdown_sorted = breakdown.sort_values(by='Month Number')
        st.bar_chart(breakdown,x='Month Name',y='Monthly Expense')
        
        breakdown_sorted['Monthly Expense'] = breakdown_sorted['Monthly Expense'].map('{:.2f}'.format)
        st.table(breakdown_sorted)