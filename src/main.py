from helpers.initialize_components import initialize_components
from helpers.process_uploaded_file import process_uploaded_file
from helpers.render_analysis import render_analysis
from controllers.summary_controller import SummaryController

def main():
    
    # Initialize all components
    (page_view, sidebar_view, data_overview_view, summary_view,
     file_controller, data_controller, visualization_controller) = initialize_components()
    
    # Set up page
    page_view.setup_page()
    
    # Get model selection from sidebar
    model_name = sidebar_view.render_settings(["gemma2:2b-instruct-q5_0", "mistral", "gemma"])
    
    # Initialize summary controller with selected model
    summary_controller = SummaryController(data_controller, model_name)
    
    # File upload
    uploaded_file = page_view.file_uploader()
    
    if uploaded_file:
        with page_view.show_processing_message():
            if process_uploaded_file(file_controller, data_controller, page_view, uploaded_file):
                render_analysis(data_controller, summary_controller, 
                               data_overview_view, summary_view, visualization_controller)
    else:
        page_view.show_info("Please upload a text file to begin analysis")

if __name__ == "__main__":
    main()