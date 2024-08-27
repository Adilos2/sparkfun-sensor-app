import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
import time

# Snowflake connection information
    USER = ''
    PASSWORD = ''
    ACCOUNT = ''  
    WAREHOUSE = ''  
    DATABASE = ''         
    SCHEMA = 'public'

# Function to create Snowflake connection
def create_snowflake_connection():
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
    )
    return conn

# Function to get the latest sensor readings
def get_latest_data(conn):
    query = """
    SELECT * FROM SENSOR_DATA.PUBLIC.READINGS
    ORDER BY TIMESTAMP DESC
    LIMIT 200  -- Assuming you want the latest 200 entries for the graph
    """
    df = pd.read_sql(query, conn)
    return df

# Initialize Streamlit app
st.title('Real-Time Sensor Data Dashboard')

# Placeholder for displaying raw data
data_placeholder = st.empty()

# Create placeholders for each graph
tvoc_placeholder = st.empty()
eco2_placeholder = st.empty()
humidity_placeholder = st.empty()
pressure_placeholder = st.empty()
temperature_placeholder = st.empty()
altitude_placeholder = st.empty()

# Main loop to update data every second
while True:
    with create_snowflake_connection() as conn:
        df = get_latest_data(conn)

    # Update the placeholder with the new raw data
    data_placeholder.write(df.head())  # Show only the top rows
    
    # Set some default Plotly parameters for styling
    line_width = 2.5
    marker_size = 7
    title_font_size = 24
    axis_font_size = 18
    
    # Generate and style Plotly graphs for each sensor metric
    # Create graphs for TVOC, eCO2, Humidity, Pressure, Temperature, and Altitude
    metrics = {
        'TVOC_PPB': 'TVOC Over Time',
        'ECO2_PPM': 'eCO2 Over Time',
        'RELATIVEHUMIDITY_PERCENT': 'Relative Humidity Over Time',
        'PRESSURE_PA': 'Pressure Over Time',
        'TEMPERATURE_C': 'Temperature Over Time',
        'ALTITUDE_METERS': 'Altitude Over Time'
    }
    placeholders = [tvoc_placeholder, eco2_placeholder, humidity_placeholder, pressure_placeholder, temperature_placeholder, altitude_placeholder]
    colors = ["#17BECF", "magenta", "orange", "green", "red", "purple"]
    
    for metric, placeholder, color in zip(metrics.keys(), placeholders, colors):
        fig = px.line(df, x='TIMESTAMP', y=metric, title=metrics[metric], markers=True, line_shape='linear')
        fig.update_traces(line=dict(color=color, width=line_width), marker=dict(size=marker_size))
        fig.update_layout(title_font=dict(size=title_font_size), xaxis_title_font=dict(size=axis_font_size), yaxis_title_font=dict(size=axis_font_size), plot_bgcolor='rgba(0,0,0,0)')
        placeholder.plotly_chart(fig, use_container_width=True)
    
    # Sleep for 1 second before fetching the data again
    time.sleep(1)
