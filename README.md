# sensor-app

Environmental Data Platform
============================

Notre projet est conçu pour apporter une nouvelle perspective sur la façon dont nous percevons et interagissons avec les données environnementales. En mettant l'accent sur la qualité de l'air et les conditions environnementales, notre plateforme aspire à devenir un outil incontournable pour les individus et les communautés soucieux de leur environnement.

Objectif Principal
------------------
Notre mission principale est de fournir une plateforme intuitive et interactive permettant à chacun de visualiser, analyser et comprendre les données environnementales en temps réel. En démocratisant l'accès à ces informations, nous espérons sensibiliser le public à l'importance de la surveillance environnementale pour promouvoir des actions en faveur d'un avenir durable.

Fonctionnalités Clés
--------------------
- Visualisation des Données : Profitez de graphiques dynamiques et en temps réel pour obtenir une vue d'ensemble claire et immédiate de l'état de l'environnement autour de vous.
- Analyse de la Qualité de l'Air : Utilisez notre suite d'outils analytiques avancés pour évaluer la qualité de l'air dans votre région, basée sur des mesures précises et des algorithmes de pointe.
- Interaction et Engagement Utilisateur : Notre interface utilisateur est conçue pour être à la fois intuitive et engageante, encourageant la participation active et l'apprentissage autour des enjeux environnementaux.

Technologies Utilisées
----------------------
Voici les principales bibliothèques Python utilisées pour ce projet :

- openai==0.28.1 : Pour l'intégration d'un chatbot intelligent.
- pandas==1.5.3 : Pour la manipulation et l'analyse de fichiers CSV.
- plotly==5.9.0 : Pour la création de graphiques interactifs et dynamiques.
- pyserial==3.5 : Pour la communication série avec des capteurs et dispositifs.
- snowflake-connector-python==3.2.0 : Pour se connecter et interagir avec la base de données Snowflake.
- streamlit==1.23.1 : Pour créer l'interface frontend et déployer l'application.
- scikit-learn==0.24.2 : Pour l'entraînement et l'évaluation des modèles de machine learning.

Matériel Utilisé
----------------
Le projet est conçu pour fonctionner normalement avec une **Raspberry Pi**, qui permet de connecter les capteurs directement à travers ses ports GPIO. Toutefois, il est également possible d'utiliser les capteurs directement avec un ordinateur en les branchant via un port USB.

Pourquoi Notre Projet?
----------------------
Face à l'urgence climatique et environnementale, il est primordial de prendre des mesures conscientes et informées pour protéger notre planète. En fournissant un accès facile à des données environnementales cruciales et en facilitant leur compréhension, nous espérons inspirer des actions positives pour un avenir plus propre et plus vert.

Lancement du Projet
-------------------
Pour exécuter ce projet localement, suivez ces étapes :

1. Installez les dépendances :
   pip install -r requirements.txt
   
3. Lancez le fichier du capteur :
   python Sensor.py
   
3. Lancez l'application avec Streamlit :
   streamlit run acceuil.py

Rejoignez-nous dans cette mission et explorons ensemble les moyens d'améliorer notre environnement, un byte à la fois. Votre participation est essentielle pour faire la différence. Ensemble, contribuons à un monde meilleur!
