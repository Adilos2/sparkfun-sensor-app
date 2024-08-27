import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objs as go

def AI():
    # Charger les données à partir du fichier CSV
    df = pd.read_csv("C:\\Users\\allio\\OneDrive\\Bureau\\Sensor\\sensor_readings.csv")

    # Calcul des moyennes pour chaque métrique
    tvoc_moyenne = df['TVOC_PPB'].mean()
    eco2_moyenne = df['ECO2_PPM'].mean()
    humidity_moyenne = df['RELATIVEHUMIDITY_PERCENT'].mean()
    pressure_moyenne = df['PRESSURE_PA'].mean()
    temperature_moyenne = df['TEMPERATURE_C'].mean()

    # Charger les modèles
    model_linear = pickle.load(open('linear_regression_model.pkl', 'rb'))
    model_ridge = pickle.load(open('ridge_regression_model.pkl', 'rb'))
    model_lasso = pickle.load(open('lasso_regression_model.pkl', 'rb'))

    # Titre de l'application Streamlit
    st.title('Prédiction de la Qualité de l’Air')

    # Interface utilisateur pour les entrées de prédictions
    st.write("## Entrez les valeurs pour prédire la qualité de l'air")
    tvoc = st.number_input('TVOC_PPB', value=float(tvoc_moyenne))
    eco2 = st.number_input('ECO2_PPM', value=float(eco2_moyenne))
    humidity = st.number_input('RELATIVEHUMIDITY_PERCENT', value=float(humidity_moyenne))
    pressure = st.number_input('PRESSURE_PA', value=float(pressure_moyenne))
    temperature = st.number_input('TEMPERATURE_C', value=float(temperature_moyenne))

    # Prédiction de la qualité de l'air pour chaque modèle
    if st.button('Prédire'):
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
