from controllers.data_controller import DataController
from controllers.summary_controller import SummaryController
from controllers.visualization_controller import VisualizationController
from views.data_overview_view import DataOverviewView
from views.summary_view import SummaryView

def render_analysis(data_controller: DataController, summary_controller: SummaryController, 
                    data_overview_view: DataOverviewView, summary_view: SummaryView, visualization_controller: VisualizationController):
    """Render all analysis components"""
    # Get statistics
    stats = data_controller.get_stats()
    
    # Show data overview
    data_overview_view.show_data_overview(stats)
    
    # Render summary tabs
    tab1, tab2 = summary_view.create_tabs()
    
    # Render product summaries in tab1
    summary_view.render_product_summaries(
        tab1, 
        stats['products'], 
        lambda product: summary_controller.generate_product_summary(product)
    )
    
    # Render raw data in tab2
    summary_view.render_raw_data(tab2, data_controller.get_mapped_data())
    
    # Render visualizations
    visualization_controller.render_visualizations(data_controller.get_mapped_data())