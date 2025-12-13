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
# PAGE CONFIG (IMPORTANT)
# -------------------------------------------------
st.set_page_config(
    page_title="Website RAG Bot",
    layout="wide"
)

# -------------------------------------------------
# GLOBAL CSS (FIXES WHITE PANEL & LAYOUT)
# -------------------------------------------------
st.markdown("""
<style>

/* Hide sidebar completely */
section[data-testid="stSidebar"] {
    display: none;
}

/* Center main content and limit width */
.block-container {
    max-width: 900px;
    padding-top: 3rem;
}

/* Floating chatbot button */
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

/* Floating chat window */
#chatbox {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 340px;
    height: 420px;
    background: #ffffff;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.25);
    z-index: 1000;
    overflow-y: auto;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

# -------------------------------------------------
# LOAD RAG PIPELINE (CACHED)
# -------------------------------------------------
@st.cache_resource
def load_rag():
    # Load website text
    loader = TextLoader("langchaintesting.txt")
    docs = loader.load()

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30
    )
    chunks = splitter.split_documents(docs)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector DB
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # LLM
    llm_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        max_new_tokens=150
    )
    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    # Prompt
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

    # LCEL RAG chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    return rag_chain


rag = load_rag()

# -------------------------------------------------
# FLOATING CHATBOT BUTTON
# -------------------------------------------------
if st.button("🤖", key="chatbot-btn"):
    st.session_state.show_chat = not st.session_state.show_chat

# -------------------------------------------------
# FLOATING CHAT WINDOW
# -------------------------------------------------
if st.session_state.show_chat:
    st.markdown("<div id='chatbox' style='pointer-events:auto;'>", unsafe_allow_html=True)

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
# MAIN PAGE CONTENT (CLEAN)
# -------------------------------------------------
st.markdown("## Website RAG Assistant")
st.write(
    "Click the 🤖 chatbot icon in the bottom-right corner to ask questions "
    "related **only** to this website."
)
