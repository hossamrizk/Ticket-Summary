from controllers.file_controller import FileController
from controllers.data_controller import DataController
from controllers.visualization_controller import VisualizationController
from views.page_view import PageView
from views.sidebar_view import SidebarView
from views.data_overview_view import DataOverviewView
from views.summary_view import SummaryView

def initialize_components():
    """Initialize all controllers and views"""
    
    # Initialize views
    page_view = PageView()
    sidebar_view = SidebarView()
    data_overview_view = DataOverviewView()
    summary_view = SummaryView()
    
    # Initialize controllers
    file_controller = FileController()
    data_controller = DataController()
    visualization_controller = VisualizationController()
    
    return (
        page_view, sidebar_view, data_overview_view, summary_view,
        file_controller, data_controller, visualization_controller
    )