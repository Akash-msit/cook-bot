import yaml, sys
sys.path.append('models')
sys.path.append('chatbot/rag')
from langchain.agents import tool 
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from geminillm import gemini  # type: ignore
from rag.bot import get_answer  # Import your RAG answer retrieval function

# Load configuration
with open('config.yaml') as config_file:
    config_file = yaml.safe_load(config_file)

# Initialize your LLM
llm = gemini()

class Input(BaseModel):
    code: str = Field(description="should be code")

class Output(BaseModel):
    response: str = Field(description="should be refactored code")

parser = StrOutputParser(pydantic_object=Output)

@tool("cooking_query_tool", args_schema=Input, return_direct=True)
def cooking_query_tool(query: str) -> str:
    """
    Use this tool to provide detailed answers and insights for any cooking-related questions, including:
    - Recipes: Step-by-step instructions for various dishes and cuisines.
    - Techniques: Guidance on cooking methods, ingredient preparation, and kitchen tips.
    - Nutritional Information: Data on calories, protein, fiber, and other nutrients in specific foods or dishes.
    - Ingredients: Substitutions, availability, and tips for using specific ingredients.
    
    The tool ensures users get accurate and helpful cooking insights, tailored to their specific queries.
    """
    response = get_answer(query)  # Use your RAG pipeline to get the response
    return parser.parse(response)
