import pandas as pd
from typing import Dict

class CategoryMapper:
    """Responsible only for mapping service categories to products"""
    
    def __init__(self, category_map: Dict[str, str] = None):
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
        """Map service categories to products"""
        try:
            mapped_df = df.copy()
            
            # Only attempt mapping if the column exists
            if 'SERVICE_CATEGORY' in mapped_df.columns:
                mapped_df['PRODUCT'] = mapped_df['SERVICE_CATEGORY'].map(self.category_map)
            else:
                # Create a default product column if SERVICE_CATEGORY doesn't exist
                mapped_df['PRODUCT'] = 'Unknown'
                
            return mapped_df
        except Exception as e:
            raise ValueError(f"Error mapping categories: {str(e)}")