from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from langchain.chains.question_answering import load_qa_chain
import re
from langdetect import detect
from pyarabic.araby import normalize_hamza, strip_tatweel, strip_tashkeel 
import streamlit as st

def process_pdf_and_get_vectorstore(pdf_file):
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

        embeddings = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v1",
                                        model_kwargs={'device': 'cpu'})
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

        return vectorstore
    
def process_question(user_question, knowledge_base):
    with st.spinner('Please wait for response😊...'):
        context = knowledge_base.similarity_search(user_question)
        llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=os.getenv("GOOGLE_API_KEY"),
                                    temperature=0.3, convert_system_message_to_human=True)
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
        prompt = PromptTemplate(template=prompt_template, input_variables=["question", 'context'])
        chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
        response = chain.run(input_documents=context, question=user_question)
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
