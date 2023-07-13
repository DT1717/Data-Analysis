import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import pytz

def perform_task(df, task):
    if task == 'Show First Rows':
        st.write(df.head())
    elif task == 'Show Last Rows':
        st.write(df.tail())
    elif task == 'Show Columns':
        st.write(df.columns.to_list())
    elif task == 'Show Dimensions':
        st.write(df.shape)
    elif task == 'Show Summary':
        st.write(df.describe())
    elif task == 'Show Missing Value Counts':
        st.write(df.isna().sum())
    elif task == 'Delete Rows With Missing Values':
        missing_rows = df[df.isna().any(axis=1)]
        st.write('Deleted Rows:')
        st.write(missing_rows)
        df.dropna(inplace=True)
        st.write('Cleaned Data:')
        st.write(df)
    elif task in ['Plot Bar Graph', 'Plot Line Graph']:
        columns_to_select = st.sidebar.multiselect("Choose two columns", df.columns, default=df.columns[:2])
        plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)
        plot_width = st.sidebar.slider('Specify plot width', 200, 500, 250)
        if len(columns_to_select) != 2:
            st.warning("Please select exactly two columns.")
        else:
            kind = 'bar' if task == 'Plot Bar Graph' else 'line'
            plt.figure(figsize=(plot_width/100, plot_height/100))  # Adjusting the size of the plot using the sliders
            df[columns_to_select].plot(kind=kind, x=columns_to_select[0], y=columns_to_select[1])
            plt.xlabel(columns_to_select[0])
            plt.ylabel(columns_to_select[1])
            plt.title(f"{kind.capitalize()} Graph for {columns_to_select[0]} vs {columns_to_select[1]}")
            st.pyplot(plt)
    elif task == 'Compare Two Columns':
        columns_to_select = st.sidebar.multiselect("Choose two columns for comparison", df.columns, default=df.columns[:2])
        if len(columns_to_select) != 2:
            st.warning("Please select exactly two columns for comparison.")
        else:
            df.plot(kind='scatter', x=columns_to_select[0], y=columns_to_select[1])
            plt.title(f"Comparison between {columns_to_select[0]} and {columns_to_select[1]}")
            st.pyplot(plt)
    else:
        st.error(f"Command '{task}' not recognized.")

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
    st.sidebar.header('Dashboard `version 2`')
    st.sidebar.markdown('Text description goes here')

    st.sidebar.subheader('Line/Bar chart parameters')
    plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])

    st.title("Data Analysis App")
    st.markdown("""
    This Web App is a tool for carrying out fundamental data analysis operations on a CSV or Excel file, it is meant to speed up the process.
    You can upload your data and then choose or enter a command to carry out several actions. 
    In the case of Excel files with multiple sheets you can select the sheet you would like to analyse.
    """)

    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            df = pd.read_excel(uploaded_file)
        
        st.markdown("## Uploaded Data")
        st.write(df)

        tasks = ['Show First Rows', 'Show Last Rows', 'Show Columns', 'Show Dimensions', 'Show Summary', 
                 'Show Missing Value Counts', 'Delete Rows With Missing Values', 'Plot Bar Graph', 
                 'Plot Line Graph', 'Compare Two Columns']
        st.markdown("## Choose an Analysis Task")
        task = st.selectbox("", tasks)
        perform_task(df, task)
        
        st.markdown("## Enter a Custom Analysis Task")
        manual_task = st.text_input("")
        if manual_task:
            perform_task(df, manual_task)

    # Display current date and time in Norway timezone
    oslo = pytz.timezone('Europe/Oslo')
    oslo_time = datetime.now(oslo)
    st.sidebar.markdown("### Date and Time")
    st.sidebar.text(f"Oslo, Norway: {oslo_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
