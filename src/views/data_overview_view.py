import streamlit as st
from typing import Dict, Any

class DataOverviewView:
    """Responsible only for displaying data overview"""
    
    def show_data_overview(self, stats: Dict[str, Any]):
        """Show data overview metrics"""
        st.subheader("Data Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Tickets Processed", stats['total_tickets'])
        with col2:
            st.metric("Unique Products", stats['unique_products'])
    