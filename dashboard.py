import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
import random
import datetime
import logging
import base64  # Import base64 library
import threading
import requests
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Olympics", page_icon=":bar_chart:", layout="wide")

# Load and display the logo with a specified width
logo_path ="background.jpeg"

# Display the logo in the first column
col1, col2 = st.columns([1, 4])  # Adjust the width ratio as needed
with col1:
    st.image(logo_path, width=200)  # Adjust the width as needed

# Display the title in the second column
with col2:
    st.title("WELCOME TO OLYMPICS ANALYSIS TOOL")

# Define functions for analysis
def show_website_visits_summary(dataframe):
    st.title("Summary of Website Visits by Country")
    summary_stats = dataframe.groupby('country').size().reset_index(name='Visits')
    st.write(summary_stats)

def show_summary_tables(dataframe):
    st.title("Summary Tables")
    st.write("### Basic Statistics:")
    st.write(dataframe.describe())
    st.write("### Data Types:")
    st.write(dataframe.dtypes)
    st.write("### Missing Values:")
    st.write(dataframe.isnull().sum())

def show_data_types_and_null_values(dataframe):
    st.title("Data Types and Null Values")
    st.write("### Data Types:")
    st.write(dataframe.dtypes)
    st.write("### Missing Values:")
    st.write(dataframe.isnull().sum())

def show_descriptive_statistics(dataframe):
    st.title("Descriptive Statistics")
    st.write(dataframe.describe())

def show_distribution_plots(dataframe):
    st.title("Distribution Plots")
    numerical_cols = dataframe.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_cols:
        fig, ax = plt.subplots()
        sns.histplot(dataframe[col], kde=True, ax=ax)
        st.write(f"### {col}")
        st.pyplot(fig)

def show_top_n_values(dataframe):
    st.title("Top N Values")
    columns = st.multiselect("Select columns", dataframe.columns)
    n = st.number_input("Select N", min_value=1, value=5)
    for col in columns:
        st.write(f"### Top {n} Values for {col}")
        st.write(dataframe[col].value_counts().head(n))

# File uploader
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))

if fl is not None:
    # Read the file if uploaded
    df = pd.read_csv(fl, encoding="ISO-8859-1")

    # Dropdown menu for analysis options
    analysis_option = st.selectbox(
        "Select an analysis option",
        ["Select an option", "View Data", "Descriptive Statistics", "Summary of Website Visits",
         "Data Types and Null Values","Distribution Plots", "Top N Values"]
    )

    if analysis_option == "View Data":
        st.write("### Uploaded File Contents:")
        st.dataframe(df)

    elif analysis_option == "Descriptive Statistics":
        show_descriptive_statistics(df)

    elif analysis_option == "Summary of Website Visits":
        show_website_visits_summary(df)

    elif analysis_option == "Data Types and Null Values":
        show_data_types_and_null_values(df)

    elif analysis_option == "Distribution Plots":
        show_distribution_plots(df)

    elif analysis_option == "Top N Values":
        show_top_n_values(df)

  # Function to fetch real web server logs from an API
def fetch_real_web_server_logs(num_logs):
    api_endpoint = "https://my.api.mockaroo.com/olympics?key=5adf4f80"
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        logs_json = response.json()
        logs = []
        for log_entry in logs_json[:num_logs]:
            logs.append([
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                log_entry.get("IP Address", ""),
                log_entry.get("Country", ""),
                log_entry.get("Referrer", ""),
                log_entry.get("Sport Category", ""),
                log_entry.get("Time Visits", ""),
                log_entry.get("Time Spent", ""),
                log_entry.get("Website Visit", ""),
                log_entry.get("Status Code", ""),
                log_entry.get("User Agent", ""),
                log_entry.get("Requested Url", "")
            ])
        return logs
    else:
        print("Failed to fetch web server logs from the API.")
        return None

