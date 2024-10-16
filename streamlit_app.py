import streamlit as st
import pandas as pd
import json
import os

# ฟังก์ชันสำหรับอ่านข้อมูลจากไฟล์ JSON
def load_data():
    if os.path.exists('inventory.json'):
        with open('inventory.json', 'r') as f:
            return json.load(f)
    return []

# ฟังก์ชันสำหรับบันทึกข้อมูลลงไฟล์ JSON
def save_data(data):
    with open('inventory.json', 'w') as f:
        json.dump(data, f)

# ฟังก์ชันหลัก
def main():
    st.title('Inventory Management System')

    inventory = load_data()
    
    # แสดงข้อมูลสินค้า
    st.subheader('Current Inventory')
    df = pd.DataFrame(inventory)
    st.dataframe(df)

    # เพิ่มสินค้า
    st.subheader('Add New Item')
    new_item_name = st.text_input('Item Name')
    new_item_quantity = st.number_input('Quantity', min_value=0)

    if st.button('Add Item'):
        if new_item_name and new_item_quantity >= 0:
            inventory.append({'name': new_item_name, 'quantity': new_item_quantity})
            save_data(inventory)
            st.success('Item added successfully!')

    # ลบสินค้า
    st.subheader('Remove Item')
    item_to_remove = st.selectbox('Select Item to Remove', [item['name'] for item in inventory])

    if st.button('Remove Item'):
        inventory = [item for item in inventory if item['name'] != item_to_remove]
        save_data(inventory)
        st.success('Item removed successfully!')

if __name__ == '__main__':
    main()
