import streamlit as st
import os
import sys
from io import BytesIO
from dotenv import load_dotenv

# Importer l'enregistreur audio
try:
    from audiorecorder import audiorecorder
    audio_recorder_available = True
except ImportError:
    audio_recorder_available = False

# Ajouter le chemin actuel au path Python pour assurer l'importation du module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importer les fonctions des modules
try:
    from audio_processor import preprocess_audio, transcribe_audio
    from text_processor import extract_visual_elements, analyze_dream_sentiment, create_image_prompt
    from image_generator import generate_image_with_clipboard, get_available_styles, preview_styled_prompt
    import_success = True
except ImportError as e:
    import_success = False
    import_error = str(e)

# Charger les variables d'environnement
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Dream Synthesizer",
    page_icon="�",
    layout="centered"
)

# Interface principale
st.title("� Synthétiseur de Rêves")
st.subheader("Transformez vos rêves parlés en images")

# Vérifier que l'importation des modules a réussi
if not import_success:
    st.error(f"Erreur lors de l'importation des modules: {import_error}")
    st.stop()

# Section d'upload de fichier audio
st.markdown("### 1. Racontez votre rêve")

# Onglets pour choisir le mode d'entrée audio
tab1, tab2 = st.tabs(["📁 Uploader un fichier", "🎤 Enregistrer directement"])

audio_data = None

with tab1:
    # Upload de fichier existant
    audio_input = st.file_uploader("Choisir un fichier MP3 ou WAV", type=["mp3", "wav", "m4a", "ogg"])
    if audio_input is not None:
        st.audio(audio_input)
        audio_data = audio_input

with tab2:
    # Enregistrement audio direct
    st.markdown("**🎤 Enregistrement audio direct**")
    st.info("💡 Cliquez sur 'Enregistrer' puis parlez. Cliquez sur 'Arrêter' quand vous avez terminé.")
    
    if audio_recorder_available:
        # Enregistreur audio fonctionnel avec streamlit-audiorecorder
        st.info("🎤 Cliquez sur le premier bouton pour commencer l'enregistrement, puis sur le second pour l'arrêter.")
        
        audio_bytes = audiorecorder(
            "Cliquer pour enregistrer",
            "Cliquer pour arrêter l'enregistrement"
        )
        
        if len(audio_bytes) > 0:
            st.audio(audio_bytes.export().read(), format="audio/wav")
            # Convertir en objet similaire au file_uploader
            audio_data = BytesIO(audio_bytes.export().read())
            audio_data.name = "recorded_audio.wav"
    else:
        # Fallback si la librairie n'est pas installée
        st.warning("⚠️ L'enregistrement direct nécessite l'installation de `streamlit-audiorecorder`. Utilisez l'onglet 'Uploader un fichier' pour le moment.")
        st.code("pip install streamlit-audiorecorder")

if audio_data is not None:
    # Afficher un lecteur audio pour le fichier téléchargé
    st.audio(audio_data)
    
    # Bouton pour traiter l'audio
    if st.button("Transcrire l'audio"):
        with st.spinner("Traitement de l'audio en cours..."):
            try:
                # Prétraiter l'audio
                audio_path = preprocess_audio(audio_data)
                
                # Transcrire l'audio
                transcript = transcribe_audio(audio_path)
                
                # Afficher la transcription
                st.markdown("### 2. Transcription de votre rêve")
                st.text_area("Texte transcrit", transcript, height=150, key="transcription_display")
                
                # Sauvegarder dans la session
                st.session_state.dream_transcript = transcript
                
            except Exception as e:
                st.error(f"Une erreur s'est produite: {str(e)}")