# Function to generate dummy web server logs
def generate_web_server_logs(num_logs):
    logs = []
    for _ in range(num_logs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        countries = ["USA", "UK", "Canada", "Germany"]
        country = random.choice(countries)
        referrers = ["Google", "Bing", "Yahoo", "Direct"]
        referrer = random.choice(referrers)
        sport_categories = ["Football", "Basketball", "Tennis", "Swimming"]
        sport_category = random.choice(sport_categories)
        time_visits = random.randint(1, 10)
        time_spent = random.randint(10, 600)
        website_visits = random.randint(1, 100)
        status_codes = [200, 304]
        status_code = random.choice(status_codes)
        user_agents = ["Chrome", "Firefox", "Safari", "Edge"]
        user_agent = random.choice(user_agents)
        requested_urls = ["/index.html", "/images/games.jpg", "/searchsports.php", "/football.html"]
        requested_url = random.choice(requested_urls)
        log_entry = {
            "Time Stamp": timestamp,
            "IP Address": ip_address,
            "Country": country,
            "Referrer": referrer,
            "Sport Category": sport_category,
            "Time Visits": time_visits,
            "Time Spent": time_spent,
            "Website Visit": website_visits,
            "Status Code": status_code,
            "User Agent": user_agent,
            "Requested Url": requested_url
        }
        logs.append(log_entry)
    return logs

# Function to display the log generation form
def display_log_generation_form():
    st.subheader("Generate Web Server Logs")
    num_logs = st.number_input("Number of Logs to Generate", min_value=1, step=1, value=10)
    if st.button("Generate Logs"):
        logs = fetch_real_web_server_logs(num_logs)
        if logs:
            if "logs_df" not in st.session_state:
                st.session_state.logs_df = pd.DataFrame(columns=["Time Stamp", "IP Address", "Country", "Referrer", "Sport Category", "Time Visits", "Time Spent", "Website Visit", "Status Code", "User Agent", "Requested Url"])
            st.session_state.logs_df = pd.concat([st.session_state.logs_df, pd.DataFrame(logs, columns=["Time Stamp", "IP Address", "Country", "Referrer", "Sport Category", "Time Visits", "Time Spent", "Website Visit", "Status Code", "User Agent", "Requested Url"])], ignore_index=True)
            with st.expander("View Generated Logs"):
                st.dataframe(st.session_state.logs_df)  # Display logs as DataFrame
            # Add download button
            download_link = create_download_link(st.session_state.logs_df.to_csv(index=False), "web_server_logs.csv", "Download Logs")
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.error("Failed to fetch web server logs from the API.")
    elif st.session_state.get("logs_df") is not None:  # Check if logs already exist
        with st.expander("View Generated Logs"):
            st.dataframe(st.session_state.logs_df)  # Display logs as DataFrame
        # Add download button
        download_link = create_download_link(st.session_state.logs_df.to_csv(index=False), "web_server_logs.csv", "Download Logs")
        st.markdown(download_link, unsafe_allow_html=True)

# Function to create download link
def create_download_link(data, filename, text):
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Main function to display the dashboard
def main():
    display_log_generation_form()

if __name__ == "__main__":
    main()

# Function to display summary tables
def show_summary_tables(dataframe):
    # Basic statistics for numerical columns
    st.write("### <span style='color:blue'>Basic Statistics:</span>", unsafe_allow_html=True)
    st.write(dataframe.describe().T)

    # Create a box plot for each numerical column
    numerical_cols = dataframe.select_dtypes(include=['number']).columns
    for col in numerical_cols:
        fig = px.box(dataframe, y=col, title=f'Box Plot for {col}', color_discrete_sequence=['lightcoral'])
        st.plotly_chart(fig)

    # Distribution of categorical columns
    st.write("### <span style='color:blue'>Categorical Column Distribution:</span>", unsafe_allow_html=True)
    categorical_cols = dataframe.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        fig = px.histogram(dataframe, x=col, title=f'Distribution of {col}', color_discrete_sequence=['mediumpurple'])
        st.plotly_chart(fig)

    # Pairplot for numerical columns
    st.write("### <span style='color:blue'>Pair Plot of Numerical Columns:</span>", unsafe_allow_html=True)
    if len(numerical_cols) > 1:  # Ensure there's more than one numerical column
        fig = px.scatter_matrix(dataframe[numerical_cols])
        st.plotly_chart(fig)

def show_website_visits_by_hour(dataframe):
    st.title("Website Visits by Hour")
    if 'Time Stamp' in dataframe.columns:
        # Ensure 'Time Stamp' is a datetime column
        dataframe['Time Stamp'] = pd.to_datetime(dataframe['Time Stamp'])
        dataframe['Hour'] = dataframe['Time Stamp'].dt.hour
        visits_by_hour = dataframe.groupby('Hour').size().reset_index(name='Visits')
        
        fig = px.bar(visits_by_hour, x='Hour', y='Visits', title='Number of Website Visits by Hour', color='Visits', color_continuous_scale='Viridis')
        st.plotly_chart(fig)
    else:
        st.error("DataFrame does not contain a 'Time Stamp' column.")
