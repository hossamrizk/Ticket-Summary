import pandas as pd
from typing import List

class DataProcessor:
    """Responsible only for processing and cleaning data"""
    
    def __init__(self, valid_categories: List[str] = None):
        self.valid_categories = valid_categories or ['HDW', 'NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD']
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and filter the data"""
        try:
            if df.empty:
                return df
                
            processed_df = df.copy()
            
            # Filter only relevant categories if the column exists
            if 'SERVICE_CATEGORY' in processed_df.columns:
                processed_df = processed_df[processed_df['SERVICE_CATEGORY'].isin(self.valid_categories)]
            
            # Convert date columns if they exist
            date_cols = ['ACCEPTANCE_TIME', 'COMPLETION_TIME']
            for col in date_cols:
                if col in processed_df.columns:
                    processed_df[col] = pd.to_datetime(processed_df[col], errors='coerce')
            
            return processed_df
        except Exception as e:
            raise ValueError(f"Error preprocessing data: {str(e)}")
    
    def calculate_resolution_time(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate resolution time from acceptance to completion"""
        if df.empty:
            return df
            
        result_df = df.copy()
        
        if all(col in result_df.columns for col in ['COMPLETION_TIME', 'ACCEPTANCE_TIME']) and \
           not result_df['COMPLETION_TIME'].isna().all() and not result_df['ACCEPTANCE_TIME'].isna().all():
            result_df['RESOLUTION_HOURS'] = (result_df['COMPLETION_TIME'] - 
                                            result_df['ACCEPTANCE_TIME']).dt.total_seconds() / 3600
        
        return result_df