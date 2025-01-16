from dotenv import load_dotenv
import os, getpass 
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key")

def gemini():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001")
    return llm



