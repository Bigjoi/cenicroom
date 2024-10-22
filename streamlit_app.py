import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ฟังก์ชันสำหรับสร้างฐานข้อมูลและตาราง
def create_database():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            tool_name TEXT,
            user_name TEXT,
            usage_datetime TEXT,
            return_datetime TEXT,
            remarks TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ฟังก์ชันสำหรับบันทึกข้อมูลลงในฐานข้อมูล
def save_data_to_db(request_data):
    with sqlite3.connect('requests.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO requests (tool_name, user_name, usage_datetime, return_datetime, remarks, timestamp) VALUES (?, ?, ?, ?, ?, ?)', 
                  (request_data['tool_name'], request_data['user_name'], request_data['usage_datetime'], request_data['return_datetime'], request_data['remarks'], request_data['timestamp']))
        conn.commit()

# ฟังก์ชันสำหรับโหลดข้อมูลจากฐานข้อมูล
def load_data_from_db():
    with sqlite3.connect('requests.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM requests')
        return c.fetchall()

# ฟังก์ชันหลัก
def main():
    create_database()  # สร้างฐานข้อมูลและตารางถ้ายังไม่มี
    st.title('Hg CENIC Request System')

    # โหลดข้อมูลจากฐานข้อมูล
    requests = load_data_from_db()

    # แสดงข้อมูลการขอใช้งานเครื่องมือ
    st.subheader('Current Requests')
    if requests:
        df = pd.DataFrame(requests, columns=['Tool Name', 'User Name', 'Usage Date', 'Return Date', 'Remarks', 'Timestamp'])
        st.dataframe(df)
    else:
        st.write("No requests found.")

    # ฟอร์มสำหรับขอใช้งานเครื่องมือ
    st.subheader('Request Mercury Analyzer NIC')
    tool_name = st.text_input('Name Model : เช่น MA-3000 NIC-01')
    user_name = st.text_input('User Name : เช่น Natthaphong MI NTP MI')
    usage_date = st.date_input('Date of Usage', datetime.today())
    return_date = st.date_input('Return Date', datetime.today())
    remarks = st.text_area('Remarks')

    if st.button('Submit Request'):
        if tool_name and user_name:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            request_data = {
                'tool_name': tool_name,
                'user_name': user_name,
                'usage_datetime': str(usage_date),
                'return_datetime': str(return_date),
                'remarks': remarks,
                'timestamp': timestamp
            }
            save_data_to_db(request_data)  # บันทึกข้อมูลลงฐานข้อมูล
            st.success('Request submitted successfully!')

    # ลบการขอใช้งานเครื่องมือ
    st.subheader('Remove a Request Only Admin')
    if requests:
        request_to_remove = st.selectbox('Select Request to Remove', 
                                           [f"{req[0]} by {req[1]} on {req[2]}" for req in requests])

        if st.button('Remove Request'):
            with sqlite3.connect('requests.db') as conn:
                c = conn.cursor()
                c.execute('DELETE FROM requests WHERE tool_name=? AND user_name=? AND usage_datetime=?', 
                          (request_to_remove.split(" by ")[0], request_to_remove.split(" by ")[1].split(" on ")[0], request_to_remove.split(" on ")[1]))
                conn.commit()
            st.success('Request removed successfully!')

if __name__ == '__main__':
    main()
