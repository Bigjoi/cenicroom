import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Path to the image
image_path = "cenic2.jpg"

# Display the image with auto-resizing
st.image(image_path, use_column_width=True)

# Function to create the database and table
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

# Function to save data to the database
def save_data_to_db(request_data):
    with sqlite3.connect('requests.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO requests (tool_name, user_name, usage_datetime, return_datetime, remarks, timestamp) VALUES (?, ?, ?, ?, ?, ?)', 
                  (request_data['tool_name'], request_data['user_name'], request_data['usage_datetime'], request_data['return_datetime'], request_data['remarks'], request_data['timestamp']))
        conn.commit()

# Function to load data from the database
def load_data_from_db():
    with sqlite3.connect('requests.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM requests')
        return c.fetchall()

# Function for main app logic
def main():
    create_database()  # Create the database and table if not exists
    st.title('Hg CENIC Request System')

    # Load data from the database
    requests = load_data_from_db()

    # Display current requests
    st.subheader('Current Requests')
    if requests:
        df = pd.DataFrame(requests, columns=['Tool Name', 'User Name', 'Usage Date', 'Return Date', 'Remarks', 'Timestamp'])
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
                                           [f"{req[0]} by {req[1]} on {req[2]}" for req in requests])

        if st.button('Remove Request'):
            tool, user, date = request_to_remove.split(" by ")[0], request_to_remove.split(" by ")[1].split(" on ")[0], request_to_remove.split(" on ")[1]
            with sqlite3.connect('requests.db') as conn:
                c = conn.cursor()
                c.execute('DELETE FROM requests WHERE tool_name=? AND user_name=? AND usage_datetime=?', 
                          (tool, user, date))
                conn.commit()
            st.success('Request removed successfully!')
            # Reload data after removing to reflect changes
            requests = load_data_from_db()

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
