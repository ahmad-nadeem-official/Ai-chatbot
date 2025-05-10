from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import GoogleGenerativeAI  # Updated import
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

gemini_api_key = "AIzaSyC4t-sTip43k6Wqk8riQESCaeRPfiMyDgE"
llm = GoogleGenerativeAI(api_key='AIzaSyC4t-sTip43k6Wqk8riQESCaeRPfiMyDgE', model="gemini-2.0-flash")

loader = TextLoader(r'/home/muhammad-ahmad-nadeem/Projects/Ai-chatbot/chatapp/bio.txt')
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
document = text_splitter.split_documents(docs)

# Ensure API key is correctly set
gemini_api_key = os.getenv("api_key")
if not gemini_api_key:
    raise ValueError("API Key not found! Set GOOGLE_API_KEY in the environment.")

# Create embedding model
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=gemini_api_key  # Ensure correct argument name
)

# Process documents
vectorstore = FAISS.from_documents(document, embedding)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)

def chat():
  print("ai is running")
  while True:
    query = input("please enetr :")
    if query == "quit":
      break
    result = qa({"question": query})
    print(result["answer"])


chat()    