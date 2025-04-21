import streamlit as st
import plotly.express as px
import pandas as pd

class ResolutionTimeView:
    """Responsible only for displaying resolution time visualizations"""
    
    def render(self, df: pd.DataFrame):
        """Render resolution time visualization"""
        # Resolution time analysis
        if all(col in df.columns for col in ['COMPLETION_TIME', 'ACCEPTANCE_TIME']) and \
           not df['COMPLETION_TIME'].isna().all() and not df['ACCEPTANCE_TIME'].isna().all():
            data_with_resolution = df.copy()
            data_with_resolution['RESOLUTION_HOURS'] = (data_with_resolution['COMPLETION_TIME'] - 
                                                     data_with_resolution['ACCEPTANCE_TIME']).dt.total_seconds() / 3600
            fig2 = px.box(data_with_resolution, x='PRODUCT', y='RESOLUTION_HOURS',
                         title="Resolution Time by Product (Hours)")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Cannot create resolution time visualization: Missing or invalid timing data")
