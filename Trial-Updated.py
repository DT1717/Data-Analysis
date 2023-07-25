# section 1 
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# section 2
def clean_data(df):
    # ... (same as before) ...

def compare_data(df1, df2):
    st.markdown("## Data Comparison")
    st.write("Uploaded Data 1:")
    st.write(df1)
    st.write("Uploaded Data 2:")
    st.write(df2)
    # You can add comparison logic here as needed
    # For example, you can compare summary statistics, visualize both datasets, etc.

def perform_task(df, task, plot_height, plot_width):
    # ... (same as before) ...

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.header('Dashboard')
    
    st.sidebar.subheader('Graph parameters')
    plot_height = st.sidebar.slider('Specify plot height', 2.0, 5.0, 2.5)  # Adjusted range
    plot_width = st.sidebar.slider('Specify plot width', 2.0, 8.0, 4.0)  # Adjusted range

# section 3
    st.title("Data Analysis App")
    st.markdown("""
    This Web App is a tool for carrying out fundamental data analysis operations on a CSV or Excel file, it is meant to speed up the process.
    You can upload your data and then choose or enter a command to carry out several actions. 
    In the case of Excel files with multiple sheets you can select the sheet you would like to analyse.
    """)

    uploaded_files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        data_frames = []
        for uploaded_file in uploaded_files:
            if "csv" in uploaded_file.type:
                try:
                    df = pd.read_csv(uploaded_file)
                except UnicodeDecodeError:
                    st.error("This CSV file isn't UTF-8 encoded.")
                    return
            elif "xlsx" in uploaded_file.type:
                try:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                except ValueError:
                    st.error("This file isn't a recognized Excel file.")
                    return
            else:
                st.error("This file type isn't supported.")
                return

            df = clean_data(df)
            data_frames.append(df)

        if len(data_frames) > 1:
            # Compare Data
            compare_data(data_frames[0], data_frames[1])

        st.markdown("## Uploaded Data")
        st.write(data_frames[0])  # Displaying the first uploaded data

        tasks = ['Show First Rows', 'Show Last Rows', 'Show Columns', 'Show Dimensions', 'Show Summary',
                 'Show Missing Value Counts', 'Delete Rows With Missing Values', 'Plot Bar Graph',
                 'Plot Line Graph', 'Compare Two Columns']
        st.markdown("## Choose an Analysis Task")
        task = st.selectbox("", tasks)
        perform_task(data_frames[0], task, plot_height, plot_width)

        st.markdown("## Enter a Custom Analysis Task")
        manual_task = st.text_input("")
        if manual_task:
            perform_task(data_frames[0], manual_task, plot_height, plot_width)

if __name__ == "__main__":
    main()
