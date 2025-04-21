from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

class AIService:
    """Service for AI-powered ticket summarization"""
    
    def __init__(self, model_name: str = "gemma2:2b-instruct-q5_0"):
        self.model_name = model_name
        self._llm = None
    
    def _initialize_llm(self):
        """Initialize LLM if not already initialized"""
        if self._llm is None:
            self._llm = ChatOllama(model=self.model_name, temperature=0.7)
    
    def set_model(self, model_name: str):
        """Change the model"""
        self.model_name = model_name
        self._llm = None  # Reset so it will be reinitialized with new model
    
    def generate_summary(self, prompt: str) -> str:
        """Generate summary using local Ollama LLM via LangChain"""
        try:
            self._initialize_llm()
            
            # Create a human message
            message = HumanMessage(content=prompt)
            
            # Get response from LLM
            response = self._llm.invoke([message])
            
            # Return the content of the response
            return response.content
        except Exception as e:
            raise RuntimeError(f"Error generating AI summary: {str(e)}")