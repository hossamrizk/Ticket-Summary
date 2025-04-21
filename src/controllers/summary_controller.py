from services.ai_service import AIService
from services.prompt_generator import PromptGenerator
from controllers.data_controller import DataController
from typing import Optional

class SummaryController:
    """Coordinates summary generation"""
    
    def __init__(self, data_controller: DataController, model_name: str = "gemma2:2b-instruct-q5_0"):
        self.data_controller = data_controller
        self.ai_service = AIService(model_name)
        self.prompt_generator = PromptGenerator()
    
    def set_model(self, model_name: str):
        """Set the AI model to use"""
        self.ai_service.set_model(model_name)
    
    def generate_product_summary(self, product: str) -> Optional[str]:
        """Generate summary for a product with enhanced section formatting"""
        product_df = self.data_controller.get_product_data(product)
        if len(product_df) == 0:
            return None
        
        sections = self.data_controller.get_timeline_sections(product)
        if not sections:
            return "No timeline sections could be created for this product."
        
        summary = f"## {product} Summary\n\n"
        for section_name, section_data in sections.items():
            summary += f"### {section_name}\n"
            
            # Create LLM prompt and generate summary
            prompt = self.prompt_generator.create_section_prompt(section_name, product, section_data)
            ai_summary = self.ai_service.generate_summary(prompt)
            
            # Add clear section divider and summary
            summary += f"{ai_summary}\n\n"
            
            # Add ticket examples with clear formatting
            available_cols = ['ORDER_NUMBER', 'ACCEPTANCE_TIME', 'ORDER_DESCRIPTION_1']
            display_cols = [col for col in available_cols if col in section_data.columns]
            
            if display_cols:
                summary += "**Relevant Tickets:**\n"
                summary += section_data[display_cols].to_markdown(index=False)
            summary += "\n\n---\n\n"  # Visual divider between sections
        
        return summary