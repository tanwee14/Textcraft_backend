# 🧠 TextCraft Backend

The backend service for **TextCraft** – an AI-powered writing assistant that enhances, corrects, and generates text. This backend handles various **Natural Language Processing (NLP)** tasks via custom or pretrained models.

---

## 🚀 Features

* ✅ Grammar & Spelling Correction (using TextBlob / LanguageTool)
* 🪄 Tone Enhancement (formal, informal, friendly, assertive, etc.)
* 📋 Text Summarization (abstractive + extractive)
* ✏️ Paraphrasing & Rewriting
* 📧 Email & Letter Generation
* 📌 Plagiarism Detection (n-gram + semantic)
* 🌐 Language Translation *(optional)*

---

## 🛠️ Tech Stack

* **Flask** or **FastAPI** (API Framework)
* **Transformers (Hugging Face)** for paraphrasing/summarization
* **TextBlob / LanguageTool** for grammar correction
* **Scikit-learn, NLTK, or spaCy** for NLP preprocessing
* **PyTorch or TensorFlow** (if using custom models)

---


## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/tan_wee/Textcraft-backend.git
cd textcraft-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Backend

### FastAPI (Recommended)

```bash
uvicorn app.main:app --reload
```

### Flask (Alternative)

```bash
python app/main.py
```

## 📄 Example Request

**POST** `/summarize`

```json
{
  "text": "TextCraft is a writing assistant that can correct grammar and summarize documents for you."
}
```

**Response**

```json
{
  "summary": "TextCraft helps correct grammar and summarize documents."
}
```

---

## ✅ TODO

* [ ] Add JWT Authentication
* [ ] Add support for more tones
* [ ] Support for document uploads (.txt/.docx/.pdf)
* [ ] Integrate with frontend (React)

---

## 🛡 License

MIT License. Use freely with attribution.

