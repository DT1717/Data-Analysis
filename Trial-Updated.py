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

def compare_data(df1, df2):
    return df1.compare(df2)

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def perform_task(df, task, plot_height, plot_width):
    # ... (similar to your original code, add button for saving data at the end) ...
    if st.button("Download Data as CSV"):
        st.markdown(download_link(df, "processed_data.csv", "Download Processed Data"), unsafe_allow_html=True)

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.header('Dashboard')
    
    st.sidebar.subheader('Graph parameters')
    plot_height = st.sidebar.slider('Specify plot height', 2.0, 5.0, 2.5)  
    plot_width = st.sidebar.slider('Specify plot width', 2.0, 8.0, 4.0)  

    st.title("Data Analysis App")
    st.markdown("""
    This Web App is a tool for carrying out fundamental data analysis operations on a CSV or Excel file, it is meant to speed up the process.
    You can upload your data and then choose or enter a command to carry out several actions. 
    In the case of Excel files with multiple sheets you can select the sheet you would like to analyse.
    """)

    uploaded_files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

    dataframes = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            st.write(file_details)
        
            if "csv" in uploaded_file.type:
                try:
                    df = pd.read_csv(uploaded_file)
                except UnicodeDecodeError:
                    st.error("This CSV file isn't UTF-8 encoded.")
                    return
            elif "excel" in uploaded_file.type:
                try:
                    df = pd.read_excel(uploaded_file)
                except ValueError:
                    st.error("This file isn't a recognized Excel file.")
                    return
            else:
                st.error("This file type isn't supported.")
                return
            dataframes.append(df)

        if len(dataframes) > 1:
            df1, df2 = dataframes[0], dataframes[1]
            st.write(compare_data(df1, df2))

        for df in dataframes:
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

        if st.button("Download Figure"):
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode()
            href = f'<a href="data:image/png;base64,{b64}" download="myimage.png">Download the Plot as Image</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
