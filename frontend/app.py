import streamlit as st
from add_update_ui import prepare_add_update_tab
from analytics_by_date_ui import prepare_analytics_tab
from anylytics_by_month_ui import prepare_monthly_analytics_tab

st.title('Expense Tracking System')

tab1 , tab2 , tab3 = st.tabs(['Add/update','Analytics by Date','Analytics by Month'])


with tab1:
    prepare_add_update_tab()

with tab2:
    prepare_analytics_tab()

with tab3:
    prepare_monthly_analytics_tab()

