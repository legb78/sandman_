# Dream Synthesizer 💭🎨

## Overview

Dream Synthesizer est une application Streamlit qui transforme vos récits de rêves parlés en images visuelles. L'application utilise l'IA pour transcrire l'audio, analyser le contenu des rêves et générer des images représentatives.

## Fonctionnalités

- **Entrée audio**: Téléchargez des fichiers audio ou enregistrez directement dans l'application
- **Transcription**: Convertissez les récits parlés en texte à l'aide de l'API Groq
- **Analyse de rêve**: Extrayez les éléments visuels et le contenu émotionnel à l'aide de Mistral AI
- **Génération d'images**: Créez des représentations visuelles de rêves à l'aide de l'API Clipboard
- **Plusieurs styles artistiques**: Choisissez parmi différents styles visuels pour vos images de rêve
- **Téléchargement d'images**: Enregistrez les images de rêve générées sur votre appareil

## Prérequis

- Python 3.8+
- Streamlit
- Clés API requises:
  - API Groq pour la transcription audio
  - Mistral AI pour l'analyse de texte
  - API Clipboard pour la génération d'images

## Installation

1. Clonez le dépôt:
   ```
   git clone <url-du-dépôt>
   cd dream-synthesizer
   ```

2. Installez les packages requis:
   ```
   pip install -r requirements.txt
   ```

3. Créez un fichier `.env` à la racine du projet avec vos clés API:
   ```
   GROQ_API_KEY=votre_clé_api_groq
   MISTRAL_API_KEY=votre_clé_api_mistral
   CLIPBOARD_API_KEY=votre_clé_api_clipboard
   ```

## Utilisation

1. Démarrez l'application:
   ```
   streamlit run src/app.py
   ```

2. Utilisez l'interface web pour:
   - Télécharger un fichier audio ou enregistrer votre récit de rêve
   - Transcrire l'audio en texte
   - Analyser le contenu du rêve
   - Générer une image représentant votre rêve
   - Télécharger l'image générée

## Structure du projet

```
.
├── .env                  # Variables d'environnement (clés API)
├── requirements.txt      # Dépendances du projet
└── src/
    ├── app.py            # Application Streamlit principale
    ├── audio_processor.py# Fonctions de traitement audio
    ├── image_generator.py# Fonctions de génération d'images
    ├── text_processor.py # Fonctions d'analyse de texte
    └── utils/
        └── helpers.py    # Fonctions utilitaires
```

## Technologies utilisées

- **Streamlit**: Framework d'application web
- **Groq**: Modèle IA pour la transcription audio
- **Mistral AI**: Analyse et compréhension du texte
- **API Clipboard**: Génération d'images à partir de descriptions textuelles
- **Python-dotenv**: Gestion des variables d'environnement
- **Pydub**: Traitement audio
- **Pillow**: Manipulation d'images

## Utilisation des API

L'application utilise trois API différentes:

1. **API Groq**: Transcrit les enregistrements audio des rêves en texte
2. **API Mistral AI**: Analyse le texte du rêve pour extraire les éléments visuels et le contenu émotionnel
3. **API Clipboard**: Génère des images basées sur le contenu du rêve analysé

## Déploiement sur Streamlit Cloud

1. Créez un compte sur [Streamlit Cloud](https://streamlit.io/cloud)
2. Connectez votre dépôt GitHub
3. Configurez les secrets avec vos clés API
4. Déployez l'application

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à soumettre une Pull Request.

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
