import re
import yaml, sys
sys.path.append('model')
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
import streamlit as st
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from geminillm import gemini #type: ignore
from geminiembed import embeddings #type: ignore
from langchain.globals import set_debug

set_debug(True)

def remove_markdown_formatting(text):
    """
    Strips Markdown-like formatting (** for bold, * for lists) from the text.
    """
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove bold (**text**)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Remove italic or list (*text*)
    return text.strip()

with open('config.yaml') as config_file:
    config_file = yaml.safe_load(config_file)

loader = PyPDFLoader('data\Indian-Recipes.pdf')
data = loader.load()
print(len(data))

template = config_file['rag_template']

def text_splitter(data):
    splitter = RecursiveCharacterTextSplitter(chunk_size= 1000, chunk_overlap = 200)
    docs = splitter.split_documents(data)
    return docs

docs= text_splitter(data)
# print(docs)

embedding_data=embeddings()

vector_store = Chroma.from_documents(documents=docs, embedding=embedding_data)

llm = gemini()

def get_answer(query):
    context = vector_store
    prompt = PromptTemplate(input_variable=["relevant_passage", "question"], template=template)
    retriever = vector_store.as_retriever(search_type="similarity", k=3)
    retrieval = RunnableParallel({"relevant_passage": retriever, "question": RunnablePassthrough()})
    chain = retrieval| prompt| llm| StrOutputParser()
    response = chain.invoke(query)
    return remove_markdown_formatting(response)

class Input(BaseModel):
    query: str = Field(description="should be question")

class Output(BaseModel):
    response: str = Field(description="should be the answer")

parser = StrOutputParser(pydantic_object=Output)
