from views.visualization_view import VisualizationView
import pandas as pd

class VisualizationController:
    """Coordinates visualization generation"""
    
    def __init__(self):
        self.visualization_view = VisualizationView()
    
    def render_visualizations(self, df: pd.DataFrame):
        """Render all visualizations for the data"""
        self.visualization_view.render_visualizations(df)
