import pandas as pd
from models.data_processor import DataProcessor
from models.category_mapper import CategoryMapper
from models.timeline_analyzer import TimelineAnalyzer
from typing import Dict, Any

class DataController:
    """Coordinates data processing operations"""
    
    def __init__(self):
        self.data_processor = DataProcessor()
        self.category_mapper = CategoryMapper()
        self.timeline_analyzer = TimelineAnalyzer()
        self.raw_df = pd.DataFrame()
        self.processed_df = pd.DataFrame()
        self.mapped_df = pd.DataFrame()
    
    def process_data(self, df: pd.DataFrame) -> bool:
        """Process raw dataframe"""
        try:
            self.raw_df = df
            self.processed_df = self.data_processor.preprocess(df)
            self.mapped_df = self.category_mapper.map_categories(self.processed_df)
            self.mapped_df = self.data_processor.calculate_resolution_time(self.mapped_df)
            return True
        except Exception as e:
            raise e
    
    def get_stats(self) -> Dict[str, Any]:
        """Get data statistics"""
        if self.mapped_df.empty:
            return {'total_tickets': 0, 'unique_products': 0, 'products': []}
        
        return {
            'total_tickets': len(self.mapped_df),
            'unique_products': self.mapped_df['PRODUCT'].nunique(),
            'products': list(self.mapped_df['PRODUCT'].unique())
        }
    
    def get_product_data(self, product: str) -> pd.DataFrame:
        """Get data for a specific product"""
        if self.mapped_df.empty:
            return pd.DataFrame()
        
        return self.mapped_df[self.mapped_df['PRODUCT'] == product]
    
    def get_timeline_sections(self, product: str) -> Dict[str, pd.DataFrame]:
        """Get timeline sections for a product"""
        product_df = self.get_product_data(product)
        return self.timeline_analyzer.create_timeline_sections(product_df)
    
    def get_mapped_data(self) -> pd.DataFrame:
        """Get the processed and mapped data"""
        return self.mapped_df