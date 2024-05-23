
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
import random
import datetime
import logging
import base64
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Olympics", page_icon=":bar_chart:", layout="wide")

# Load and display the logo with a specified width
logo_path = "background.jpeg"

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
         "Data Types and Null Values", "Distribution Plots", "Top N Values"]
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

    # Data types of columns
    st.write("### <span style='color:blue'>Data Types:</span>", unsafe_allow_html=True)
    data_types_df = pd.DataFrame(dataframe.dtypes, columns=['Data Type']).T
    st.write(data_types_df)

    # Create a pie chart for data types
    data_type_counts = dataframe.dtypes.value_counts().reset_index()
    data_type_counts.columns = ['Data Type', 'Count']
    data_type_counts['Data Type'] = data_type_counts['Data Type'].astype(str)  # Convert data types to string
    fig_pie = px.pie(data_type_counts, values='Count', names='Data Type', title='Distribution of Data Types')
    st.plotly_chart(fig_pie)

    # Missing values
    st.write("### <span style='color:blue'>Missing Values:</span>", unsafe_allow_html=True)
    missing_values = dataframe.isnull().sum()
    st.write(missing_values.to_frame().T)

    # Create a bar chart for missing values
    if missing_values.sum() == 0:
        st.write("No missing values in the dataset.")
    else:
        fig_bar = px.bar(missing_values[missing_values > 0], title='Missing Values per Column')
        st.plotly_chart(fig_bar)

    # Categorical variables
    categorical_cols = dataframe.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        st.write(f"### <span style='color:blue'>Unique values for {col}:</span>", unsafe_allow_html=True)
        st.write(dataframe[col].value_counts().to_frame().T)

    # Date-time analysis
    date_cols = dataframe.select_dtypes(include=['datetime64']).columns
    for col in date_cols:
        st.write(f"### <span style='color:blue'>Date-time analysis for {col}:</span>", unsafe_allow_html=True)
        st.write(pd.DataFrame({
            'Earliest Date': [dataframe[col].min()],
            'Latest Date': [dataframe[col].max()],
            'Range of Dates': [dataframe[col].max() - dataframe[col].min()]
        }).T)

# Function to display website visit insights by country with optional filtering
def show_website_visit_insights_by_country(dataframe):
    st.title("Website Visit Insights by Country")

    # Filter by country
    countries = dataframe['country'].unique().tolist()
    selected_countries = st.multiselect("Select countries to filter by", countries)

    # Apply the filter if any countries are selected
    if selected_countries:
        dataframe = dataframe[dataframe['country'].isin(selected_countries)]

    # Total number of visits by country
    total_visits_by_country = dataframe.groupby('country').size().reset_index(name='Total Visits')
    st.subheader("Total Number of Visits by Country")
    st.write(total_visits_by_country.style.background_gradient(cmap='viridis', subset=None))

    # Scatter plot for Total number of visits by country
    st.write("Scatter plot for Total Number of Visits by Country:")
    fig1 = px.scatter(total_visits_by_country, x='country', y='Total Visits', title='Total Number of Visits by Country')
    st.plotly_chart(fig1, use_container_width=True)

    # Top referring domains by country
    top_referring_domains_by_country = dataframe.groupby(['country', 'referrer']).size().reset_index(name='Visits').sort_values(by='Visits', ascending=False)
    st.subheader("Top Referring Domains by Country")
    st.write(top_referring_domains_by_country.style.background_gradient(cmap='viridis', subset=None))

    # Scatter plot for Top referring domains by country
    st.write("Scatter plot for Top Referring Domains by Country:")
    fig2 = px.scatter(top_referring_domains_by_country, x='referrer', y='Visits', color='country', title='Top Referring Domains by Country')
    st.plotly_chart(fig2, use_container_width=True)

    # Most visited pages by country
    most_visited_pages_by_country = dataframe.groupby(['country', 'Viewed_sports_categories']).size().reset_index(name='Visits').sort_values(by='Visits', ascending=False)
    st.subheader("Most Visited Pages by Country")
    st.write(most_visited_pages_by_country.style.background_gradient(cmap='viridis', subset=None))

    # Scatter plot for Most visited pages by country
    st.write("Scatter plot for Most Visited Pages by Country:")
    fig3 = px.scatter(most_visited_pages_by_country, x='Viewed_sports_categories', y='Visits', color='country', title='Most Visited Pages by Country')
    st.plotly_chart(fig3, use_container_width=True)

