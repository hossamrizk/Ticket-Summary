import streamlit as st

class PageView:
    """Responsible for basic page setup"""
    
    def setup_page(self):
        """Set up the page layout and title"""
        st.set_page_config(layout="wide")
        st.title("📊 System Ticket Data Analyzer")
        st.caption("Upload raw ticket data text file to generate AI-powered summaries")
    
    def file_uploader(self):
        """Render file upload component"""
        return st.file_uploader("Upload Ticket Data Text File", type=["txt"])
    
    def show_error(self, message: str):
        """Show error message"""
        st.error(message)
    
    def show_processing_message(self):
        """Show processing message"""
        return st.spinner("Processing data...")
    
    def show_info(self, message: str):
        """Show info message"""
        st.info(message)