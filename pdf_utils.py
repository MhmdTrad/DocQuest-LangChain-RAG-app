from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import  RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

import re
from langdetect import detect
from pyarabic.araby import normalize_hamza, strip_tatweel, strip_tashkeel 
import streamlit as st

def process_pdf(pdf_file):
    with st.spinner('Please wait 🌸'):
        text = ""
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = text_splitter.split_text(text=text)
        return  chunks
def get_vectorstore(chunks):
    with st.spinner('Please wait 🌸'):
        embeddings = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v1",
                                                model_kwargs={'device': 'cpu'})
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

        return vectorstore


def process_question(user_question, vectorstore):
    with st.spinner('Please wait for response😊...'):
        
        llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=os.getenv("GOOGLE_API_KEY"),
                                    temperature=0.3, convert_system_message_to_human=True, max_output_tokens= 5000 )
        prompt_template = """
                            **PDF Reader Expert**

                            **Context:**

                            {context}

                            **Instructions:**

                            As the PDF Reader Expert, your goal is to assist with information from the PDF. 

                            - If someone asks for a summary of the PDF, provide a summary of its content.
                            - If the question is unrelated to the PDF, kindly guide the person to ask something relevant.

                            **Question:**

                            {question}

                            **Answer:**
                        """.strip()
        prompt = ChatPromptTemplate.from_template(prompt_template)
        retriever = vectorstore.as_retriever()
        chain = (
                    {"context": retriever, "question": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
                )
        response = chain.invoke(user_question)

        return response

def PrepChunks(chunks):
    """
    This function preprocesses a list of text chunks, but only if they are Arabic.

    Args:
        chunks: The list of text chunks to preprocess.

    Returns:
        The preprocessed list of text chunks.
    """
    preprocessed_chunks = [
        chunk if detect(chunk) != 'ar' else re.sub(r'[,\t\n\r\x0b\x0c]', ' ', strip_tatweel(strip_tashkeel(chunk))).strip()
        for chunk in chunks
    ]
    return preprocessed_chunks
