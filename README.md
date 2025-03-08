RAG-Based Chatbot using Gemini and FAISS
========================================

Overview
--------

This project implements a **Retrieval-Augmented Generation (RAG) chatbot** using **Google Gemini**, **FAISS**, and **LangChain**. The chatbot loads a text document, splits it into chunks, embeds it using Google Generative AI embeddings, and retrieves relevant information for conversational responses.

Features
--------

*   Uses **Gemini-2.0 Flash** for generating responses.
    
*   Implements **Conversational Memory** to maintain chat history.
    
*   Loads and processes documents using **TextLoader** and **RecursiveCharacterTextSplitter**.
    
*   Uses **FAISS** for efficient document retrieval.
    
*   Supports an interactive chat interface.
    

Requirements
------------

### Prerequisites

Ensure you have Python installed (>=3.8) and install the required dependencies:

    pip install langchain langchain_google_genai faiss-cpu python-dotenv

Setup
-----

1.  **Create and configure your API key:**
    
    *   Sign up for **Google AI Studio** and obtain an API key.
        
    *   Create a file named `.env` (or `api.env` as used in the script) and add:
        
            api_key=YOUR_GEMINI_API_KEY
        
2.  **Prepare your text file:**
    
    *   Store the document (e.g., `bio.txt`) in the same directory.
        
3.  **Run the chatbot:**
    
        python chatbot.py
    

Code Breakdown
--------------

### 1\. **Load API Key**

The script loads the API key from `api.env`:

    from dotenv import load_dotenv
    import os
    load_dotenv("api.env")
    gemini_api_key = os.getenv("api_key")

### 2\. **Initialize Language Model and Load Documents**

    from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    llm = GoogleGenerativeAI(api_key=gemini_api_key, model="gemini-2.0-flash")
    loader = TextLoader(r'bio.txt')
    docs = loader.load()

### 3\. **Split and Embed Documents**

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    document = text_splitter.split_documents(docs)
    
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=gemini_api_key
    )
    vectorstore = FAISS.from_documents(document, embedding)

### 4\. **Setup Conversational Memory and Chain**

    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationalRetrievalChain
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)

### 5\. **Chat Function**

    def chat():
        print("AI is running...")
        while True:
            query = input("Please enter: ")
            if query.lower() == "quit":
                break
            result = qa({"question": query})
            print(result["answer"])
    
    chat()

Usage
-----

*   **Start the chatbot** and ask questions based on the document.
    
*   **Type** `**quit**` **to exit the chat.**
    

Troubleshooting
---------------

*   Ensure your **API key is valid**.
    
*   If you see authentication errors, confirm `.env` is properly set and installed using `pip install python-dotenv`.
    
*   If **no relevant responses**, check if `bio.txt` contains meaningful content.
    

Future Enhancements
-------------------

*   Improve retrieval with better chunking strategies.
    
*   Implement multi-document support.
    
*   Deploy the chatbot using a web interface.
    

License
-------

This project is open-source under the **MIT License**.