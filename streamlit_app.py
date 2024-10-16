import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime


# เพิ่มรูปภาพด้านบน
st.image('cenic1.jpg', width=700)  # เปลี่ยนเป็นชื่อไฟล์รูปภาพของคุณ



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

    requests = load_data()
    
    # แสดงข้อมูลการขอใช้งานเครื่องมือ
    st.subheader('Current Requests')
    if requests:
        df = pd.DataFrame(requests)
        st.dataframe(df)
    else:
        st.write("No requests found.")

    # ฟอร์มสำหรับขอใช้งานเครื่องมือ
    st.subheader('Request Mercury Analyzer NIC')
    tool_name = st.text_input('Name Model')
    user_name = st.text_input('User Name')
    usage_date = st.date_input('Date of Usage', datetime.today())
    usage_time = st.time_input('Time of Usage', datetime.now().time())
    
    # เพิ่มช่องวันที่และเวลาคืนเครื่องมือ
    return_date = st.date_input('Return Date', datetime.today())
    return_time = st.time_input('Return Time', datetime.now().time())
    
    #reason = st.text_area('Reason for Request')
    remarks = st.text_area('Remarks')

    if st.button('Submit Request'):
        if tool_name and user_name:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            request_data = {
                'tool_name': tool_name,
                'user_name': user_name,
                'usage_datetime': f"{usage_date} {usage_time}",
                'return_datetime': f"{return_date} {return_time}",
                #'reason': reason,
                'remarks': remarks,
                'timestamp': timestamp
            }
            requests.append(request_data)
            save_data(requests)
            st.success('Request submitted successfully!')

    # ลบการขอใช้งานเครื่องมือ
    st.subheader('Remove a Request Only Admin')
    request_to_remove = st.selectbox('Select Request to Remove', 
                                       [f"{req['tool_name']} by {req['user_name']} on {req['usage_datetime']}" for req in requests])

    if st.button('Remove Request'):
        requests = [req for req in requests if f"{req['tool_name']} by {req['user_name']} on {req['usage_datetime']}" != request_to_remove]
        save_data(requests)
        st.success('Request removed successfully!')

if __name__ == '__main__':
    main()
