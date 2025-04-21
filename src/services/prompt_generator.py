import pandas as pd

class PromptGenerator:
    """Responsible only for generating prompts for AI summarization"""
    
    def create_section_prompt(self, section_name: str, category: str, section_data: pd.DataFrame) -> str:
        """Create a prompt for summarizing a section of tickets"""
        # Generate ticket details string
        ticket_details = "\n".join(
            f"- Ticket {row.get('ORDER_NUMBER', 'Unknown')} ({row.get('ACCEPTANCE_TIME', 'Unknown date').date() if hasattr(row.get('ACCEPTANCE_TIME', pd.NaT), 'date') else 'Unknown date'}): "
            f"{row.get('ORDER_DESCRIPTION_1', '')} - {row.get('ORDER_DESCRIPTION_2', '')}. "
            f"Resolution: {row.get('COMPLETION_RESULT_KB', '')}"
            for _, row in section_data.iterrows()
        )
        
        prompt = f"""Create a concise, professional summary for the '{section_name}' section of {category} tickets.
        Focus on identifying patterns, common issues, and resolution effectiveness. Write in clear business English.
        
        Ticket Details:
        {ticket_details}
        
        Summary:"""
        
        return prompt