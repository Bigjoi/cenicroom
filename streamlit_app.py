import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Path to the CSV file
csv_path = 'requests.csv'

# Function to create CSV file if it doesn't exist
def create_csv():
    if not os.path.exists(csv_path):
        # Create the CSV file with header if it doesn't exist
        df = pd.DataFrame(columns=['Tool Name', 'User Name', 'Usage Date', 'Return Date', 'Remarks', 'Timestamp'])
        df.to_csv(csv_path, index=False)

# Function to save data to the CSV file
def save_data_to_csv(request_data):
    df = pd.read_csv(csv_path)
    df = df.append(request_data, ignore_index=True)
    df.to_csv(csv_path, index=False)

# Function to load data from the CSV file
def load_data_from_csv():
    return pd.read_csv(csv_path)

# Function for main app logic
def main():
    create_csv()  # Create the CSV file if not exists
    st.title('Hg CENIC Request System')

    # Load data from the CSV file
    requests = load_data_from_csv()

    # Display current requests
    st.subheader('Current Requests')
    if not requests.empty:
        st.dataframe(requests)
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
                'Tool Name': tool_name,
                'User Name': user_name,
                'Usage Date': str(usage_date),
                'Return Date': str(return_date),
                'Remarks': remarks,
                'Timestamp': timestamp
            }
            save_data_to_csv(request_data)  # Save data to CSV
            st.success('Request submitted successfully!')
            # Reload data after submitting to show the new entry
            requests = load_data_from_csv()

    # Editing requests (Admin Only)
    st.subheader('Edit a Request (Admin Only)')
    if not requests.empty:
        request_to_edit = st.selectbox('Select Request to Edit', 
                                       [f"{row['Tool Name']} by {row['User Name']} on {row['Usage Date']}" for index, row in requests.iterrows()])

        if request_to_edit:
            # Extract selected request details
            tool, user, date = request_to_edit.split(' by ')[0], request_to_edit.split(' by ')[1].split(' on ')[0], request_to_edit.split(' on ')[1]
            selected_row = requests[(requests['Tool Name'] == tool) & (requests['User Name'] == user) & (requests['Usage Date'] == date)]

            # Display fields with current data
            new_tool_name = st.text_input('Tool Name', selected_row['Tool Name'].values[0])
            new_user_name = st.text_input('User Name', selected_row['User Name'].values[0])
            new_usage_date = st.date_input('Date of Usage', pd.to_datetime(selected_row['Usage Date'].values[0]))
            new_return_date = st.date_input('Return Date', pd.to_datetime(selected_row['Return Date'].values[0]))
            new_remarks = st.text_area('Remarks', selected_row['Remarks'].values[0])

            if st.button('Save Changes'):
                # Update the selected row with new data
                requests.loc[(requests['Tool Name'] == tool) & (requests['User Name'] == user) & (requests['Usage Date'] == date), 'Tool Name'] = new_tool_name
                requests.loc[(requests['Tool Name'] == tool) & (requests['User Name'] == user) & (requests['Usage Date'] == date), 'User Name'] = new_user_name
                requests.loc[(requests['Tool Name'] == tool) & (requests['User Name'] == user) & (requests['Usage Date'] == date), 'Usage Date'] = str(new_usage_date)
                requests.loc[(requests['Tool Name'] == tool) & (requests['User Name'] == user) & (requests['Usage Date'] == date), 'Return Date'] = str(new_return_date)
                requests.loc[(requests['Tool Name'] == tool) & (requests['User Name'] == user) & (requests['Usage Date'] == date), 'Remarks'] = new_remarks
                requests.to_csv(csv_path, index=False)  # Save changes to CSV
                st.success('Request updated successfully!')
                # Reload data after editing to reflect changes
                requests = load_data_from_csv()

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