# Function to display distribution of website visits by hour of the day
def show_website_visits_by_hour(dataframe, visualization_type):
    # Extract the hour of the day from the timestamp
    dataframe['hour_of_day'] = pd.to_datetime(dataframe['Time_visits']).dt.hour
    visits_by_hour = dataframe.groupby('hour_of_day').size().reset_index(name='Visits')

    if visualization_type == "Line Chart":
        fig_hour = px.line(visits_by_hour, x='hour_of_day', y='Visits', title='Website Visits by Time of Day',
                           labels={'hour_of_day': 'Hour of Day', 'Visits': 'Number of Visits'})
    elif visualization_type == "Bar Chart":
        fig_hour = px.bar(visits_by_hour, x='hour_of_day', y='Visits', title='Website Visits by Time of Day',
                          labels={'hour_of_day': 'Hour of Day', 'Visits': 'Number of Visits'})
    elif visualization_type == "Area Chart":
        fig_hour = px.area(visits_by_hour, x='hour_of_day', y='Visits', title='Website Visits by Time of Day',
                           labels={'hour_of_day': 'Hour of Day', 'Visits': 'Number of Visits'})
    else:
        st.error("Invalid visualization type selected!")

    col2.subheader("4.Website Visits by Time of Day")
    col2.plotly_chart(fig_hour, use_container_width=True)

    # Display the expandable section for View Data of TimeSeries
    with col2.expander("View Data of TimeSeries"):
        st.write("Distribution of website visits by hour of the day.")
        st.dataframe(visits_by_hour.style.background_gradient(cmap="Blues"))
        csv = visits_by_hour.to_csv(index=False).encode("utf-8")
        st.download_button('Download Data', data=csv, file_name="VisitsByHour.csv", mime='text/csv')

# Sidebar filters
visualization_types = ["Line Chart", "Bar Chart", "Area Chart"]
visualization_type = st.sidebar.selectbox("4.Select Visualization Type", visualization_types)

# Call the function to display distribution of website visits by hour of the day
    # Extract the hour of the day from the timestamp
# Extract the hour of the day from the timestamp
filtered_df['hour_of_day'] = filtered_df['Time_visits'].dt.hour
visits_by_hour = filtered_df.groupby('hour_of_day').size().reset_index(name='Visits')

if visualization_type == "Line Chart":
    fig_hour = px.line(visits_by_hour, x='hour_of_day', y='Visits', title='Website Visits by Time of Day',
                       labels={'hour_of_day': 'Hour of Day', 'Visits': 'Number of Visits'})
elif visualization_type == "Bar Chart":
    fig_hour = px.bar(visits_by_hour, x='hour_of_day', y='Visits', title='Website Visits by Time of Day',
                      labels={'hour_of_day': 'Hour of Day', 'Visits': 'Number of Visits'})
elif visualization_type == "Area Chart":
    fig_hour = px.area(visits_by_hour, x='hour_of_day', y='Visits', title='Website Visits by Time of Day',
                       labels={'hour_of_day': 'Hour of Day', 'Visits': 'Number of Visits'})
else:
    st.error("Invalid visualization type selected!")

col2.subheader("4.Website Visits by Time of Day")
col2.plotly_chart(fig_hour, use_container_width=True)

# Display the expandable section for View Data of TimeSeries
with col2.expander("View Data of TimeSeries"):
    st.write("Distribution of website visits by hour of the day.")
    st.dataframe(visits_by_hour.style.background_gradient(cmap="Blues"))
    csv = visits_by_hour.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data=csv, file_name="VisitsByHour.csv", mime='text/csv')
  


# Sidebar filters
visualization_types = ["Line Chart", "Bar Chart", "Area Chart"]
visualization_type = st.sidebar.selectbox("4.Select Visualization Type", visualization_types)

# Call the function to display distribution of website visits by hour of the day
show_website_visits_by_hour(filtered_df, visualization_type)


   

# Group the data by referrer and country
referrer_country_data = df.groupby(['referrer', 'country']).size().reset_index(name='Visits')

# Create a treemap using Plotly Express
fig = px.treemap(referrer_country_data, path=['referrer', 'country'], values='Visits',
                 title='Hierarchical View of Website Visits by Referrer and Country')

# Plot the treemap
st.plotly_chart(fig, use_container_width=True)

# Provide a download button for the underlying data
csv = referrer_country_data.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name='referrer_country_data.csv', mime='text/csv',
                   help='Click here to download the data represented in the treemap')

