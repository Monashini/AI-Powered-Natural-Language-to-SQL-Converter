# 🤖 AI-Powered Natural Language to SQL Converter

## 📌 Overview

This project is an AI-based system that converts natural language queries into SQL statements. It allows users to interact with databases using plain English instead of writing SQL manually.

The system uses a fine-tuned transformer model (**FLAN-T5**) along with a fallback rule-based mechanism to ensure accurate and reliable query generation.

---

## 🚀 Features

* 🔹 Convert English queries into SQL
* 🔹 Supports conditions (marks, city, etc.)
* 🔹 Hybrid AI + rule-based system
* 🔹 Real-time query execution
* 🔹 Interactive Streamlit dashboard

---

## 🧠 Tech Stack

* Python
* Streamlit
* Transformers (FLAN-T5)
* PyTorch
* SQLite

---

## 📊 Example

### Input:

```
students with marks above 80 in chennai
```

### Output SQL:

```sql
SELECT * FROM students WHERE marks > 80 AND city = 'Chennai';
```

---

## ⚙️ Installation

```bash
python -m pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
python train.py
python -m streamlit run app.py
```

---

## 🏗️ Project Structure

```
├── app.py              # Streamlit application
├── train.py            # Model fine-tuning script
├── model/              # Saved trained model
├── data.csv            # Dataset (if used)
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

1. User enters query in natural language
2. Transformer model converts it to SQL
3. Fallback logic ensures reliability
4. Query is executed on database
5. Results are displayed in dashboard

---

## 🔮 Future Improvements

* Larger training dataset
* More complex SQL support
* Voice-based query input
* ChatGPT-style UI

---

## 👩‍💻 Author

**Monashini S**
B.E CSE (AI & ML)

---

## ⭐ Acknowledgment

* FLAN-T5 model by Google
* Streamlit for UI framework
