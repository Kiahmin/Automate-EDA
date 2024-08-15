# Automated EDA Web App

## Overview

This project is a web application built with Streamlit that automates Exploratory Data Analysis (EDA) for CSV files. It provides an interactive interface for users to upload datasets and visualize various statistics, correlations, and distributions. The app features:

- **Dataset Overview**: Displays the dataset, its shape, and basic statistics.
- **Correlation Chart**: Visualizes correlations between continuous features.
- **Missing Values Distribution**: Shows the distribution of missing values in the dataset.
- **Individual Column Stats**: Analyzes and visualizes statistics for both continuous and categorical features.
- **Feature Relationships**: Explores relationships between features using scatter plots.

## Features

- **Interactive Data Exploration**: View data, statistics, and visualizations interactively.
- **Charts and Graphs**: Correlation heatmaps, missing values bar charts, histograms, and bar charts for categorical features.
- **Customizable Views**: Select features to analyze and visualize different aspects of the data.

## Installation

To run this application, ensure you have Python installed, and then install the required libraries listed in the requirements.txt file:

```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```
2. Run the app:
  ```bash
  streamlit run app.py
  ```
3. Upload dataset. If uploading dataset results in axios error, try running the app using:
   ```bash
   streamlit run app.py --server.enableXsrfProtection false
   ```
4. Explore the Application:
  - **Dataset Overview Tab**: View the dataset, basic statistics, correlation chart, and missing values distribution.
  - **Individual Column Stats Tab**: Analyze and visualize statistics for selected continuous or categorical features.
  - **Feature Relationships Tab**: Examine relationships between features with scatter plots, including color encoding for categorical features.

## Sample Dataset
You can use the Titanic Dataset from Kaggle as a sample dataset to explore the app's features.

## Dependencies
Streamlit
Pandas
Numpy
Bokeh==2.4.3
Matplotlib
Missingno