# Si une transcription existe dans la session, afficher la section d'analyse
if 'dream_transcript' in st.session_state:
    st.markdown("### 3. Analyse et traitement du rêve")
    
    # Permettre à l'utilisateur de modifier la transcription si nécessaire
    modified_transcript = st.text_area(
        "Vous pouvez modifier le texte avant l'analyse:",
        st.session_state.dream_transcript,
        height=150,
        key="transcript_editor"
    )
    
    # Bouton pour analyser le texte
    if st.button("Analyser le rêve avec Mistral"):
        with st.spinner("Analyse du rêve en cours..."):
            try:
                # Extraire les éléments visuels
                visual_analysis = extract_visual_elements(modified_transcript)
                
                # Analyser le sentiment
                sentiment_analysis = analyze_dream_sentiment(modified_transcript)
                
                # Sauvegarder les analyses
                st.session_state.visual_analysis = visual_analysis
                st.session_state.sentiment_analysis = sentiment_analysis
                
                # Afficher les résultats
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🎨 Éléments visuels détectés")
                    st.json(visual_analysis["elements_visuels"])
                    
                    st.markdown("#### 🎭 Ambiance du rêve")
                    st.json(visual_analysis["ambiance"])
                
                with col2:
                    st.markdown("#### 😊 Analyse émotionnelle")
                    st.json(sentiment_analysis)
                    
                    st.markdown("#### 🎨 Style recommandé")
                    st.write(f"**{visual_analysis.get('style_recommande', 'artistique')}**")
                
                # Afficher le prompt optimisé
                st.markdown("#### 📝 Description optimisée pour l'image")
                st.write(visual_analysis.get("prompt_optimise", ""))
                
            except Exception as e:
                st.error(f"Erreur lors de l'analyse: {str(e)}")
    
    # Si les analyses existent, afficher la section de génération d'image
    if 'visual_analysis' in st.session_state:
        st.markdown("### 4. Génération d'image")
        
        # Obtenir les styles disponibles
        available_styles = get_available_styles()
        
        # Interface pour choisir le style
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Options de style avec descriptions
            style_options = list(available_styles.keys())
            style_labels = [f"{style}: {desc}" for style, desc in available_styles.items()]
            
            selected_style_idx = st.selectbox(
                "Choisissez un style d'image:", 
                range(len(style_options)),
                format_func=lambda x: style_labels[x],
                help="'automatic' utilise le style recommandé par l'analyse Mistral"
            )
            selected_style = style_options[selected_style_idx]
        
        with col2:
            # Paramètres de l'image
            st.markdown("**Paramètres de l'image**")
            image_width = st.selectbox("Largeur:", [512, 768, 1024], index=2)
            image_height = st.selectbox("Hauteur:", [512, 768, 1024], index=2)
        
        # Créer le prompt final
        image_prompt_data = create_image_prompt(
            st.session_state.visual_analysis, 
            selected_style
        )
        
        # Prévisualiser le prompt modifié selon le style
        if selected_style != "automatic":
            prompt_preview = preview_styled_prompt(
                image_prompt_data["prompt_principal"], 
                selected_style
            )
            
            st.markdown("#### 🔍 Aperçu du prompt modifié")
            with st.expander("Voir les modifications appliquées"):
                st.markdown("**Prompt original (Mistral):**")
                st.text(prompt_preview["original_prompt"])
                st.markdown("**Prompt avec style appliqué:**")
                st.text(prompt_preview["styled_prompt"])
        
        # Afficher le prompt qui sera utilisé
        st.markdown("#### 🖼️ Prompt final pour la génération")
        final_prompt = image_prompt_data["prompt_principal"]
        st.code(final_prompt)
        
        # Bouton de génération d'image
        if st.button("🎨 Générer l'image", type="primary"):
            with st.spinner("Génération de l'image en cours... Cela peut prendre quelques instants..."):
                try:
                    # Générer l'image avec l'API Clipboard
                    result = generate_image_with_clipboard(
                        prompt=final_prompt,
                        style=selected_style
                    )
                    
                    if result["success"]:
                        # Afficher l'image générée
                        st.success("🎉 Image générée avec succès !")
                        
                        # Afficher l'image
                        st.image(
                            result["image"], 
                            caption=f"Votre rêve visualisé en style {selected_style}",
                            use_column_width=True
                        )
                        
                        # Informations sur la génération
                        with st.expander("Détails de la génération"):
                            st.json({
                                "style_utilisé": result["style"],
                                "prompt_utilisé": result["prompt_used"],
                                "dimensions": f"{image_width}x{image_height}",
                                "chemin_image": result["image_path"]
                            })
                        
                        # Sauvegarder dans la session
                        st.session_state.generated_image = result
                        
                        # Bouton de téléchargement
                        if st.button("💾 Télécharger l'image"):
                            # Convertir l'image en bytes pour le téléchargement
                            img_bytes = BytesIO()
                            result["image"].save(img_bytes, format='PNG')
                            img_bytes.seek(0)
                            
                            st.download_button(
                                label="📁 Télécharger PNG",
                                data=img_bytes.getvalue(),
                                file_name=f"dream_image_{selected_style}.png",
                                mime="image/png"
                            )
                    
                    else:
                        # Afficher l'erreur
                        st.error(f"❌ Erreur lors de la génération: {result['error']}")
                        
                        # Suggestion de solutions
                        if "API" in result['error']:
                            st.info("💡 Vérifiez que votre clé API Clipboard est correctement configurée dans le fichier .env")
                        
                except Exception as e:
                    st.error(f"Erreur inattendue: {str(e)}")
        
        # Si une image a été générée, afficher les options supplémentaires
        if 'generated_image' in st.session_state:
            st.markdown("### 5. Actions supplémentaires")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Regénérer avec le même style"):
                    st.rerun()
            
            with col2:
                if st.button("🎨 Essayer un autre style"):
                    # Effacer l'image actuelle pour permettre un nouveau choix
                    if 'generated_image' in st.session_state:
                        del st.session_state.generated_image
                    st.rerun()
            
            with col3:
                if st.button("🆕 Nouveau rêve"):
                    # Effacer toute la session
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

def main():
    """Entry point for the application when run as a package"""
    # Nothing to do as Streamlit automatically runs the script
    pass

if __name__ == "__main__":
    main()
