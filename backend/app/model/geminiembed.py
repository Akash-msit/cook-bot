from dotenv import load_dotenv
import os, getpass
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key")

def embeddings():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return embeddings
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# vector = embeddings.embed_query("My name is Akash Dey")
# print(vector[:5])