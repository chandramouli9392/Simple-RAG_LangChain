import streamlit as st

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from transformers import pipeline

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Website RAG Bot", layout="centered")

# -------------------------------------------------
# Floating Chatbot CSS
# -------------------------------------------------
st.markdown("""
<style>
#chatbot-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #2563eb;
    color: white;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 28px;
    border: none;
    cursor: pointer;
    z-index: 1000;
}
#chatbox {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 320px;
    height: 420px;
    background: white;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.25);
    z-index: 1000;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

# -------------------------------------------------
# Load RAG Pipeline (Cached)
# -------------------------------------------------
@st.cache_resource
def load_rag():
    loader = TextLoader("langchaintesting.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    llm_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        max_new_tokens=150
    )

    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    prompt = PromptTemplate.from_template(
        """Answer the question using ONLY the context below.
If the answer is not present, say:
"I can only answer questions related to this website."

Context:
{context}

Question:
{question}
"""
    )

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    return rag_chain


rag = load_rag()

# -------------------------------------------------
# Floating Chatbot Button
# -------------------------------------------------
if st.button("🤖", key="chatbot-btn"):
    st.session_state.show_chat = not st.session_state.show_chat

# -------------------------------------------------
# Chat Window
# -------------------------------------------------
if st.session_state.show_chat:
    st.markdown("<div id='chatbox'>", unsafe_allow_html=True)

    st.markdown("### 🤖 Website Assistant")

    user_question = st.text_input(
        "Ask a question:",
        key="chat_input",
        placeholder="Example: What is an AI Agent?"
    )

    if user_question:
        with st.spinner("Thinking..."):
            answer = rag.invoke(user_question)

        st.markdown("**Answer:**")
        st.write(answer)

    if st.button("❌ Close Chat"):
        st.session_state.show_chat = False

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# Main Page Content (Optional)
# -------------------------------------------------
st.title("Website RAG Assistant")
st.write(
    "Click the 🤖 button in the bottom-right corner to ask questions "
    "related **only** to this website."
)
