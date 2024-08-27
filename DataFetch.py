import snowflake.connector
import pandas as pd
import os
import streamlit as st
def Fetch():
    # Snowflake connection information
    USER = ''
    PASSWORD = ''
    ACCOUNT = ''  
    WAREHOUSE = ''  
    DATABASE = ''         
    SCHEMA = 'public'

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
    )

    # Cursor to execute SQL query
    cur = conn.cursor()

    # Function to fetch the last 60 records
    def fetch_data():
        query = """
        SELECT
            AIRQUALITYINDEX,
            TVOC_PPB,
            ECO2_PPM,
            RELATIVEHUMIDITY_PERCENT,
            PRESSURE_PA,
            TEMPERATURE_C      
        FROM READINGS
        ORDER BY TIMESTAMP DESC
        LIMIT 60
        """
        cur.execute(query)
        df = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
        return df

    # Function to create or replace the CSV file
    def create_or_replace_csv(df):
        csv_file = 'sensor_readings.csv'
        if os.path.exists(csv_file):
            os.remove(csv_file)
        df.to_csv(csv_file, index=False)

    # Streamlit interface
    st.title('Sensor Data Visualization and Export')

    if st.button('Run Test'):
        df = fetch_data()
        create_or_replace_csv(df)
        st.success('The latest 60 sensor readings have been exported to sensor_readings.csv.')
        st.write(df)

    # Close the cursor and connection
    cur.close()
    conn.close()
