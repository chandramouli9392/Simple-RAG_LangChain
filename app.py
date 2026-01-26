import streamlit as st

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(page_title="Website RAG Assistant")
st.title("🔍 Ask About This Website")

# ----------------------------
# Load RAG Pipeline (Cached)
# ----------------------------
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

    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

    llm_pipeline = pipeline(
        task="text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=150
    )

    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    prompt = PromptTemplate.from_template(
        """Answer the question using only the context below.
If the answer is not in the context, say "I can only answer based on this website."

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
        answer = rag.invoke(question)

    st.subheader("📌 Answer")
    st.write(answer)
