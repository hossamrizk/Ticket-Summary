from models.data_loader import DataLoader

class FileController:
    """Responsible only for file operations"""
    
    def __init__(self):
        self.data_loader = DataLoader()
    
    def read_file(self, file) -> str:
        """Read file content"""
        return file.read().decode("utf-8")
    
    def process_file_content(self, text_content: str):
        """Process uploaded file content"""
        try:
            return self.data_loader.load_from_text(text_content)
        except Exception as e:
            raise e