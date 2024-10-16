import streamlit as st

st.title("🎈 My new appaaaaaaa")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

import sqlite3

# สร้างฐานข้อมูลและตาราง
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# สร้างตารางสำหรับสินค้า
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
''')

# เพิ่มข้อมูลตัวอย่าง
c.execute("INSERT INTO products (name, description, price, stock) VALUES ('Product A', 'Description A', 100.0, 10)")
c.execute("INSERT INTO products (name, description, price, stock) VALUES ('Product B', 'Description B', 150.0, 5)")
c.execute("INSERT INTO products (name, description, price, stock) VALUES ('Product C', 'Description C', 200.0, 0)")

conn.commit()
conn.close()

import streamlit as st
import pandas as pd
import sqlite3

# ฟังก์ชันเพื่อเชื่อมต่อฐานข้อมูล
def get_connection():
    conn = sqlite3.connect('inventory.db')
    return conn

# ฟังก์ชันเพื่อดึงข้อมูลสินค้า
def load_data():
    conn = get_connection()
    query = "SELECT * FROM products"
    data = pd.read_sql(query, conn)
    conn.close()
    return data

# สร้างส่วนของแอป Streamlit
st.title("Inventory Management System")

# โหลดข้อมูล
data = load_data()

# แสดงข้อมูล
st.subheader("Product List")
st.write(data)

# ฟอร์มเพิ่มสินค้า
st.subheader("Add New Product")
with st.form(key='add_product'):
    name = st.text_input("Product Name")
    description = st.text_input("Description")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    stock = st.number_input("Stock", min_value=0)

    submit_button = st.form_submit_button("Add Product")
    if submit_button:
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)", 
                  (name, description, price, stock))
        conn.commit()
        conn.close()
        st.success("Product added successfully!")

# ปุ่ม Refresh
if st.button("Refresh"):
    st.experimental_rerun()
