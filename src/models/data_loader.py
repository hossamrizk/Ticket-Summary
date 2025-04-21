import pandas as pd
import io
from typing import Tuple

class DataLoader:
    """Responsible only for loading data from text files"""
    
    def load_from_text(self, text_content: str) -> pd.DataFrame:
        """Load data from text content"""
        try:
            lines = text_content.splitlines()
            lines = [line.strip() for line in lines if line.strip()]
            
            # Detect delimiter (tab or comma)
            first_line = lines[0]
            delimiter = '\t' if '\t' in first_line else ','
            
            # Create DataFrame
            return pd.read_csv(io.StringIO(text_content), delimiter=delimiter)
        except Exception as e:
            raise ValueError(f"Error converting text file: {str(e)}")
