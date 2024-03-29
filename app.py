from dotenv import load_dotenv
import streamlit as st
import os
from htmlTemplates import css, bot_template, page_bg_img, footer
from pdf_utils import process_pdf,get_vectorstore, process_question, PrepChunks


def main():
    load_dotenv()
    # Apply the HTML and JavaScript
    st.set_page_config(page_title="Ask your PDF 🦜️🔗")

    st.write(css,unsafe_allow_html=True)
    st.markdown(page_bg_img, unsafe_allow_html=True)
    # st.header("Ask your PDF 💬 ")
    st.markdown("<h1 class='title'>DocQuest 💬</h1>", unsafe_allow_html=True)
    
    # upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    # Extract the text
    if pdf is not None:
        # Create the chunks then the  embeddings
        chunks = process_pdf(pdf)
        if chunks:
            vectorstore = get_vectorstore(chunks)

            greeting ="Hi, I'm DocQuest your assistant, happy to meet you"
            st.write(bot_template.replace("{{MSG}}", greeting), unsafe_allow_html=True)
            # show user input
            user_question = st.text_input("Ask a question about your PDF:")
            if user_question:  # Check if the user has provided a question
                response = process_question(user_question, vectorstore)

                st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)
        else:
            handling_error = "Please try differnet PDF contains texts 😊"
            st.write(bot_template.replace("{{MSG}}", handling_error), unsafe_allow_html=True)
            pass
if __name__ == '__main__':
    main()

st.markdown(footer, unsafe_allow_html=True)
