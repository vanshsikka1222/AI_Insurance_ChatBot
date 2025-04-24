import os
import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory

# Load Hugging Face model for question answering
qa_pipeline = pipeline("question-answering")

def load_pdfs_and_create_contexts(pdf_folder):
    all_text = []
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            reader = PdfReader(os.path.join(pdf_folder, pdf_file))
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text("\n".join(all_text))

    docs = [Document(page_content=t) for t in texts]
    return docs

def create_chatbot_chain(docs):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def get_answer_from_model(question, context):
        result = qa_pipeline(question=question, context=context)
        return result['answer']

    def retrieve_best_context(query, docs):
        # Simple retrieval based on word overlap score
        query_words = set(query.lower().split())
        best_doc = max(docs, key=lambda d: len(query_words & set(d.page_content.lower().split())))
        return best_doc

    class SimpleRetriever:
        def get_relevant_documents(self, query):
            return [retrieve_best_context(query, docs)]

    retriever = SimpleRetriever()

    class SimpleQAChain:
        def __call__(self, inputs):
            query = inputs["query"]
            context_doc = retriever.get_relevant_documents(query)[0]
            answer = get_answer_from_model(query, context_doc.page_content)
            return {
                "result": answer,
                "source_documents": [context_doc]
            }

    return SimpleQAChain()

# Streamlit UI
st.set_page_config(page_title="Insurance Chatbot 🤖", layout="centered")

st.markdown("## 🛡️ Insurance Policy Chatbot")
st.markdown("Welcome! Ask any questions about **Life**, **Health**, **Auto**, or **Home Insurance** and get instant answers.")
st.divider()

# Load docs and QA chain only once
if "docs" not in st.session_state:
    with st.spinner("📚 Loading insurance documents..."):
        st.session_state.docs = load_pdfs_and_create_contexts("pdfs")
        st.session_state.qa_chain = create_chatbot_chain(st.session_state.docs)
    st.success("Knowledge base loaded successfully!")

# Input field
st.markdown("### 🔍 Ask a Question")
query = st.text_input("Type your question below:", placeholder="E.g., What is covered in life insurance?")

# Chat output
if query:
    with st.spinner("🧠 Thinking..."):
        try:
            result = st.session_state.qa_chain({"query": query})
            st.success("✅ Answer: " + result["result"])
            with st.expander("📄 Source document preview"):
                for i, doc in enumerate(result["source_documents"], 1):
                    st.markdown(f"**Source {i}:**")
                    st.write(doc.page_content[:300] + "...")
        except Exception as e:
            st.error("⚠️ Sorry, I couldn't answer your question.")
            st.info("💡 Please contact [support@insurancecorp.com](mailto:support@insurancecorp.com) for help.")
            st.code(str(e), language="bash")
