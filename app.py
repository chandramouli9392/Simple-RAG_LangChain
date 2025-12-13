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
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Website RAG Bot", layout="wide")

# -------------------------------------------------
# GLOBAL CSS (FIXED BOT ICON + CHATBOX)
# -------------------------------------------------
st.markdown("""
<style>

/* Hide sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Center main content */
.block-container {
    max-width: 900px;
    padding-top: 3rem;
}

/* Floating bot toggle (checkbox disguised as button) */
div[data-testid="stCheckbox"] {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000;
}

/* Hide checkbox label */
div[data-testid="stCheckbox"] label {
    display: none;
}

/* Style checkbox as bot icon */
div[data-testid="stCheckbox"] input[type="checkbox"] {
    appearance: none;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #2563eb;
    cursor: pointer;
}

div[data-testid="stCheckbox"] input[type="checkbox"]::after {
    content: "🤖";
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: white;
    height: 100%;
}

/* Floating chatbox */
#chatbox {
    position: fixed;
    bottom: 95px;
    right: 20px;
    width: 340px;
    height: 420px;
    background: white;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.25);
    z-index: 1000;
    overflow-y: auto;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD RAG PIPELINE (CACHED)
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
If the answer is not in the context, say:
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
# BOT ICON TOGGLE (THIS NEVER MOVES)
# -------------------------------------------------
open_chat = st.checkbox("", key="bot_toggle")

# -------------------------------------------------
# CHAT WINDOW
# -------------------------------------------------
if open_chat:
    st.markdown("<div id='chatbox'>", unsafe_allow_html=True)

    st.markdown("### 🤖 Website Assistant")

    user_question = st.text_input(
        "Ask a question:",
        placeholder="Example: What is an AI Agent?",
        key="chat_input"
    )

    if user_question:
        with st.spinner("Thinking..."):
            answer = rag.invoke(user_question)

        st.markdown("**Answer:**")
        st.write(answer)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# MAIN PAGE CONTENT
# -------------------------------------------------
st.markdown("## Website RAG Assistant")
st.write(
    "Click the 🤖 bot icon in the bottom-right corner to ask questions "
    "related **only** to this website."
)
