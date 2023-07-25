# section 1 
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import base64
import io

# section 2
def clean_data(df):
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert all columns to numeric
    df = df.dropna(how='all')  # Remove rows where all values are NaN
    df = df.dropna(axis=1, how='all')  # Remove columns where all values are NaN
    return df

def harmonize_dataframes(df1, df2):
    df1 = df1.reindex(sorted(df1.columns), axis=1)
    df2 = df2.reindex(sorted(df2.columns), axis=1)
    shared_columns = set(df1.columns).intersection(df2.columns)
    return df1[shared_columns], df2[shared_columns]

def compare_data(df1, df2):
    df1, df2 = harmonize_dataframes(df1, df2)
    return df1.compare(df2)

# section 3
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

# ... (continue as before)

# section 4
def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.header('Dashboard')
    
    st.sidebar.subheader('Graph parameters')
    plot_height = st.sidebar.slider('Specify plot height', 2.0, 5.0, 2.5)  # Adjusted range
    plot_width = st.sidebar.slider('Specify plot width', 2.0, 8.0, 4.0)  # Adjusted range

# section 5
    st.title("Data Analysis App")
    st.markdown("""
    This Web App is a tool for carrying out fundamental data analysis operations on a CSV or Excel file, it is meant to speed up the process.
    You can upload your data and then choose or enter a command to carry out several actions. 
    In the case of Excel files with multiple sheets you can select the sheet you would like to analyse.
    """)

    uploaded_files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

    dfs = []
    for uploaded_file in uploaded_files:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        
        if "csv" in uploaded_file.type:
            try:
                df = pd.read_csv(uploaded_file)
                dfs.append(df)
            except UnicodeDecodeError:
                st.error("This CSV file isn't UTF-8 encoded.")
                return
        elif "excel" in uploaded_file.type:
            try:
                df = pd.read_excel(uploaded_file)
                dfs.append(df)
            except ValueError:
                st.error("This file isn't a recognized Excel file.")
                return
        else:
            st.error("This file type isn't supported.")
            return

    if len(dfs) == 2:
        df_comparison = compare_data(dfs[0], dfs[1])
        st.markdown("## Comparison Between Uploaded Files")
        st.write(df_comparison)

        if st.button('Download comparison data as CSV'):
            tmp_download_link = download_link(df_comparison, 'comparison.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

# section 6
    for df in dfs:
        df = clean_data(df)

        st.markdown("## Uploaded Data")
        st.write(df)

        tasks = ['Show First Rows', 'Show Last Rows', 'Show Columns', 'Show Dimensions', 'Show Summary',
                 'Show Missing Value Counts', 'Delete Rows With Missing Values', 'Plot Bar Graph',
                 'Plot Line Graph', 'Compare Two Columns']
        st.markdown("## Choose an Analysis Task")
        task = st.selectbox("", tasks)
        perform_task(df, task, plot_height, plot_width)

        st.markdown("## Enter a Custom Analysis Task")
        manual_task = st.text_input("")
        if manual_task:
            perform_task(df, manual_task, plot_height, plot_width)

        if st.button('Download data as CSV'):
            tmp_download_link = download_link(df, 'download.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
