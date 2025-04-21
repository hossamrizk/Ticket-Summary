from views.time_series_view import TimeSeriesView
from views.resolution_time_view import ResolutionTimeView
import streamlit as st
import plotly.express as px
import pandas as pd

class VisualizationView:
    """Coordinates all visualization components"""
    
    def __init__(self):
        self.time_series_view = TimeSeriesView()
        self.resolution_time_view = ResolutionTimeView()
    
    def render_visualizations(self, df: pd.DataFrame):
        """Render all visualizations"""
        st.subheader("Data Visualizations")
        if df.empty:
            st.warning("No data available for visualizations")
            return
            
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            self.time_series_view.render(df)
        
        with viz_col2:
            self.resolution_time_view.render(df)