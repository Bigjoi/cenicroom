import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Path to the image
image_path = "cenic2.jpg"

# Display the image with auto-resizing
st.image(image_path, use_column_width=True)

# Database connection details (PostgreSQL)
DB_HOST = "your_host"  # เช่น 'localhost' หรือ 'db.heroku.com'
DB_NAME = "your_database"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_PORT = "5432"  # ปกติแล้วจะเป็น 5432

# Function to create the database and table
def create_database():
    try:
        # เชื่อมต่อกับ PostgreSQL
        conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
        c = conn.cursor()

        # สร้างตาราง requests หากไม่มี
        c.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id SERIAL PRIMARY KEY,
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
    except Exception as e:
        st.error(f"Error creating database: {e}")

# Function to save data to the database
def save_data_to_db(request_data):
    try:
        # เชื่อมต่อกับ PostgreSQL
        conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
        c = conn.cursor()
        
        # บันทึกข้อมูลลงในฐานข้อมูล
        c.execute('''
            INSERT INTO requests (tool_name, user_name, usage_datetime, return_datetime, remarks, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (request_data['tool_name'], request_data['user_name'], request_data['usage_datetime'],
              request_data['return_datetime'], request_data['remarks'], request_data['timestamp']))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Function to load data from the database
def load_data_from_db():
    try:
        # เชื่อมต่อกับ PostgreSQL
        conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
        c = conn.cursor()
        
        # โหลดข้อมูลจากฐานข้อมูล
        c.execute('SELECT * FROM requests')
        requests = c.fetchall()
        conn.close()
        return requests
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

# Function for main app logic
def main():
    create_database()  # Create the database and table if not exists
    st.title('Hg CENIC Request System')

    # Load data from the database
    requests = load_data_from_db()

    # Display current requests
    st.subheader('Current Requests')
    if requests:
        df = pd.DataFrame(requests, columns=['ID', 'Tool Name', 'User Name', 'Usage Date', 'Return Date', 'Remarks', 'Timestamp'])
        st.dataframe(df)
    else:
        st.write("No requests found.")

    # Form for requesting tool usage
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
            save_data_to_db(request_data)  # Save data to database
            st.success('Request submitted successfully!')
            # Reload data after submitting to show the new entry
            requests = load_data_from_db()

    # Remove a request (admin only)
    st.subheader('Remove a Request (Admin Only)')
    if requests:
        request_to_remove = st.selectbox('Select Request to Remove',
                                           [f"{req[1]} by {req[2]} on {req[3]}" for req in requests])

        if st.button('Remove Request'):
            tool, user, date = request_to_remove.split(" by ")[0], request_to_remove.split(" by ")[1].split(" on ")[0], request_to_remove.split(" on ")[1]
            try:
                conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
                c = conn.cursor()
                c.execute('DELETE FROM requests WHERE tool_name=%s AND user_name=%s AND usage_datetime=%s',
                          (tool, user, date))
                conn.commit()
                conn.close()
                st.success('Request removed successfully!')
                # Reload data after removing to reflect changes
                requests = load_data_from_db()
            except Exception as e:
                st.error(f"Error removing request: {e}")

if __name__ == '__main__':
    main()

# Custom CSS for the background
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
