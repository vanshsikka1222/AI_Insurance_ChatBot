**Comprehensive Report: AI-Powered Insurance Policy Information Chatbot**

---

### **1. Introduction**

Insurance companies often face challenges in providing quick and accurate responses to customer inquiries regarding various policy types such as health, life, auto, and home insurance. To solve this problem, we developed an **AI-powered insurance chatbot** that uses Natural Language Processing (NLP) to understand user queries and respond with relevant information extracted from a knowledge base of insurance documents.

---

### **2. Objective**

The goal was to build a chatbot that:
- Understands natural language queries from customers.
- Retrieves relevant information from policy documents.
- Provides instant, accurate answers.
- Escalates complex issues to human agents when needed.
- Offers a simple and intuitive web-based user interface.

---

### **3. Methodology**

#### **3.1 Language Model Selection**
- We chose **Hugging Face's DistilBERT** for question-answering. It is lightweight, does not require an API key, and runs locally, making it a great open-source alternative to proprietary models like OpenAI’s GPT.

#### **3.2 Knowledge Base Creation**
- Policy documents were loaded from PDFs using `PyPDF2`.
- Text was split into manageable chunks using Langchain's `CharacterTextSplitter`.
- These chunks were indexed for retrieval using `FAISS`, an efficient similarity search library.

#### **3.3 Retrieval-Based QA Pipeline**
- A retrieval-based system was implemented using `RetrievalQA` with DistilBERT as the answering model.
- The chatbot matches user questions with relevant document chunks and extracts the best possible answer using the DistilBERT pipeline.

#### **3.4 User Interface**
- Developed with **Streamlit** for rapid prototyping and ease of deployment.
- The interface includes:
  - A title and input field for user questions.
  - A display area for chatbot answers.
  - An expandable section showing document sources.

#### **3.5 Fallback Mechanism**
- When no relevant context is found or a failure occurs, a fallback message is triggered, prompting the user to contact human support.

---

### **4. Results**

- The chatbot was successfully able to:
  - Load multiple PDF documents.
  - Respond to natural language questions with high accuracy.
  - Retrieve answers along with sources.
- Example successful queries:
  - "What does the health insurance policy cover?"
  - "How can I file an auto insurance claim?"
  - "What is not covered under this policy?"

---

### **5. Conclusion**

The implemented approach was selected for the following reasons:
- **Local execution** using Hugging Face avoids dependency on external APIs.
- **DistilBERT** balances speed and accuracy, suitable for real-time QA.
- **Streamlit** enables fast UI development and deployment.
- **FAISS** provides fast and scalable document search.

This chatbot can be further enhanced with:
- User authentication.
- Human-agent live chat integration.
- Voice input/output.
- Dynamic policy update mechanisms.

---

### **6. Demo and Submission**

A live demonstration was recorded showcasing:
- Chatbot answering insurance-related queries.
- Real-time Streamlit UI in action.
- Document retrieval and fallback mechanisms.

> **Note**: The complete source code and sample PDF documents are included in the project repository for testing and further enhancement.

