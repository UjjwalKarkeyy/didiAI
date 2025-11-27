# didiAI — AI Assistant with RAG, Memory & Interview Booking

didiAI is an AI-powered assistant built with **FastAPI**, **LangChain**, **Gemini**, **Redis**, **SQLite**, and **Vector Search**.  
It supports:

- 📄 Document Ingestion  
- 🔍 RAG-based Question Answering  
- 🧠 Conversational Memory  
- 🤖 Intent Classification  
- 🗂 Multi-Step Interview Booking  
- 🗓 Structured Date/Time Extraction  
- 🧾 SQLite-backed Booking Storage  

---

# 📁 Project Structure

app/
├── api/
│   ├── __init__.py
|   ├── chat.py
│   └── ingestion.py
├── db/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   └── db_session.py
├── rag/
│   ├── __init__.py
│   ├── retriever.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── prompt_builder.py
│   └── vector_store.py
├── services/
│   ├── chat_service.py
│   ├── booking_service.py
│   ├── booking_extractors.py
│   └── ingestion_service.py
├── intent/
│   └── intent_classifier.py
├── state/
│   ├── state_manager.py
│   └── slot_manager.py
├── memory/
│   ├── chat_memory.py
│   └── redis_client.py
├── __init__.py
└── main.py

---

# 📥 **1. Document Ingestion Flow**

### **Ingest Request**
<img src="assets/ingest_request.png" width="600">

### **Ingest Response**
<img src="assets/ingest_response.png" width="600">

---

# 💬 **2. Chat (RAG) Flow**

### **RAG Chat Request**
<img src="assets/doc_chat_request.png" width="600">

### **RAG Chat Response**
<img src="assets/doc_chat_response.png" width="600">

---

# 📝 **3. Interview Booking Flow**

Below is the full slot-filling sequence:  
**name → email → date → time → phone → booking confirmation**

---

## 🔹 Step 1 — User Requests Interview Booking
<img src="assets/interview_book_request.png" width="600">

## 🔹 Step 2 — Assistant Starts Booking Flow
<img src="assets/interview_book_response.png" width="600">

---

## 🔹 Step 3 — User Provides Name
<img src="assets/one_give_name.png" width="600">

## 🔹 Step 4 — Asking for Email
<img src="assets/two_ask_email.png" width="600">

## 🔹 Step 5 — User Provides Email
<img src="assets/three_give_email.png" width="600">

---

## 🔹 Step 6 — Asking for Date
<img src="assets/four_ask_date.png" width="600">

## 🔹 Step 7 — User Provides Date
<img src="assets/five_give_date.png" width="600">

---

## 🔹 Step 8 — Asking for Time
<img src="assets/six_ask_time.png" width="600">

## 🔹 Step 9 — User Provides Time
<img src="assets/seven_give_time.png" width="600">

---

## 🔹 Step 10 — Asking for Phone Number
<img src="assets/eight_ask_phoneNo.png" width="600">

## 🔹 Step 11 — User Provides Phone Number
<img src="assets/nine_give_phoneNo.png" width="600">

---

## ✅ Final Booking Confirmation
<img src="assets/interview_booked_response.png" width="600">

### ✅**SQLite Table (Stored Documents)**
<img src="assets/sqlite_table.png" width="600">

---

# 🧠 How didiAI Works

### 🔹 Session-Based Architecture
- Every ingestion & chat request includes a `session_id`.
- Documents, chat memory, and booking flow are tied to that session.

### 🔹 Intent Classification
The assistant distinguishes between:
- `normal_chat`
- `book_interview`

### 🔹 Slot Filling
Extractors gather:
- **Name**
- **Email**
- **Phone**
- **Date (YYYY-MM-DD)**
- **Time (HH:MM)**

### 🔹 RAG Retrieval
Only documents associated with the current `session_id` are used for context-aware responses.

### 🔹 SQLite Bookings
Final structured booking is stored as:

| Field | Value |
|-------|--------|
| name | user-provided |
| email | extracted |
| phone | extracted |
| date_time | combined UTC datetime |
| session_id | conversation session |

---

# 🚀 Running the Project

### Install Dependencies
```bash
pip install -r requirements.txt
