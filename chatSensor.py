import streamlit as st
import pandas as pd
import openai

import streamlit as st
import pandas as pd
import openai

def chatSensorPage():
    # Configurez votre clé API OpenAI ici
    openai.api_key = 'sk-complete your key here'

    def calculer_moyennes(csv_path):
        df = pd.read_csv(csv_path)
        tvoc_moyenne = df['TVOC_PPB'].mean()
        eco2_moyenne = df['ECO2_PPM'].mean()
        humidity_moyenne = df['RELATIVEHUMIDITY_PERCENT'].mean()
        pressure_moyenne = df['PRESSURE_PA'].mean()
        temperature_moyenne = df['TEMPERATURE_C'].mean()
        return tvoc_moyenne, eco2_moyenne, humidity_moyenne, pressure_moyenne, temperature_moyenne

    def generer_texte_explicatif(tvoc_moyenne, eco2_moyenne, humidity_moyenne, pressure_moyenne, temperature_moyenne):
        prompt = f"""
        TVOC (Total Volatile Organic Compounds) en PPB : {tvoc_moyenne},
        eCO2 (Equivalent CO2) en PPM : {eco2_moyenne},
        Humidité Relative en Pourcentage : {humidity_moyenne},
        Pression en PA : {pressure_moyenne},
        Température en °C : {temperature_moyenne}.
        Expliquez en quoi chaque métrique inflence la qualite de l air et prpose un indice de qualité de l'air (entre 1 et 5) basé sur ces valeurs.
        (Un indice de qualité de l'air de 1 indiquerait une excellente qualité de l'air, Un indice de qualité de l'air de 5 indiquerait une très mauvaise qualité de l'air)."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant intelligent qui fournit la qualité de l'air intérieur basées sur des données spécifiques."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        if response['choices']:
            return response['choices'][0]['message']['content']
        else:
            return "Désolé, je ne peux pas générer de réponse en ce moment."

    st.title('Prédiction et explication de la Qualité de l’Air avec GPT-3')
    
    csv_path = "C:\\Users\\allio\\OneDrive\\Bureau\\Sensor\\sensor_readings.csv"
    
    tvoc_moyenne, eco2_moyenne, humidity_moyenne, pressure_moyenne, temperature_moyenne = calculer_moyennes(csv_path)

    tvoc = st.number_input('TVOC (PPB)', value=float(tvoc_moyenne))
    eco2 = st.number_input('eCO2 (PPM)', value=float(eco2_moyenne))
    humidity = st.number_input('Humidité Relative (%)', value=float(humidity_moyenne))
    pressure = st.number_input('Pression (PA)', value=float(pressure_moyenne))
    temperature = st.number_input('Température (°C)', value=float(temperature_moyenne))

    if st.button('Explication'):
        texte_explicatif = generer_texte_explicatif(tvoc, eco2, humidity, pressure, temperature)
        st.markdown(f"### Explication sur la Qualité de l'Air\n{texte_explicatif}", unsafe_allow_html=True)


