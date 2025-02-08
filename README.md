# 🚀 AskGenie - AI-Powered Content Processing API

AskGenie is an **AI-powered FastAPI service** that allows users to **upload multiple documents and URLs**, extract relevant information, and **ask questions**. The service uses **Google Gemini API** to process queries and fetch relevant data from uploaded content.

---

## ✨ **Features**
✅ Upload multiple **documents (PDFs, text files) and URLs**  
✅ AI-powered **question answering** from uploaded content  
✅ Supports **text extraction from documents and web pages**  
✅ **Google Gemini API** for intelligent query processing  
✅ **Google Cloud Function deployment** for scalability  
✅ **Secure authentication** using **Google Service Accounts**  

---

## 📂 **Project Structure**
```
📁 AskGenie/
 ├️ 📁 app/                      # FastAPI application
 │    ├️ main.py                 # Main API server
 │    ├️ utils.py                # Utility functions for text extraction
 │    ├️ resources.py            # API key and model setup
 │    ├️ typings.py              # API request and response models
 │    ├️ firebase.py             # Firebase integration for data storage
 ├️ 📂 uploads/                  # Directory to store uploaded files
 ├️ 📄 requirements.txt          # Dependencies
 ├️ 📄 .gitignore                # Ignored files (e.g., secrets, logs)
 ├️ 📄 README.md                 # Project documentation
 ├️ 📄 .env                      # Environment variables (DO NOT COMMIT)
```

---

## 🚀 **Deployment on Google Cloud Functions**
This API is designed to be deployed on **Google Cloud Functions**. To deploy:
1. **Enable Cloud Functions** in your **Google Cloud Console**.
2. **Create a Service Account** and download the credentials (`gcp-key.json`).
3. **Set up environment variables** (`.env`) to include:
   ```
   API_KEY="your-gemini-api-key"
   MODEL="gemini-1.5-flash"
   GCP_KEY_PATH="gcp-key.json"
   LOCAL_PATH="uploads"
   ```
4. **Deploy to Google Cloud Functions**:
   ```sh
   gcloud functions deploy askgenie --runtime python39 --trigger-http --allow-unauthenticated
   ```

---

## 🔧 **Installation & Setup**
### **Step 1: Clone the Repository**
```sh
git clone https://github.com/babarali581/AskGenie.git
cd AskGenie
```

### **Step 2: Create a Virtual Environment**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```sh
pip install -r requirements.txt
```

### **Step 4: Set Up Environment Variables**
Create a `.env` file in the project root and add:
```
API_KEY="your-gemini-api-key"
MODEL="gemini-1.5-flash"
GCP_KEY_PATH="gcp-key.json"
LOCAL_PATH="uploads"
```

### **Step 5: Run the FastAPI Server**
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API will be available at: `http://127.0.0.1:8000`

---

## 🔥 **Core API Endpoints**
### 1️⃣ **Upload Files & URLs**
**Endpoint:** `POST /upload/`  
**Description:** Uploads **multiple files and URLs**, extracts text, and stores them in Firebase.

📌 **Request:**
```json
{
  "urls": ["https://example.com"],
  "files": [UploadFile]
}
```

📌 **Response:**
```json
{
  "files": {"document.pdf": "content_id"},
  "urls": {"https://example.com": "content_id"}
}
```

---

## 🔐 **Authentication & Security**
1. **Google Service Account:**  
   - You need a **Google Cloud Service Account** with access to **Cloud Functions & Firestore**.
   - Store the service account JSON file as **`gcp-key.json`**.
   - Never commit `gcp-key.json` (already in `.gitignore`).
  
2. **API Key Authentication:**  
   - Gemini API requires an **API Key** (stored in `.env`).
  
3. **CORS Configuration:**  
   - API is configured to allow **cross-origin requests**.

---

## 🤝 **How to Contribute**
Contributions are welcome! Follow these steps:
1. **Fork the repository**.
2. **Clone your fork**:
   ```sh
   git clone https://github.com/yourusername/AskGenie.git
   cd AskGenie
   ```
3. **Create a new branch**:
   ```sh
   git checkout -b feature-name
   ```
4. **Make changes & commit**:
   ```sh
   git add .
   git commit -m "Added new feature"
   ```
5. **Push your changes**:
   ```sh
   git push origin feature-name
   ```
6. **Open a Pull Request**.

---

## 🐝 **License**
This project is licensed under the **MIT License**. Feel free to modify and use it.

---

## 🌟 **Acknowledgments**
- Built using **FastAPI, Firebase, and Gemini API**
- Inspired by **AI-driven document processing tools**
- Hosted on **Google Cloud Functions**

---

### 🔗 **Follow & Support**
- **GitHub Repo:** [AskGenie](https://github.com/babarali581/AskGenie)
- **Author:** [babarali581](https://github.com/babarali581)
- **Contribute & Improve!** 🚀

