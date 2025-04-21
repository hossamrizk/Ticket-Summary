import streamlit as st
from typing import List

class SidebarView:
    """Responsible only for sidebar components"""
    
    def render_settings(self, model_options: List[str]):
        """Render sidebar settings UI"""
        with st.sidebar:
            st.header("Settings")
            model = st.selectbox(
                "Ollama Model",
                model_options,
                help="Select which local LLM model to use for summarization"
            )
            st.divider()
            st.info("Note: Requires Ollama running locally with the selected model downloaded")
            
            # Instructions for running Ollama
            st.sidebar.divider()
            st.sidebar.markdown("""
            **Ollama Setup Instructions:**
            1. Download and install Ollama from [ollama.ai](https://ollama.ai/)
            2. Run in terminal: `ollama pull llama3`
            3. Keep Ollama running in background
            """)
            
            return model