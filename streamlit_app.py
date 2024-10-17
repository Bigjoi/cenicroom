import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ใส่ที่อยู่ของภาพ
#image_path = "cenic1.jpg"

# แสดงภาพโดยปรับขนาดอัตโนมัติ
#st.image(image_path, use_column_width=True)

st.markdown(
    """
    <style>
    .video-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    .video-background iframe {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        transform: translate(-50%, -50%);
        pointer-events: none; /* ป้องกันการคลิก */
    }
    .content {
        position: relative;
        z-index: 1;
        color: white; /* เปลี่ยนสีข้อความ */
        text-align: center;
        padding: 20px;
    }
    </style>
    <div class="video-background">
        <iframe src="https://www.youtube.com/embed/EsptM4ULxgI?autoplay=1&mute=1&loop=1&playlist=EsptM4ULxgI" frameborder="0" allowfullscreen></iframe>
    </div>
    <div class="content">
    </div>
    """,
    unsafe_allow_html=True
)

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
