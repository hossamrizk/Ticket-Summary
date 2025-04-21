# views/summary_view.py
import streamlit as st
import pandas as pd
from typing import List, Callable, Dict

class SummaryView:
    """Responsible only for displaying summary content"""
    
    def create_tabs(self):
        """Create summary tabs"""
        st.subheader("AI-Powered Ticket Summaries")
        tab1, tab2 = st.tabs(["Summary View", "Raw Data"])
        return tab1, tab2
    
    def render_product_summaries(self, tab, products: List[str], get_summary_callback: Callable):
        """Render product summaries in the given tab"""
        with tab:
            for product in products:
                with st.expander(f"{product} Tickets", expanded=True):
                    with st.spinner(f"Generating summary for {product}..."):
                        summary = get_summary_callback(product)
                        if summary:
                            # Split the summary into sections and display with clear headers
                            sections = summary.split('### ')
                            for section in sections[1:]:  # Skip the first empty split
                                section_title, *section_content = section.split('\n', 1)
                                with st.container():
                                    st.subheader(section_title)
                                    st.markdown('\n'.join(section_content))
                        else:
                            st.warning(f"No tickets found for {product}")
    
    def render_raw_data(self, tab, df: pd.DataFrame):
        """Render raw data in the given tab"""
        with tab:
            st.dataframe(df)