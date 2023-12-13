import streamlit as st
import sqlite3
from datetime import datetime

# Function to connect to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

# Function to create a table (if it doesn't exist)
def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS property_data (
                    id INTEGER PRIMARY KEY,
                    asset_id TEXT,
                    address TEXT,
                    date TEXT,
                    value REAL,
                    general_comments TEXT,
                    image BLOB
                 );'''
        conn.execute(sql)
    except Exception as e:
        print(e)

# Function to insert data into the table
def insert_data(conn, data, image_data=None):
    sql = '''INSERT INTO property_data (asset_id, address, date, value, general_comments, image)
             VALUES (?, ?, ?, ?, ?, ?);'''
    cur = conn.cursor()
    cur.execute(sql, data + (image_data,))
    conn.commit()
    return cur.lastrowid

# Function to convert image to binary format
def convert_image_to_binary(image):
    if image is not None:
        return image.getvalue()
    return None

# Streamlit app
def main():
    # Database connection
    database = "webappDB.db"
    conn = create_connection(database)
    create_table(conn)

    # Title of the app
    st.header("Student Homes", divider='violet')
    st.subheader("Property inspection data submission portal")

    # User input fields
    asset_id = st.selectbox("Asset ID", ["A1", "A2", "A3", "A4"])
    address = st.text_input("Property Address")
    date = st.date_input("Inspection Date")
    value = st.slider("Input a numerical value", min_value=0.0, max_value=100000.0, value=50000.0)
    general_comments = st.text_area("General Comments on the Property", height=150)

    # Image upload
    image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    # Data preview before submission
    st.write("## Preview of your input")
    st.write("Asset ID:", asset_id)
    st.write("Property Address:", address)
    st.write("Date:", date)
    st.write("Value:", value)
    st.write("General Comments:", general_comments)
    if image is not None:
        st.image(image, caption='Uploaded Image', use_column_width=True)

    # Submit button
    if st.button("Submit"):
        if address and date and value is not None:
            # Convert image to binary
            image_binary = convert_image_to_binary(image)

            # Insert data into the database
            data = (address, asset_id, date.strftime("%Y-%m-%d"), value, general_comments)
            insert_data(conn, data, image_binary)
            st.success("Data submitted successfully!")

    # Clear input button
    if st.button("Clear Input"):
        st.experimental_rerun()

    # Close the connection
    if conn:
        conn.close()

if __name__ == "__main__":
    main()