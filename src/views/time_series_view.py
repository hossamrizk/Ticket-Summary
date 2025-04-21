import streamlit as st
import plotly.express as px
import pandas as pd

class TimeSeriesView:
    """Responsible only for displaying time series visualizations"""
    
    def render(self, df: pd.DataFrame):
        """Render time series visualization"""
        
        # Only create date-based visualization if the column exists and has valid dates
        if 'ACCEPTANCE_TIME' in df.columns and not df['ACCEPTANCE_TIME'].isna().all():
            # Ensure we have a date column
            data_with_date = df.copy()
            data_with_date['DATE'] = data_with_date['ACCEPTANCE_TIME'].dt.date
            daily_counts = data_with_date.groupby(['DATE', 'PRODUCT']).size().reset_index(name='COUNT')
            fig1 = px.line(daily_counts, x='DATE', y='COUNT', color='PRODUCT',
                          title="Daily Ticket Volume by Product")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Cannot create time-based visualization: Missing or invalid date data")
