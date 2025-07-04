import os
import json
from mistralai import Mistral
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialiser le client Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)

def extract_visual_elements(raw_text):
    """
    Utilise Mistral pour extraire et enrichir les éléments visuels d'un rêve
    """
    
    # Prompt optimisé pour extraire les éléments visuels
    prompt = f"""
Tu es un expert en analyse de rêves et en génération d'images. Analyse ce récit de rêve et extrais tous les éléments visuels importants pour créer une image détaillée.

RÉCIT DU RÊVE:
{raw_text}

INSTRUCTIONS:
1. Identifie les ÉLÉMENTS VISUELS principaux (personnages, objets, lieux, couleurs, lumière)
2. Détermine l'AMBIANCE et l'ÉMOTION dominante du rêve
3. Extrait les DÉTAILS SENSORIELS qui peuvent être traduits visuellement
4. Identifie le STYLE artistique approprié (surréaliste, réaliste, fantastique, etc.)
5. Crée une DESCRIPTION OPTIMISÉE pour un générateur d'images

FORMAT DE RÉPONSE (JSON):
{{
    "elements_visuels": {{
        "personnages": ["description des personnages"],
        "objets": ["liste des objets importants"],
        "environnement": "description de l'environnement/lieu",
        "couleurs": ["couleurs dominantes"],
        "lumiere": "description de l'éclairage"
    }},
    "ambiance": {{
        "emotion": "émotion principale (joyeux, anxieux, paisible, etc.)",
        "atmosphere": "description de l'atmosphère",
        "intensite": "faible/moyenne/forte"
    }},
    "style_recommande": "style artistique recommandé",
    "prompt_optimise": "description complète et optimisée pour générateur d'images",
    "mots_cles": ["mots-clés importants pour l'image"]
}}

Réponds uniquement en JSON valide, sans texte supplémentaire.
"""

    try:
        # Appel à l'API Mistral
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Créativité modérée
            max_tokens=1500
        )
        
        # Extraire le contenu de la réponse
        content = response.choices[0].message.content
        
        # Parser le JSON
        try:
            processed_data = json.loads(content)
            return processed_data
        except json.JSONDecodeError:
            # Si le JSON n'est pas valide, retourner une structure basique
            return {
                "elements_visuels": {"environnement": raw_text},
                "ambiance": {"emotion": "neutre", "atmosphere": "indéterminée", "intensite": "moyenne"},
                "style_recommande": "artistique",
                "prompt_optimise": raw_text,
                "mots_cles": raw_text.split()[:10]
            }
            
    except Exception as e:
        print(f"Erreur lors du traitement avec Mistral: {e}")
        # Retourner une structure de base en cas d'erreur
        return {
            "elements_visuels": {"environnement": raw_text},
            "ambiance": {"emotion": "neutre", "atmosphere": "indéterminée", "intensite": "moyenne"},
            "style_recommande": "artistique", 
            "prompt_optimise": raw_text,
            "mots_cles": []
        }

def analyze_dream_sentiment(raw_text):
    """
    Analyse le sentiment et l'émotion du rêve avec Mistral
    """
    
    prompt = f"""
Analyse ce récit de rêve et détermine son sentiment émotionnel global.

RÉCIT: {raw_text}

Réponds en JSON avec cette structure exacte:
{{
    "sentiment_global": "positif/neutre/négatif",
    "emotions_principales": ["liste des émotions détectées"],
    "niveau_stress": "faible/moyen/élevé",
    "type_reve": "cauchemar/rêve paisible/rêve aventureux/rêve étrange/autre",
    "recommandation_style": "style visuel recommandé basé sur l'émotion"
}}
"""

    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Plus déterministe pour l'analyse
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        print(f"Erreur analyse sentiment: {e}")
        return {
            "sentiment_global": "neutre",
            "emotions_principales": ["indéterminé"],
            "niveau_stress": "moyen",
            "type_reve": "autre",
            "recommandation_style": "artistique"
        }

def create_image_prompt(processed_data, style_preference="automatique"):
    """
    Crée un prompt optimisé pour la génération d'image
    """
    
    elements = processed_data.get("elements_visuels", {})
    ambiance = processed_data.get("ambiance", {})
    
    # Style de base
    if style_preference == "automatique":
        style = processed_data.get("style_recommande", "artistique")
    else:
        style = style_preference
    
    # Construction du prompt
    prompt_parts = []
    
    # Environnement principal
    if elements.get("environnement"):
        prompt_parts.append(f"Environnement: {elements['environnement']}")
    
    # Personnages
    if elements.get("personnages"):
        prompt_parts.append(f"Personnages: {', '.join(elements['personnages'])}")
    
    # Objets
    if elements.get("objets"):
        prompt_parts.append(f"Objets: {', '.join(elements['objets'])}")
    
    # Ambiance et couleurs
    if ambiance.get("emotion"):
        prompt_parts.append(f"Ambiance {ambiance['emotion']}")
    
    if elements.get("couleurs"):
        prompt_parts.append(f"Couleurs dominantes: {', '.join(elements['couleurs'])}")
    
    # Assemblage final
    final_prompt = f"{processed_data.get('prompt_optimise', '')}, style {style}, haute qualité, détaillé"
    
    return {
        "prompt_principal": final_prompt,
        "prompt_detaille": " | ".join(prompt_parts),
        "style_applique": style,
        "mots_cles": processed_data.get("mots_cles", [])
    }
