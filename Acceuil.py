import streamlit as st
from DataFetch import Fetch
from AI import AI
from Show import show
from showgraph import graph
from chatSensor import chatSensorPage
def page_description():
    
    st.title("🌍🚀 Description du Projet 🚀🌍")
    st.markdown("""
### Bienvenue sur la page de description de notre projet ! 🎉🎈

Notre projet est conçu pour **apporter une nouvelle perspective** sur la façon dont nous percevons et interagissons avec les données environnementales. 💡🌱 En mettant l'accent sur la **qualité de l'air** et les **conditions environnementales**, notre plateforme aspire à devenir un outil incontournable pour les individus et les communautés soucieux de leur environnement. 🌏💚

#### 🎯 Objectif Principal
Notre mission principale est de fournir une **plateforme intuitive et interactive** permettant à chacun de visualiser, analyser et comprendre les données environnementales en temps réel. 🕒📊 En démocratisant l'accès à ces informations, nous espérons sensibiliser le public à l'importance de la surveillance environnementale pour promouvoir des actions en faveur d'un avenir durable. 🌟🛡️

#### 🛠️ Fonctionnalités Clés
- **Visualisation des Données** : Profitez de graphiques dynamiques et en temps réel pour obtenir une vue d'ensemble claire et immédiate de l'état de l'environnement autour de vous. 📊📈
- **Analyse de la Qualité de l'Air** : Utilisez notre suite d'outils analytiques avancés pour évaluer la qualité de l'air dans votre région, basée sur des mesures précises et des algorithmes de pointe. 🌬️💨
- **Interaction et Engagement Utilisateur** : Notre interface utilisateur est conçue pour être à la fois intuitive et engageante, encouragent la participation active et l'apprentissage autour des enjeux environnementaux. 🌐👥

#### 🌍 Pourquoi Notre Projet?
Face à l'urgence climatique et environnementale, il est primordial de prendre des mesures conscientes et informées pour protéger notre planète. En fournissant un accès facile à des données environnementales cruciales et en facilitant leur compréhension, nous espérons inspirer des actions positives pour un avenir plus propre et plus vert. 🌿♻️

Rejoignez-nous dans cette mission et explorons ensemble les moyens d'améliorer notre environnement, **un byte à la fois**. Votre participation est essentielle pour faire la différence. Ensemble, contribuons à un monde meilleur! 🚀🌎
""", unsafe_allow_html=True)





st.sidebar.title('Navigation')
page = st.sidebar.radio("Aller à", ('Accueil', 'Show', 'Graph','Fetch','Prediction','Chat'))

if page == 'Accueil':
    page_description()
elif page == 'Show':
    show()
elif page == 'Graph':
    graph()
elif page == 'Fetch':
    Fetch()
elif page == 'Prediction':
    AI()
elif page == 'Chat':
    chatSensorPage()
