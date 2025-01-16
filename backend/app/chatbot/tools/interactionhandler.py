import yaml, sys
sys.path.append('model')
from langchain.agents import tool 
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from geminillm import gemini #type: ignore
from langchain.prompts import PromptTemplate
from langchain.globals import set_debug

with open('config.yaml') as config_file:
    config_file = yaml.safe_load(config_file)

llm = gemini()

# set_debug(True)

class Input(BaseModel):
    code: str = Field(description="should be code")

class Output(BaseModel):
    response: str = Field(description="should be refactored code")

parser = StrOutputParser(pydantic_object=Output)


@tool("interactionhandler", args_schema=Input, return_direct=True)
def interactionhandler(query: str) -> str:
    """
    Use this tool to respond to greetings.
    - Offer a warm response to common greetings such as "Good morning", "Hello", "Hi" etc.
    - Focus on delivering brief and appropriate replies without delving into additional information or context.
    """
    template = config_file["interactionhandler_template"]
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke(query)
    return parser.parse(response)