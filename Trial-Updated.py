# section 1 
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# section 2
def clean_data(df):
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert all columns to numeric
    df = df.dropna(how='all')  # Remove rows where all values are NaN
    df = df.dropna(axis=1, how='all')  # Remove columns where all values are NaN
    return df

def compare_data(df1, df2):
    st.markdown("## Data Comparison")
    st.write("First 5 Rows of First Dataset:")
    st.write(df1.head())
    st.write("First 5 Rows of Second Dataset:")
    st.write(df2.head())

def perform_task(df, task, plot_height, plot_width):
    # Your task execution code here...

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.header('Dashboard')
    
    st.sidebar.subheader('Graph parameters')
    plot_height = st.sidebar.slider('Specify plot height', 2.0, 5.0, 2.5)  # Adjusted range
    plot_width = st.sidebar.slider('Specify plot width', 2.0, 8.0, 4.0)  # Adjusted range

    st.title("Data Analysis App")
    # ... (same as before) ...

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
                st.error("One or more files have an unsupported file type.")
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
