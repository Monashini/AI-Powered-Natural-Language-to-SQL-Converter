import streamlit as st
import sqlite3
import pandas as pd
import re
from transformers import T5Tokenizer, T5ForConditionalGeneration

# ---------------- LOAD MODEL ---------------- #
tokenizer = T5Tokenizer.from_pretrained("./model")
model = T5ForConditionalGeneration.from_pretrained("./model")

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("students.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS students
             (id INTEGER PRIMARY KEY, name TEXT, marks INTEGER, city TEXT)''')

# Sample data
c.execute("DELETE FROM students")
data = [
    (1, "Alice", 85, "Chennai"),
    (2, "Bob", 72, "Mumbai"),
    (3, "Charlie", 90, "Chennai"),
    (4, "David", 60, "Delhi"),
    (5, "Eva", 88, "Chennai"),
    (6, "Frank", 45, "Mumbai"),
    (7, "Grace", 30, "Delhi")
]
c.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", data)
conn.commit()


# ---------------- AI MODEL FUNCTION ---------------- #
def generate_sql_ai(text):
    prompt = f"""
    Translate English to SQL query.
    Table: students(id, name, marks, city)

    English: {text}
    SQL:
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_length=64,
        num_beams=5,
        early_stopping=True
    )

    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql


# ---------------- FALLBACK (VERY IMPORTANT 🔥) ---------------- #
def fallback_sql(query):
    query = query.lower()
    conditions = []

    # Marks
    if "above" in query or "greater" in query:
        num = re.findall(r'\d+', query)
        if num:
            conditions.append(f"marks > {num[0]}")

    elif "below" in query or "less" in query:
        num = re.findall(r'\d+', query)
        if num:
            conditions.append(f"marks < {num[0]}")

    # City
    if "chennai" in query:
        conditions.append("city = 'Chennai'")
    if "mumbai" in query:
        conditions.append("city = 'Mumbai'")
    if "delhi" in query:
        conditions.append("city = 'Delhi'")

    # Count
    if "count" in query:
        base = "SELECT COUNT(*) FROM students"
    else:
        base = "SELECT * FROM students"

    if conditions:
        return base + " WHERE " + " AND ".join(conditions) + ";"
    else:
        return base + ";"


# ---------------- MAIN GENERATOR ---------------- #
def generate_sql(query):
    ai_sql = generate_sql_ai(query)

    # 🔥 If model gives bad/default output → use fallback
    if "select * from students" in ai_sql.lower() and len(query.split()) > 3:
        return fallback_sql(query)

    return ai_sql


# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="AI Text → SQL", layout="centered")

st.title("🤖 AI Natural Language → SQL Converter")
st.write("Type any English query 👇")

user_input = st.text_input("Enter your query:")

if st.button("Generate SQL 🚀"):

    if user_input.strip() == "":
        st.warning("Please enter a query")
    else:
        sql_query = generate_sql(user_input)

        st.subheader("🧾 Generated SQL:")
        st.code(sql_query, language="sql")

        try:
            result = c.execute(sql_query).fetchall()

            st.subheader("📊 Results:")

            if result:
                df = pd.DataFrame(result, columns=["ID", "Name", "Marks", "City"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No results found")

        except Exception as e:
            st.error(f"SQL Error: {e}")


# ---------------- EXAMPLES ---------------- #
st.markdown("---")
st.markdown("### 💡 Try these:")

st.markdown("""
- students with marks above 80  
- students in chennai  
- students in mumbai with marks below 50  
- count students in delhi  
- top 3 students  
""")