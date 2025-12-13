import streamlit as st

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="Website RAG Assistant",
    layout="centered"
)

st.title("🔍 Ask About This Website")
st.write("This assistant answers questions **only** from the website content.")

# ----------------------------
# Load RAG Pipeline (Cached)
# ----------------------------
@st.cache_resource
def load_rag():
    # Load text file
    loader = TextLoader("langchaintesting.txt")
    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30
    )
    chunks = splitter.split_documents(documents)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector database
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Retriever (limit chunks to avoid token overflow)
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 2}
    )

    # Lightweight open-source LLM
    llm_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        max_new_tokens=150
    )

    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    # RAG Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return qa_chain

qa = load_rag()

# ----------------------------
# User Input
# ----------------------------
question = st.text_input(
    "Ask a question related to this website:",
    placeholder="Example: What is an AI Agent?"
)

# ----------------------------
# Answer
# ----------------------------
if question:
    with st.spinner("Thinking..."):
        answer = qa(question)

    st.subheader("📌 Answer")
    st.write(answer)
