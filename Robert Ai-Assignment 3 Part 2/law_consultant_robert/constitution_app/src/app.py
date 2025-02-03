import os
import json
import streamlit as st
from pymongo import MongoClient
import logging
import time
import pandas as pd
import fitz  # PyMuPDF for PDF processing
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Setup logging
logging.basicConfig(level=logging.INFO)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://AdvancedProgramming:AdvancedProgramming@cluster0.uemob.mongodb.net/test?retryWrites=true&w=majority")
db = client.support_bot
dialogue_collection = db.dialogues

# Load Constitution JSON Dataset
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "dataset", "constitution.json")
try:
    with open(json_path, "r", encoding="utf-8") as f:
        constitution = json.load(f)
        logging.info("Constitution JSON file loaded successfully.")
except FileNotFoundError:
    logging.error(f"Constitution JSON file not found: {json_path}")
    constitution = {}
except Exception as e:
    logging.error(f"Error loading Constitution JSON file: {str(e)}")
    constitution = {}

# Function to load dataset into MongoDB
def load_dataset():
    try:
        train_data = pd.read_csv("EmpatheticDialogues/train.csv")
        dialogues = train_data[["prompt", "utterance"]].drop_duplicates().dropna()
        dialogue_collection.insert_many(dialogues.to_dict(orient="records"), ordered=False)
        logging.info("EmpatheticDialogues dataset loaded into MongoDB.")
    except Exception as e:
        logging.info("Dataset already exists or encountered an error.")

# Load the EmpatheticDialogues dataset into MongoDB
load_dataset()

# Function to find response from MongoDB
def find_response(user_input):
    result = dialogue_collection.find_one({"prompt": {"$regex": user_input, "$options": "i"}})
    return result["utterance"] if result else None

# Function to store query and response in MongoDB
def store_query_response(user_input, assistant_response):
    dialogue_collection.insert_one({
        "prompt": user_input,
        "utterance": assistant_response,
        "timestamp": time.time()
    })
    logging.info(f"Stored query and response in MongoDB: {user_input} - {assistant_response}")

# Function to handle file upload
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "pdf":
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            file_text = "\n".join([page.get_text("text") for page in doc])
        else:
            file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        return file_text[:500]  # Preview the first 500 characters
    return ""

# Multi-Query Prompt
multi_query_template = """You are an AI assistant. Generate five different versions of the user's question to improve document retrieval.\nUser question: {question}"""

prompt_perspectives = ChatPromptTemplate.from_template(multi_query_template)

def get_multi_queries(question):
    """Generate multiple reformulations of the query."""
    generate_queries = (
        prompt_perspectives
        | ChatOpenAI(temperature=0)
        | StrOutputParser()
        | (lambda x: x.split("\n"))
    )
    return generate_queries.invoke({"question": question})

# Reciprocal Rank Fusion (RRF)
def reciprocal_rank_fusion(results: list[list], k=60):
    """RRF for merging multi-query search results."""
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)
    return [loads(doc) for doc, _ in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)]

def handle_question(query, retriever):
    """Enhanced retrieval using Multi-Query and RRF."""
    queries = get_multi_queries(query)
    retrieved_docs = [retriever.get_relevant_documents(q) for q in queries]
    reranked_docs = reciprocal_rank_fusion(retrieved_docs)
    return reranked_docs[:5]  # Return top 5 results

# Initialize Vectorstore
vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

def query_pipeline(query):
    """Query pipeline to retrieve and display responses."""
    return handle_question(query, retriever)

# Streamlit UI
def main():
    st.title("Chat with Robert ['-']")
    logging.info("App started")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "phi3"])
    logging.info(f"Model selected: {model}")
    
    for message in reversed(st.session_state.messages):
        with st.chat_message(message.role):
            st.write(message.content)
    
    prompt = st.text_input("Enter your question:", key="user_prompt")
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
    send_button = st.button("Send")
    
    if send_button:
        file_text = handle_file_upload(uploaded_file)
        full_prompt = f"{prompt}\n\n[File Content Preview]: {file_text}" if file_text else prompt
        
        if not full_prompt.strip():
            st.error("Please enter text or upload a file.")
        else:
            response_message = query_pipeline(full_prompt)
            response_text = "\n".join([doc["content"] for doc in response_message]) if response_message else "I'm sorry, I couldn't process your request."
            st.write(response_text)
            store_query_response(full_prompt, response_text)

if __name__ == "__main__":
    main()
