from controllers.file_controller import FileController
from controllers.data_controller import DataController
from views.page_view import PageView


def process_uploaded_file(file_controller: FileController, data_controller: DataController, page_view: PageView, uploaded_file):
    """Process the uploaded file and return success status"""
    try:
        text_content = file_controller.read_file(uploaded_file)
        df = file_controller.process_file_content(text_content)
        success = data_controller.process_data(df)
        
        if not success or data_controller.mapped_df.empty:
            page_view.show_error("Could not process the file. Please check the format.")
            return False
        return True
    except Exception as e:
        page_view.show_error(f"Error processing file: {str(e)}")
        return False