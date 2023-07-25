# section 1 
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import base64
from io import BytesIO

# section 2
def clean_data(df):
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert all columns to numeric
    df = df.dropna(how='all')  # Remove rows where all values are NaN
    df = df.dropna(axis=1, how='all')  # Remove columns where all values are NaN
    return df

def compare_data(df1, df2):
    return df1.compare(df2)

def perform_task(df, task, plot_height, plot_width):
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
        missing_rows = df.loc[df.isna().any(axis=1), :]
        st.write('Deleted Rows:')
        st.write(missing_rows)
        df.dropna(inplace=True)
        st.write('Cleaned Data:')
        st.write(df)
    elif task in ['Plot Bar Graph', 'Plot Line Graph']:
        if len(df.columns) >= 2:
            default_columns = df.columns[:2].tolist()
        else:
            default_columns = df.columns.tolist()
        columns_to_select = st.multiselect("Choose two columns", df.columns, default=default_columns)
        if len(columns_to_select) != 2:
            st.warning("Please select exactly two columns.")
        else:
            if pd.api.types.is_numeric_dtype(df[columns_to_select[0]]) and pd.api.types.is_numeric_dtype(df[columns_to_select[1]]):
                kind = 'bar' if task == 'Plot Bar Graph' else 'line'
                fig, ax = plt.subplots(figsize=(plot_width, plot_height))
                df.plot(kind=kind, x=columns_to_select[0], y=columns_to_select[1], ax=ax)
                plt.xlabel(columns_to_select[0])
                plt.ylabel(columns_to_select[1])
                plt.title(f"{kind.capitalize()} Graph for {columns_to_select[0]} vs {columns_to_select[1]}")
                st.pyplot(fig)
            else:
                st.warning("Both selected columns must be numeric for plotting.")
    elif task == 'Compare Two Columns':
        columns_to_select = st.multiselect("Choose two columns for comparison", df.columns, default=df.columns[:2])
        if len(columns_to_select) != 2:
            st.warning("Please select exactly two columns for comparison.")
        else:
            fig, ax = plt.subplots(figsize=(plot_width, plot_height))
            df.plot(kind='scatter', x=columns_to_select[0], y=columns_to_select[1], ax=ax)
            plt.title(f"Comparison between {columns_to_select[0]} and {columns_to_select[1]}")
            st.pyplot(fig)
    else:
        st.error(f"Command '{task}' not recognized.")

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df, file_format):
    if file_format == 'CSV':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  
        return f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
    elif file_format == 'Excel':
        val = to_excel(df)
        b64 = base64.b64encode(val).decode()  
        return f'<a href="data:application/octet-stream;base64,{b64}" download="data.xlsx">Download Excel File</a>'

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

    uploaded_files = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files is not None and len(uploaded_files) > 0:
        dataframes = []
        for file in uploaded_files:
            file_details = {"FileName": file.name, "FileType": file.type, "FileSize": file.size}
            st.write(file_details)

            try:
                if file.type == "application/vnd.ms-excel":
                    df = pd.read_csv(file)
                elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    df = pd.read_excel(file)
                else:
                    st.error("File type not supported.")
                    continue
            except Exception as e:
                st.error(f"Error reading file: {e}")
                continue

            df = clean_data(df)
            dataframes.append(df)

            st.dataframe(df.head())
            
            tasks = ['Show First Rows', 'Show Last Rows', 'Show Columns', 'Show Dimensions', 'Show Summary', 'Show Missing Value Counts', 'Delete Rows With Missing Values', 'Plot Bar Graph', 'Plot Line Graph', 'Compare Two Columns']
            task = st.selectbox("What operation would you like to perform?", tasks)
            
            perform_task(df, task, plot_height, plot_width)
            
            file_format = st.selectbox("Choose file format for download", ['CSV', 'Excel'])
            if st.button('Download Dataframe as CSV or Excel'):
                tmp_download_link = get_table_download_link(df, file_format)
                st.markdown(tmp_download_link, unsafe_allow_html=True)

        if len(dataframes) > 1:
            df1, df2 = dataframes[0], dataframes[1]
            if st.button('Compare'):
                compare_data(df1, df2)
                
if __name__ == '__main__':
    main()
