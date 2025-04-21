# Code Documentation
## 1. Data Loading (`models/data_loader.py`)

```python
"""
Converts raw text ticket data into structured DataFrame
Handles format detection and initial parsing
"""
import pandas as pd
import io
from typing import Tuple

class DataLoader:
    def load_from_text(self, text_content: str) -> pd.DataFrame:
        """
        Parses raw text content into DataFrame
        Args:
            text_content: Raw string from uploaded file
        Returns:
            pd.DataFrame: Structured ticket data
        Raises:
            ValueError: If parsing fails
        """
        try:
            # Detect delimiter from first line
            first_line = text_content.split('\n')[0]
            delimiter = '\t' if '\t' in first_line else ','
            
            # Convert to DataFrame with error handling
            return pd.read_csv(io.StringIO(text_content), 
                   delimiter=delimiter,
                   on_bad_lines='warn')
        except Exception as e:
            raise ValueError(f"Data loading failed: {str(e)}")
```
## 2. Data Processing(`models/data_processor`)
```python
"""
Cleans and prepares raw ticket data for analysis
Handles filtering, date conversion, and feature engineering
"""
import pandas as pd
from typing import List

class DataProcessor:
    def __init__(self, valid_categories: List[str] = None):
        # Default valid service categories
        self.valid_categories = valid_categories or [
            'HDW', 'NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD'
        ]

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies cleaning pipeline:
        1. Filters by valid categories
        2. Converts date columns
        3. Handles missing values
        """
        processed_df = df.copy()
        
        # Category filtering
        if 'SERVICE_CATEGORY' in processed_df.columns:
            processed_df = processed_df[
                processed_df['SERVICE_CATEGORY'].isin(self.valid_categories)
            ]
        
        # Date conversion
        date_cols = ['ACCEPTANCE_TIME', 'COMPLETION_TIME']
        for col in date_cols:
            if col in processed_df.columns:
                processed_df[col] = pd.to_datetime(
                    processed_df[col], 
                    errors='coerce'  # Converts invalid dates to NaT
                )
        
        return processed_df.dropna(subset=['ACCEPTANCE_TIME'])
```
## 3. Category Mapping (`models/category_mapper.py`)
```python
"""
Maps technical service codes to business product names
Maintains consistent product categorization
"""
import pandas as pd
from typing import Dict

class CategoryMapper:
    def __init__(self, category_map: Dict[str, str] = None):
        # Product mapping dictionary
        self.category_map = category_map or {
            'KAI': 'Broadband',
            'NET': 'Broadband',
            'KAV': 'Voice',
            'KAD': 'TV',
            'GIGA': 'GIGA',
            'VOD': 'VOD',
            'HDW': 'Hardware'
        }

    def map_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds PRODUCT column based on SERVICE_CATEGORY
        Preserves original data for debugging
        """
        mapped_df = df.copy()
        mapped_df['PRODUCT'] = (
            mapped_df['SERVICE_CATEGORY']
            .map(self.category_map)
            .fillna('Unknown')  # Handle unmapped categories
        )
        return mapped_df
```
## 4. Timeline Analysis (`models/timeline_analyzer.py`)
```python
"""
Creates storytelling timeline sections from ticket data
Implements both time-based and count-based splitting
"""
import pandas as pd
from datetime import timedelta
from typing import Dict

class TimelineAnalyzer:
    def create_timeline_sections(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Main entry point - auto-selects splitting strategy:
        1. For small datasets (<10 tickets): adaptive distribution
        2. For short periods (<7 days): split by ticket count
        3. For longer periods: split by time intervals
        """
        if len(df) == 0:
            return self._create_empty_sections()
        
        sorted_df = df.sort_values('ACCEPTANCE_TIME')
        date_range = (sorted_df['ACCEPTANCE_TIME'].max() - 
                     sorted_df['ACCEPTANCE_TIME'].min()).days
        
        if len(sorted_df) <= 10:
            return self._create_adaptive_sections(sorted_df)
        elif date_range <= 7:
            return self._create_count_based_sections(sorted_df)
        else:
            return self._create_time_based_sections(sorted_df, date_range)
```
## 5. AI Service (`services/ai_service.py`)
```python
"""
Interface with local Ollama LLM for summarization
Handles model initialization and text generation
"""
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

class AIService:
    def __init__(self, model_name: str = "gemma2:2b-instruct-q5_0"):
        """
        Configures LLM with defaults:
        - model: Local Ollama model name
        - temperature: 0.7 for balanced creativity/accuracy
        """
        self.model_name = model_name
        self._llm = None  # Lazy initialization

    def generate_summary(self, prompt: str) -> str:
        """
        Generates AI summary from structured prompt
        Args:
            prompt: Pre-formatted analysis instructions
        Returns:
            str: Generated summary text
        """
        self._initialize_llm()
        message = HumanMessage(content=prompt)
        return self._llm.invoke([message]).content
```
## 6. Streamlit Views (`views/summary_view.py`)
```python
"""
Handles presentation of AI summaries in Streamlit UI
Manages tab layout and section display
"""
import streamlit as st
from typing import List, Callable

class SummaryView:
    def render_product_summaries(self, tab, products: List[str], 
                              get_summary_callback: Callable):
        """
        Displays expandable summary sections per product
        Args:
            tab: Streamlit tab container
            products: List of product categories
            get_summary_callback: Function to generate summaries
        """
        with tab:
            for product in products:
                with st.expander(f"{product} Tickets", expanded=True):
                    summary = get_summary_callback(product)
                    if summary:
                        self._render_sections(summary)
                    else:
                        st.warning(f"No data for {product}")

    def _render_sections(self, summary: str):
        """Helper to parse and display markdown sections"""
        sections = summary.split('### ')[1:]  # Skip header
        for section in sections:
            title, content = section.split('\n', 1)
            with st.container():
                st.subheader(title)
                st.markdown(content)
```
