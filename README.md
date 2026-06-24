## 📂 Project Structure

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=700&size=24&pause=1000&color=36BCF7&center=true&vCenter=true&width=700&lines=Clean+Project+Architecture;Modular+RAG+Pipeline;Easy+to+Understand+for+Beginners" />

</div>

```text
📦 simple-rag
│
├── 📄 app.py
│   ├── Streamlit User Interface
│   ├── Chatbot Logic
│   └── RAG Pipeline Execution
│
├── 📄 langchaintesting.txt
│   └── Knowledge Base / Source Document
│
├── 📄 requirements.txt
│   └── Project Dependencies
│
├── 📄 README.md
│   └── Project Documentation
│
└── 📁 assets
    ├── 🖼️ screenshots
    └── 🎥 demo.gif
```

---

### 🔍 File Responsibilities

| File                   | Purpose                                          |
| ---------------------- | ------------------------------------------------ |
| `app.py`               | Main Streamlit application and chatbot interface |
| `langchaintesting.txt` | Document used as the knowledge source            |
| `requirements.txt`     | Python package dependencies                      |
| `README.md`            | Project documentation                            |
| `assets/`              | Screenshots, GIFs and project visuals            |

---

### ⚡ RAG Processing Flow

```mermaid
flowchart TD

A["📄 langchaintesting.txt"]
--> B["✂️ Text Chunking"]

B --> C["🧠 Sentence Transformers"]

C --> D["⚡ FAISS Vector Store"]

E["👤 User Query"]
--> F["🔍 Similarity Search"]

F --> D

D --> G["📚 Relevant Context"]

G --> H["🤖 FLAN-T5 LLM"]

H --> I["✨ Final Answer"]
```

<div align="center">

### 🚀 Simple Yet Powerful Architecture

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&height=120&section=header&text=Document%20→%20Embeddings%20→%20Retrieval%20→%20Generation&fontSize=25&fontColor=fff" />

</div>
