import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ใส่ที่อยู่ของภาพ
image_path = "cenic2.jpg"
st.image(image_path, use_column_width=True)

# ฟังก์ชันสำหรับอ่านข้อมูลจากไฟล์ JSON
def load_data():
    if os.path.exists('requests.json'):
        with open('requests.json', 'r') as f:
            return json.load(f)
    return []

# ฟังก์ชันสำหรับบันทึกข้อมูลลงไฟล์ JSON
def save_data(data):
    with open('requests.json', 'w') as f:
        json.dump(data, f)

# ฟังก์ชันหลัก
def main():
    st.title('Hg CENIC Request System')

    # โหลดข้อมูลลงใน session state หากยังไม่มี
    if 'requests' not in st.session_state:
        st.session_state.requests = load_data()

    # แสดงข้อมูลการขอใช้งานเครื่องมือ
    st.subheader('Current Requests')
    if st.session_state.requests:
        df = pd.DataFrame(st.session_state.requests)
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
            st.session_state.requests.append(request_data)
            save_data(st.session_state.requests)
            st.success('Request submitted successfully!')

    # ลบการขอใช้งานเครื่องมือ
    st.subheader('Remove a Request Only Admin')
    if st.session_state.requests:
        request_to_remove = st.selectbox('Select Request to Remove', 
                                           [f"{req['tool_name']} by {req['user_name']} on {req['usage_datetime']}" for req in st.session_state.requests])

        if st.button('Remove Request'):
            st.session_state.requests = [req for req in st.session_state.requests if f"{req['tool_name']} by {req['user_name']} on {req['usage_datetime']}" != request_to_remove]
            save_data(st.session_state.requests)
            st.success('Request removed successfully!')

if __name__ == '__main__':
    main()

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3F0MzBlcWJnM211NHJhNGI0ZTcwbDJreHBsM3Vja3RndTR6bmxnNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dAgEMJ7HKC6jgoxFWp/giphy.gif');
        background-size: cover;
        background-position: center;
        height: 100vh;
    }
    </style>
    """,
    unsafe_allow_html=True
)
