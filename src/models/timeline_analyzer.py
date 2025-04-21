# models/timeline_analyzer.py
import pandas as pd
from datetime import timedelta
from typing import Dict

class TimelineAnalyzer:
    """Responsible only for creating timeline sections from ticket data"""
    
    def create_timeline_sections(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Divide tickets into storytelling timeline sections"""
        if len(df) == 0:
            return self._create_empty_sections()
        
        # Make sure we have a valid date column
        if 'ACCEPTANCE_TIME' not in df.columns or df['ACCEPTANCE_TIME'].isna().all():
            return {"All Tickets": df}
        
        # Convert to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df['ACCEPTANCE_TIME']):
            df['ACCEPTANCE_TIME'] = pd.to_datetime(df['ACCEPTANCE_TIME'], errors='coerce')
        
        sorted_df = df.sort_values('ACCEPTANCE_TIME')
        date_range = (sorted_df['ACCEPTANCE_TIME'].max() - sorted_df['ACCEPTANCE_TIME'].min()).days
        
        # For small datasets, prioritize showing all sections with at least 1 ticket
        if len(sorted_df) <= 10:
            return self._create_adaptive_sections(sorted_df)
        elif date_range <= 7:
            return self._create_count_based_sections(sorted_df)
        else:
            return self._create_time_based_sections(sorted_df, date_range)
    
    def _create_empty_sections(self) -> Dict[str, pd.DataFrame]:
        """Return all section headers even when empty"""
        return {
            'Initial Issues': pd.DataFrame(),
            'Follow-ups': pd.DataFrame(),
            'Developments': pd.DataFrame(),
            'Later Incidents': pd.DataFrame(),
            'Recent Events': pd.DataFrame()
        }
    
    def _create_adaptive_sections(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Create sections that adapt to very small datasets"""
        sections = self._create_empty_sections()
        ticket_count = len(df)
        
        # Distribute tickets across sections more evenly
        if ticket_count >= 1:
            sections['Initial Issues'] = df.iloc[:1]
        if ticket_count >= 2:
            sections['Follow-ups'] = df.iloc[1:2]
        if ticket_count >= 3:
            sections['Developments'] = df.iloc[2:3]
        if ticket_count >= 4:
            sections['Later Incidents'] = df.iloc[3:4]
        if ticket_count >= 5:
            sections['Recent Events'] = df.iloc[4:]
            
        return {k: v for k, v in sections.items() if len(v) > 0}
    
    def _create_count_based_sections(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Create sections based on ticket count"""
        sections = self._create_empty_sections()
        ticket_count = len(df)
        
        sections['Initial Issues'] = df.iloc[:min(2, ticket_count)]
        if ticket_count > 2:
            sections['Follow-ups'] = df.iloc[min(2, ticket_count):min(4, ticket_count)]
        if ticket_count > 4:
            sections['Developments'] = df.iloc[min(4, ticket_count):min(6, ticket_count)]
        if ticket_count > 6:
            sections['Later Incidents'] = df.iloc[min(6, ticket_count):min(8, ticket_count)]
        if ticket_count > 8:
            sections['Recent Events'] = df.iloc[min(8, ticket_count):]
            
        return {k: v for k, v in sections.items() if len(v) > 0}
    
    def _create_time_based_sections(self, df: pd.DataFrame, date_range: int) -> Dict[str, pd.DataFrame]:
        """Create sections based on time periods"""
        sections = self._create_empty_sections()
        time_split = max(1, date_range // 5)  # Ensure at least 1 day per section
        min_date = df['ACCEPTANCE_TIME'].min()
        
        sections['Initial Issues'] = df[df['ACCEPTANCE_TIME'] < min_date + timedelta(days=time_split)]
        sections['Follow-ups'] = df[(df['ACCEPTANCE_TIME'] >= min_date + timedelta(days=time_split)) & 
                                  (df['ACCEPTANCE_TIME'] < min_date + timedelta(days=time_split*2))]
        sections['Developments'] = df[(df['ACCEPTANCE_TIME'] >= min_date + timedelta(days=time_split*2)) & 
                                     (df['ACCEPTANCE_TIME'] < min_date + timedelta(days=time_split*3))]
        sections['Later Incidents'] = df[(df['ACCEPTANCE_TIME'] >= min_date + timedelta(days=time_split*3)) & 
                                        (df['ACCEPTANCE_TIME'] < min_date + timedelta(days=time_split*4))]
        sections['Recent Events'] = df[df['ACCEPTANCE_TIME'] >= min_date + timedelta(days=time_split*4)]
        
        return {k: v for k, v in sections.items() if len(v) > 0}