import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
import time
def graph():
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
        # Query to retrieve all entries from SENSORREADINGS table
        query = """
        SELECT * FROM SENSOR_DATA.PUBLIC.READINGS
        ORDER BY TIMESTAMP DESC
          -- Assuming you want the latest 100 entries for the graph
        """
        df = pd.read_sql(query, conn)
        return df

    # Initialize Streamlit app
    st.title('Real-Time Sensor Data Dashboard')

    # Create a placeholder for each graph
    tvoc_placeholder = st.empty()
    eco2_placeholder = st.empty()
    humidity_placeholder = st.empty()
    pressure_placeholder = st.empty()
    temperature_placeholder = st.empty()
    altitude_placeholder = st.empty()  # New placeholder for altitude


    # Main loop to update data every second
    # Main loop to update data every second
    while True:
        with create_snowflake_connection() as conn:
            # Get the latest data
            df = get_latest_data(conn)

        # Example customization
        line_color = "#17BECF"  # Turquoise, feel free to change it to your preferred color
        line_width = 2
        marker_size = 3.5
        title_font_size = 24
        axis_font_size = 18

        # Update the graphs with more colorful and user-friendly styles
        tvoc_fig = px.line(df, x='TIMESTAMP', y='TVOC_PPB', title='TVOC Over Time',
                        markers=True, line_shape='linear')
        tvoc_fig.update_traces(line=dict(color=line_color, width=line_width),
                            marker=dict(size=marker_size))
        tvoc_fig.update_layout(title_font=dict(size=title_font_size),
                            xaxis_title_font=dict(size=axis_font_size),
                            yaxis_title_font=dict(size=axis_font_size),
                                plot_bgcolor='rgba(0,0,0,0)')  # Transparent background


        eco2_fig = px.line(df, x='TIMESTAMP', y='ECO2_PPM', title='eCO2 Over Time',
                        markers=True, line_shape='linear')
        eco2_fig.update_traces(line=dict(color="magenta", width=line_width),
                            marker=dict(size=marker_size))
        eco2_fig.update_layout(title_font=dict(size=title_font_size),
                            xaxis_title_font=dict(size=axis_font_size),
                            yaxis_title_font=dict(size=axis_font_size),
                                plot_bgcolor='rgba(0,0,0,0)')  # Transparent background

        
        humidity_fig = px.line(df, x='TIMESTAMP', y='RELATIVEHUMIDITY_PERCENT', title='Relative Humidity Over Time',
                            markers=True, line_shape='linear')
        humidity_fig.update_traces(line=dict(color="orange", width=line_width),
                                marker=dict(size=marker_size))
        humidity_fig.update_layout(title_font=dict(size=title_font_size),
                                xaxis_title_font=dict(size=axis_font_size),
                                yaxis_title_font=dict(size=axis_font_size),
                                plot_bgcolor='rgba(0,0,0,0)')  # Transparent background
        
        pressure_fig = px.line(df, x='TIMESTAMP', y='PRESSURE_PA', title='Pressure Over Time',
                            markers=True, line_shape='linear')
        pressure_fig.update_traces(line=dict(color="green", width=line_width),
                                marker=dict(size=marker_size))
        pressure_fig.update_layout(title_font=dict(size=title_font_size),
                                xaxis_title_font=dict(size=axis_font_size),
                                yaxis_title_font=dict(size=axis_font_size),
                                plot_bgcolor='rgba(0,0,0,0)')  # Transparent background
        

        temperature_fig = px.line(df, x='TIMESTAMP', y='TEMPERATURE_C', title='Temperature Over Time',
                                markers=True, line_shape='linear')
        temperature_fig.update_traces(line=dict(color="red", width=line_width),
                                    marker=dict(size=marker_size))
        temperature_fig.update_layout(title_font=dict(size=title_font_size),
                                    xaxis_title_font=dict(size=axis_font_size),
                                    yaxis_title_font=dict(size=axis_font_size),
                                    plot_bgcolor='rgba(0,0,0,0)')  # Transparent background

    # Create and update the graph for Altitude
        altitude_fig = px.line(df, x='TIMESTAMP', y='ALTITUDE_METERS', title='Altitude Over Time',
                            markers=True, line_shape='linear')
        altitude_fig.update_traces(line=dict(color="purple", width=line_width),
                                marker=dict(size=marker_size))
        altitude_fig.update_layout(title_font=dict(size=title_font_size),
                                xaxis_title_font=dict(size=axis_font_size),
                                yaxis_title_font=dict(size=axis_font_size),
                                plot_bgcolor='rgba(0,0,0,0)')
        
        # Update the placeholders with the new graphs
        tvoc_placeholder.plotly_chart(tvoc_fig, use_container_width=True)
        eco2_placeholder.plotly_chart(eco2_fig, use_container_width=True)
        humidity_placeholder.plotly_chart(humidity_fig, use_container_width=True)
        pressure_placeholder.plotly_chart(pressure_fig, use_container_width=True)
        temperature_placeholder.plotly_chart(temperature_fig, use_container_width=True)
        altitude_placeholder.plotly_chart(altitude_fig, use_container_width=True)  

        
        # Sleep for 1 second before fetching the data again
        time.sleep(1)
