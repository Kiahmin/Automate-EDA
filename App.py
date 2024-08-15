from collections import Counter
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
        if len(df[col].unique()) <= 25 or df[col].dtype == np.object_:
            cat.append(col.strip())
        else:
            cont.append(col.strip())
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
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Missing Values", df.isna().sum()), unsafe_allow_html=True)
            missing_fig = create_missing_values_chart(df)
            st.pyplot(missing_fig, use_container_width=True)
        
        with tab2:
            # Describe 
            describe_df = df.describe()
            st.subheader("Analyze Individual Feature Distributions")

            # Continous Features
            st.markdown("### 1. Understand Continuous Features")
            cont_feature = st.selectbox(label = "Select Continous Feature", options = cont, index = 0)

            cnt_na = df[cont_feature].isna().sum()
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Count", describe_df[cont_feature]['count']), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {} / ({:.2f} %)".format("Missing Values Count", cnt_na, cnt_na/df.shape[0]), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {:.2f}".format("Mean", describe_df[cont_feature]['mean']), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {:.2f}".format("Standard Deviation", describe_df[cont_feature]['std']), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Minimum", describe_df[cont_feature]['min']), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Maximum", describe_df[cont_feature]['max']), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> :".format("Quantiles"), unsafe_allow_html=True)
            st.write(describe_df[[cont_feature]].T[['25%', "50%", "75%"]])

            # Distribution of cont features
            hist = df.plot_bokeh.hist(y=cont_feature, bins=50, legend=False, vertical_xlabel=True, show_figure=False)
            st.bokeh_chart(hist, use_container_width=True)

            # Categorical Features
            st.subheader("#### 2. Understand Categorical Features")
            cat_feature = st.selectbox(label="Select Categorical Feature", options=cat, index=0)

            cnt_na = df[cont_feature].isna().sum()
            st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Count", describe_df[cont_feature]['count']), unsafe_allow_html=True)
            st.markdown("<span style='font-weight:bold;'>{}</span> : {} / ({:.2f} %)".format("Missing Values Count", cnt_na, cnt_na/df.shape[0]), unsafe_allow_html=True)

            # Distribution of cat columns
            df[cat_feature] = df[cat_feature].fillna("Missing")
            cnt_feature = Counter(df[cat_feature].values)
            df_cnt = pd.DataFrame({"Value": cnt_feature.keys(), "Count": cnt_feature.values()})
            bar_fig = df_cnt.plot_bokeh.bar(x="Value", y="Count", color="tomato", legend=False, show_figure=False)
            st.bokeh_chart(bar_fig, use_container_width=True)

        with tab3:
            st.subheader("Explore Relationships between Features")
            colA, colB = st.columns(2)
            with colA:
                x = st.selectbox(label="X_axis", options=cont, index=0)
            with colB:
                y = st.selectbox(label="Y_axis", options=cont, index=0)

            color_by = st.selectbox(label="Color by", options=[None,] + cat )

            scatter_plt = df.plot_bokeh.scatter(x=x, 
                                                y=y,
                                                category=color_by if color_by else None,
                                                title="{} vs {}".format(x.capitalize(), y.capitalize()),
                                                figsize=(600,500),
                                                show_figure=False)
            st.bokeh_chart(scatter_plt, use_container_width=True)