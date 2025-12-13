🤖 Simple RAG – Beginner Friendly Project

A Simple Retrieval-Augmented Generation (RAG) project built using Streamlit + LangChain.
This app allows users to ask questions only from a given text file, just like a website assistant chatbot.
Here I made a Example RAG Using Text File

Perfect for beginners learning RAG 💡

✨ What This Project Does

✅ Reads data from a text file
✅ Converts text into embeddings
✅ Stores data in a vector database (FAISS)
✅ Retrieves relevant content
✅ Generates answers using an LLM
✅ Shows a floating chatbot 🤖 at the bottom-right corner

🧠 What is RAG? (In Simple Words)

RAG = Retrieve + Generate

📄 Retrieve → Find relevant text from documents
🤖 Generate → Use AI to answer based on that text

👉 This avoids wrong answers (hallucinations).

🛠️ Tech Stack Used

🐍 Python

🧩 LangChain (modern LCEL style)

🧠 Sentence Transformers (Embeddings)

📦 FAISS (Vector Database)

🌐 Streamlit (UI)

🤖 FLAN-T5 (Open-source LLM)

📁 Project Structure
simple-rag/
├── app.py
├── langchaintesting.txt
├── requirements.txt
└── README.md

▶️ How to Run the App (Step by Step)
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run Streamlit App
streamlit run app.py

3️⃣ Open in Browser

The app will open automatically 🌐
Click the 🤖 bot icon at the bottom-right corner and ask questions.

📄 Input Data File

All answers come only from this file:

langchaintesting.txt


✏️ You can replace the content with:

Website text

Notes

Documentation

FAQs

🤖 Features

✨ Floating chatbot icon
✨ Clean UI
✨ Beginner-friendly code
✨ No API keys required
✨ Works on Streamlit Cloud
✨ No hallucinated answers

🚀 Deployment

You can deploy this app easily using:

🌥️ Streamlit Cloud

Push code to GitHub

Connect repo on Streamlit Cloud

Deploy 🎉

🧑‍🎓 Who Is This For?

✔ Beginners learning RAG
✔ Students learning LangChain
✔ AI/ML learners
✔ Anyone building website chatbots
