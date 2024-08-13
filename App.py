import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_bokeh
import missingno as msno

# Ensure pandas_bokeh is set up
pandas_bokeh.output_notebook()

# Correlation chart function
def create_corr_chart(corr_df):
    fig = plt.figure(figsize=(15,15))
    plt.imshow(corr_df.values, cmap="Blues")
    plt.xticks(range(corr_df.shape[0]), corr_df.columns, rotation=90, fontsize=15)
    plt.yticks(range(corr_df.shape[0]), corr_df.columns, fontsize=15)
    plt.colorbar()

    for i in range(corr_df.shape[0]):
        for j in range(corr_df.shape[0]):
            plt.text(j, i, "{:.2f}".format(corr_df.values[i, j]), color="red", ha="center", fontsize=14, fontweight="bold")
    
    return fig

# Missing values chart function
def create_missing_values_chart(df):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    msno.bar(df, figsize=(10,5), fontsize=12, ax=ax)
    return fig

# Function to separate continuous and categorical columns 
def find_cont_cat_cols(df):
    cont, cat = [], []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) and len(df[col].unique()) > 25:
            cont.append(col.strip())
        else:
            cat.append(col.strip())
    return cont, cat

## Web App
st.set_page_config(page_icon=":bar_chart:", page_title="Automated EDA")
st.title("Utilising Python to automate EDA")
st.caption("Upload CSV or use sample data <a href='https://www.kaggle.com/competitions/titanic/data?select=train.csv'>Titanic Dataset</a> available from Kaggle.", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        tab1, tab2, tab3 = st.tabs(["Dataset Overview", "Individual Column Stats", "Explore Relationshis between Features"])

        with tab1:
            st.subheader("1. Dataset")
            st.write(df)

            st.subheader("2. Dataset Overview")
            cont, cat = find_cont_cat_cols(df)
            num_rows = df.shape[0]
            features = df.shape[1]
            duplicates = df.shape[0] - df.drop_duplicates().shape[0]
            cat_len = len(cat)
            cont_len = len(cont)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Rows", num_rows), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Features", features), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Duplicates", duplicates), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Categorical Columns", cat_len), unsafe_allow_html=True)
            st.write(cat)

            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Continuous Columns", cont_len), unsafe_allow_html=True)
            st.write(cont)
        
            st.subheader("3. Correlation Chart")
            corr_df = df[cont].corr()
            corr_fig = create_corr_chart(corr_df)
            st.pyplot(corr_fig, use_container_width=True)

            st.subheader("4. Missing Values Distribution")
            missing_fig = create_missing_values_chart(df)
            st.pyplot(missing_fig, use_container_width=True)
        
        with tab2:
            pass

        with tab3:
            pass