import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load API key
load_dotenv()
gemini_api_key = r'AIzaSyATBUc1UbXZJwNAGkfyHNi_o65GNUdWpqk'

# Set page layout
st.set_page_config(page_title="Alfred", page_icon='/home/muhammad-ahmad-nadeem/Projects/Ai-chatbot/chatapp/src/alfred.png',layout="centered")
st.markdown("""
    <style>
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding-right: 10px;
        margin-bottom: 20px;
    }
    .message {
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 400;
        line-height: 1.4;
        word-wrap: break-word;
    }
    .user {
        background-color: #DCF8C6;
        text-align: right;
        margin-left: 20%;
    }
    .ai {
        background-color: #F1F0F0;
        text-align: left;
        margin-right: 20%;
    }
    </style>
""", unsafe_allow_html=True)


image_path = "src/alfred.png"


# Use columns to display content in the same line
col1, col2 = st.columns([1, 2])  # Adjust the width ratio if needed

with col1:
    if os.path.exists(image_path):
       st.image(image_path, width=250)
    else:
       st.warning(f"Image not found at {image_path}")

with col2:
    st.markdown("<h1 style='text-align: left; font-size: 36px;'>Hi, I'm Alfred</h1>", unsafe_allow_html=True)

# Validate API key
if not gemini_api_key:
    st.error("❌ API key not found. Please set 'api_key' in your .env file.")
    st.stop()

# Initialize chain once
@st.cache_resource
def initialize_chain():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",google_api_key=gemini_api_key)
    loader = TextLoader(r"bio.txt")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=gemini_api_key
    )
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    return ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)

qa_chain = initialize_chain()

# Chat history state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat bubble display area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, message in st.session_state.chat_history:
    role_class = "user" if sender == "You" else "ai"
    st.markdown(f"""
        <div class="message {role_class}">
            <strong style="color: black;">{sender}:</strong><br>
            <span style="color: black;">{message}</span>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Centered input box at the bottom
with st.form("chat_input_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        user_input = st.text_input(
            "", placeholder="Type your message here...", label_visibility="collapsed"
        )
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append(("You", user_input))
    result = qa_chain({"question": user_input})
    ai_response = result["answer"]
    st.session_state.chat_history.append(("Alfred", ai_response))
    st.rerun()
