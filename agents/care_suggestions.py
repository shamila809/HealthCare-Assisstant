# care_suggestions.py
import json

# =============================================================================
# KNOWLEDGE BASE (Care Suggestions)
# =============================================================================
# Strictly General Advice - NO Medicines, NO Diagnosis.

DISEASE_CARE = {
    "viral fever": [
        "Take adequate rest to help your body recover.",
        "Drink plenty of fluids (water, soups, juices) to stay hydrated.",
        "Monitor your body temperature daily.",
        "Use a cool damp cloth on the forehead to comfort fever symptoms.",
        "Avoid strenuous physical activity until fully recovered."
    ],
    "typhoid": [
        "Drink boiled or bottled water only.",
        "Eat home-cooked, easy-to-digest meals.",
        "Avoid raw fruits and vegetables that cannot be peeled.",
        "Wash hands frequently with soap and water.",
        "Complete the full course of rest as advised."
    ],
    "migraine": [
        "Rest in a dark, quiet room.",
        "Apply a cold or warm compress to your head or neck.",
        "Stay hydrated.",
        "Avoid known triggers like bright lights or loud noises.",
        "Practice relaxation techniques like deep breathing."
    ],
    "common cold": [
        "Stay hydrated with warm water or herbal teas.",
        "Rest as much as possible.",
        "Use steam inhalation to relieve congestion.",
        "Gargle with warm salt water for sore throat relief."
    ],
    "diabetes": [
       "Monitor blood sugar levels regularly.",
       "Follow a balanced diet low in sugar and refined carbs.",
       "Ensure regular physical activity as advised.",
       "Keep feet clean and dry; check for any cuts or sores."
    ],
     "hypertension": [
        "Limit salt intake in your diet.",
        "Engage in regular, moderate physical exercise.",
        "Manage stress through relaxation or hobbies.",
        "Avoid tobacco and limit alcohol consumption."
    ],
    "asthma": [
        "Avoid known triggers such as dust, smoke, or cold air.",
        "Keep the living environment clean and dust-free.",
        "Practice breathing exercises as advised.",
        "Ensure adequate rest and avoid overexertion."
    ],

    "gastritis": [
        "Eat small, frequent meals instead of large ones.",
        "Avoid spicy, oily, or acidic foods.",
        "Do not lie down immediately after eating.",
        "Manage stress through relaxation techniques."
    ],

    "urinary tract infection": [
        "Drink plenty of water to stay well hydrated.",
        "Maintain proper personal hygiene.",
        "Avoid holding urine for long periods.",
        "Wear loose, breathable clothing."
    ],

    "anemia": [
        "Include iron-rich foods in your daily meals.",
        "Ensure a balanced diet with adequate nutrients.",
        "Avoid skipping meals.",
        "Take adequate rest if feeling tired."
    ],

    "arthritis": [
        "Engage in gentle joint-friendly exercises.",
        "Maintain a healthy body weight.",
        "Apply warm compresses to stiff joints.",
        "Avoid prolonged strain on affected joints."
    ],

    "allergic rhinitis": [
        "Avoid known allergens like dust or pollen.",
        "Keep windows closed during high pollen seasons.",
        "Maintain cleanliness of bedding and surroundings.",
        "Rinse nose gently with clean water if needed."
    ]

}

SYMPTOM_CARE = {
    "fever": [
        "Keep the room well-ventilated and comfortable.",
        "Wear light, breathable clothing.",
        "Drink plenty of water to prevent dehydration.",
        "Rest continuously."
    ],
    "cough": [
        "Drink warm water or herbal tea with honey.",
        "Use steam inhalation to loosen mucus.",
        "Elevate your head while sleeping to ease breathing.",
        "Avoid cold or sugary drinks that might irritate the throat."
    ],
    "headache": [
        "Drink water, as dehydration serves as a common trigger.",
        "Rest in a quiet, low-lit environment.",
        "Massage your temples gently."
    ],
    "sore throat": [
        "Gargle with warm salt water 2-3 times a day.",
        "Drink warm liquids like soups or herbal teas.",
        "Avoid spicy or acidic foods."
    ],
    "pain": [
        "Apply a warm or cold pack to the affected area.",
        "Rest the affected part of the body.",
        "Maintain good posture."
    ],
    "fatigue": [
        "Prioritize sleep and stick to a regular schedule.",
        "Eat balanced, energy-rich meals.",
        "Stay hydrated throughout the day."
    ],
    "nausea": [
        "Eat small, frequent meals instead of heavy ones.",
        "Drink ginger tea or clear fluids.",
        "Avoid strong smells/odors."
    ],
    "dizziness": [
        "Sit or lie down immediately if you feel dizzy.",
        "Move slowly when changing positions.",
        "Drink water."
    ],
        "shortness of breath": [
        "Sit upright and try to stay calm.",
        "Ensure good airflow in the room.",
        "Avoid strenuous activities.",
        "Practice slow, deep breathing."
    ],

    "chest discomfort": [
        "Rest and avoid physical exertion.",
        "Sit in a comfortable, upright position.",
        "Try to remain calm and relaxed."
    ],

    "vomiting": [
        "Take small sips of clear fluids.",
        "Avoid solid foods until feeling better.",
        "Rest and avoid strong smells."
    ],

    "diarrhea": [
        "Drink plenty of clean fluids to prevent dehydration.",
        "Eat light, easy-to-digest foods.",
        "Maintain good hand hygiene."
    ],

    "loss of appetite": [
        "Eat small meals at regular intervals.",
        "Choose nutritious, easy-to-eat foods.",
        "Drink fluids between meals."
    ],

    "sleep disturbance": [
        "Maintain a regular sleep schedule.",
        "Avoid screens before bedtime.",
        "Create a calm and comfortable sleep environment."
    ],

    "constipation": [
        "Increase fiber intake through fruits and vegetables.",
        "Drink adequate water throughout the day.",
        "Engage in light physical activity."
    ],

    "muscle cramps": [
        "Stretch the affected muscle gently.",
        "Stay hydrated.",
        "Avoid sudden or intense physical exertion."
    ],
    "period pain": [
        "Apply a warm heating pad or hot water bottle to the lower abdomen.",
        "Practice gentle stretching or light physical activity if comfortable.",
        "Drink warm fluids and stay well hydrated."
    ]

    
}

