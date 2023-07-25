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

def perform_task(df, task, plot_height, plot_width):
    # ... (same as before) ...

def compare_data(df1, df2):
    st.markdown("## Data Comparison")
    st.write("Uploaded Data 1:")
    st.write(df1)
    st.write("Uploaded Data 2:")
    st.write(df2)

    # You can add comparison logic here as needed
    # For example, you can compare summary statistics, visualize both datasets, etc.
    pass  # Correctly indented

def save_data(df, file_name):
    df.to_csv(file_name, index=False)
    st.success(f"Data saved as {file_name}")

def save_graph(fig, file_name):
    fig.savefig(file_name)
    st.success(f"Graph saved as {file_name}")

def main():
    # ... (same as before) ...
    
    if __name__ == "__main__":
        main()
