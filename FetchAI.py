import streamlit as st
import pandas as pd
import snowflake.connector
import os
import pickle
import time
import plotly.graph_objs as go
def FetchAI():
    # Initialisation de l'état de session si non défini
    if 'data_fetched' not in st.session_state:
        st.session_state.data_fetched = False

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
        # Mettre à jour l'état de session
        st.session_state.data_fetched = True

    # Titre et section de récupération des données restent inchangées
    st.title('Sensor Data Visualization, Export, and Air Quality Prediction')

    st.header('Sensor Data Visualization and Export')
    if st.button('Fetch and Export Data'):
        try:
            df = fetch_data()
            create_or_replace_csv(df)
            st.success('The latest 60 sensor readings have been exported to sensor_readings.csv.')
            st.write(df)
            st.session_state.data_fetched = True
        except Exception as e:
            # Ici, vous pouvez décider d'afficher un message d'erreur personnalisé
            # ou de simplement passer pour ne rien afficher.
            #st.error('An error occurred while fetching or exporting data.')
            # Ou pour ne rien afficher, commentez la ligne ci-dessus et décommentez la ligne ci-dessous
            pass
    # Pour éviter l'erreur, assurez-vous que tout le code utilisant `df` est dans ce bloc
    if st.session_state.data_fetched:
        try:
            # Assurez-vous que ce bloc est sécurisé aussi
            csv_path = "sensor_readings.csv"
            df = pd.read_csv(csv_path)
            
            st.header('Air Quality Prediction')
        # Calculate averages
            tvoc_moyenne = df['TVOC_PPB'].mean()
            eco2_moyenne = df['ECO2_PPM'].mean()
            humidity_moyenne = df['RELATIVEHUMIDITY_PERCENT'].mean()
            pressure_moyenne = df['PRESSURE_PA'].mean()
            temperature_moyenne = df['TEMPERATURE_C'].mean()

            # Load models
            model_linear = pickle.load(open('linear_regression_model.pkl', 'rb'))
            model_ridge = pickle.load(open('ridge_regression_model.pkl', 'rb'))
            model_lasso = pickle.load(open('lasso_regression_model.pkl', 'rb'))

            # User inputs for predictions
            st.write("## Enter values to predict air quality")
            tvoc = st.number_input('TVOC_PPB', value=float(tvoc_moyenne))
            eco2 = st.number_input('ECO2_PPM', value=float(eco2_moyenne))
            humidity = st.number_input('RELATIVEHUMIDITY_PERCENT', value=float(humidity_moyenne))
            pressure = st.number_input('PRESSURE_PA', value=float(pressure_moyenne))
            temperature = st.number_input('TEMPERATURE_C', value=float(temperature_moyenne))

            # Prediction
            if st.button('Predict'):
                def color_for_prediction(prediction):
                    if prediction <= 2:
                        return "green"
                    elif prediction <= 4:
                        return "yellow"
                    elif prediction <= 6:
                        return "orange"
                    elif prediction <= 8:
                        return "red"
                    else:
                        return "purple"
                input_data = pd.DataFrame([[tvoc, eco2, humidity, pressure, temperature]],
                                columns=['TVOC_PPB', 'ECO2_PPM', 'RELATIVEHUMIDITY_PERCENT', 'PRESSURE_PA', 'TEMPERATURE_C'])
                prediction_linear = model_linear.predict(input_data)[0]
                prediction_ridge = model_ridge.predict(input_data)[0]
                prediction_lasso = model_lasso.predict(input_data)[0]

                st.write("## Air Quality Predictions (AIRQUALITYINDEX):")

                # Créer le graphique à barres
                data = go.Bar(
                    x=['Linear Regression', 'Ridge Regression', 'Lasso Regression'],
                    y=[prediction_linear, prediction_ridge, prediction_lasso],
                    marker_color=[color_for_prediction(prediction_linear), color_for_prediction(prediction_ridge), color_for_prediction(prediction_lasso)] # Utilisez votre fonction color_for_prediction ici
                )

                layout = go.Layout(
                    title='Air Quality Predictions (AIRQUALITYINDEX)',
                    xaxis=dict(title='Regression Type'),
                    yaxis=dict(title='Quality Index'),
                    plot_bgcolor='rgba(0,0,0,0)'
                )

                fig = go.Figure(data=data, layout=layout)
                st.plotly_chart(fig, use_container_width=True)

            

            # Afficher les prédictions avec des couleurs associées
            st.markdown(f"<span style='color: {color_for_prediction(prediction_linear)};'>Linear Regression: {prediction_linear:.2f}</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color: {color_for_prediction(prediction_ridge)};'>Ridge Regression: {prediction_ridge:.2f}</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color: {color_for_prediction(prediction_lasso)};'>Lasso Regression: {prediction_lasso:.2f}</span>", unsafe_allow_html=True)
        except Exception as e:
            # Gérer l'exception ou la passer silencieusement
            
            pass
# N'oubliez pas de fermer le curseur et la connexion
    cur.close()
    conn.close()
