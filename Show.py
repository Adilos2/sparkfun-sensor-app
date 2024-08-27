import streamlit as st
import pandas as pd
import snowflake.connector
import time
def show():
    # Snowflake connection information
    USER = 'ADILALL'
    PASSWORD = 'Omar0661402741'
    ACCOUNT = 'lj15515.ca-central-1.aws'  
    WAREHOUSE = 'ADLS_SENSOR_SPARKFUN'  
    DATABASE = 'SENSOR_DATA'         
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
        # Query to retrieve all entries from SENSORREADINGS table
        query = """
        SELECT * FROM SENSOR_DATA.PUBLIC.READINGS
        ORDER BY TIMESTAMP DESC
        """
        df = pd.read_sql(query, conn)
        return df

    # Initialize Streamlit app
    st.title('Real-Time Sensor Data Dashboard')

    # Placeholder for displaying data
    data_placeholder = st.empty()

    # Main loop to update data every second
    while True:
        with create_snowflake_connection() as conn:
            # Get the latest data
            df = get_latest_data(conn)
        
        # Update the placeholder with the new data
        data_placeholder.write(df)
        
        # Sleep for 1 second before fetching the data again
        time.sleep(1)