GENERIC_CARE = [
    "Ensure you are getting adequate sleep and rest.",
    "Maintain good hydration by drinking plenty of water.",
    "Eat a balanced diet rich in fruits and vegetables.",
    "Wash hands frequently to maintain hygiene.",
    "Monitor your condition and consult a doctor if symptoms persist."
]

DISCLAIMER = """Disclaimer:
These are general care suggestions and do not replace medical advice.
Always follow your doctor’s instructions."""

def generate_care_suggestions(disease=None, symptoms=None, consultation_summary=None):
    """
    Generates a structured dictionary of care suggestions.
    Returns: { "Condition Name": [List of Suggestions], ... }
    """
    suggestion_map = {}
    
    # Normalize inputs
    disease_str = disease.lower().strip() if disease else ""
    symptom_list = [s.lower().strip() for s in symptoms] if symptoms else []
    summary_text = consultation_summary.lower() if consultation_summary else ""

    # Strategy 1: Disease-Based (Highest Priority)
    if disease_str and disease_str in DISEASE_CARE:
        suggestion_map[disease_str.title()] = DISEASE_CARE[disease_str]
        return suggestion_map

    # Strategy 2: Symptom-Based
    # We want to group suggestions by the symptom that triggered them
    found_symptom_matches = set()
    
    for s in symptom_list:
        for key in SYMPTOM_CARE:
            if key in s: 
                 found_symptom_matches.add(key)
    
    # Strategy 3: Fallback using Consultation Summary
    if not disease_str and not found_symptom_matches and summary_text:
        for d_key in DISEASE_CARE:
            if d_key in summary_text:
                suggestion_map[d_key.title() + " (from summary)"] = DISEASE_CARE[d_key]
                return suggestion_map
        
        for s_key in SYMPTOM_CARE:
            if s_key in summary_text:
                found_symptom_matches.add(s_key)

    # Compile Symptom Suggestions per Symptom
    if found_symptom_matches:
        for key in found_symptom_matches:
            # key is the normalized symptom from KB (e.g. "fever")
            # We add it to the map
            suggestion_map[key.title()] = SYMPTOM_CARE[key]
        return suggestion_map

    # Strategy 4: Generic Fallback
    suggestion_map["General Wellness Advice (No specific match found)"] = GENERIC_CARE
    return suggestion_map

def format_output(suggestion_map):
    """Formats the dictionary into a readable categorized string."""
    output = "General Care Suggestions:\n"
    output += "="*30 + "\n"
    
    for category, tips in suggestion_map.items():
        output += f"\n👉 {category}:\n"
        for tip in tips:
            output += f"   - {tip}\n"
    
    output += "\n" + "-"*40 + "\n"
    output += DISCLAIMER
    return output

if __name__ == "__main__":
    import os
    
    # Determine path to medical_data.json (in transcriptions folder)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_FILE = os.path.join(BASE_DIR, "transcriptions", "medical_data.json")
    
    print(f"📄 Loading medical data from: {DATA_FILE}")
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Extract fields
            extracted_diseases = data.get("diseases", [])
            primary_disease = extracted_diseases[0] if extracted_diseases else None
            
            extracted_symptoms = data.get("symptoms", [])
            
            print(f"🔍 Found: Disease='{primary_disease}', Symptoms={extracted_symptoms}\n")
            
            sugg_map = generate_care_suggestions(disease=primary_disease, symptoms=extracted_symptoms)
            print(format_output(sugg_map))
            
        except Exception as e:
            print(f"❌ Error reading data: {e}")
    else:
        print("❌ 'medical_data.json' not found. Please run 'medical_extractor.py' first.")
