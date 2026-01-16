import spacy
import json
import sys
import re
import os
from spacy.matcher import PhraseMatcher, Matcher

# Load English tokenizer, tagger, parser and NER
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("❌ Error: Model 'en_core_web_sm' not found.")
    print("Please run: python -m spacy download en_core_web_sm")
    sys.exit(1)

def extract_medical_info(text):
    doc = nlp(text)
    
    data = {
        "diseases": [],
        "symptoms": [],
        "medicines": []
    }

    # ---------------------------------------------------------
    # 1. Define Knowledge Base (Simple Lists for Demo)
    # ---------------------------------------------------------
    # In a real app, load these from a database or ontology (SNOMED/ICD).
    symptom_list = [
        "fever", "cough", "headache", "sore throat", "pain", "nausea", 
        "vomiting", "dizziness", "fatigue", "rash", "chest pain", "cold", "flu"
    ]
    
    disease_list = [
        "viral fever", "typhoid", "malaria", "diabetes", "hypertension", 
        "infection", "pneumonia", "migraine"
    ]
    
    medicine_indicators = [
        "tablet", "syrup", "capsule", "antibiotic", "injection", "cream", 
        "gel", "drops", "paracetamol", "dolopar", "azithromycin", "crocin"
    ]

    # ---------------------------------------------------------
    # 2. Extract Symptoms & Diseases (PhraseMatcher)
    # ---------------------------------------------------------
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    # Add patterns
    symptom_patterns = [nlp.make_doc(text) for text in symptom_list]
    disease_patterns = [nlp.make_doc(text) for text in disease_list]
    
    matcher.add("SYMPTOM", symptom_patterns)
    matcher.add("DISEASE", disease_patterns)

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]
        if label == "SYMPTOM":
            if span.text.lower() not in data["symptoms"]:
                data["symptoms"].append(span.text.lower())
        elif label == "DISEASE":
            if span.text.lower() not in data["diseases"]:
                data["diseases"].append(span.text.lower())

    # ---------------------------------------------------------
    # 3. Extract Medicines & Dosage (Custom NER / Rules)
    # ---------------------------------------------------------
    # Strategy: Look for sentences containing medicine keywords, 
    # then extract dosage details from the same sentence.
    
    for sent in doc.sents:
        sent_text_lower = sent.text.lower()
        
        # Check if sentence mentions a medicine form or specific name
        if any(ind in sent_text_lower for ind in medicine_indicators):
            
            # Simple extraction strategy: 
            # 1. Find the medicine name (simplest: match known list or look for Nouns near 'tablet/syrup')
            # 2. Find dosage (regex for mg, ml)
            # 3. Find frequency (once daily, twice a day, 1-0-1)
            # 4. Find duration (for 3 days, 1 week)
            
            med_entry = {
                "name": "",
                "dosage": "",
                "timing": "",
                "frequency": "",
                "duration": "",
                "source": "auto_extracted"
            }
            
            # Extract Dosage (e.g., 500mg, 5 ml)
            dosage_pattern = re.search(r"(\d+\s?(?:mg|ml|g|mcg))", sent.text, re.IGNORECASE)
            if dosage_pattern:
                med_entry["dosage"] = dosage_pattern.group(1)

            # Extract Duration (e.g., for 5 days)
            duration_pattern = re.search(r"(?:for\s)(\d+\s(?:days|weeks))", sent.text, re.IGNORECASE)
            if duration_pattern:
                med_entry["duration"] = duration_pattern.group(1)

            # Identify Medicine Name (Heuristic: Look for Proper Nouns or Nouns around keywords)
            # For this demo, we'll try to match from our indicator list + context
            matching_meds = [m for m in medicine_indicators if m in sent_text_lower]
            if matching_meds:
                # Pick the most specific one or combine (e.g., "paracetamol tablet")
                # Here we just take the first matched keyword as a safe fallback
                med_entry["name"] = matching_meds[0] 
                
                # Try to find a Proper Noun preceding "tablet" or "syrup"
                for i, token in enumerate(sent):
                    if token.text.lower() in ["tablet", "syrup", "capsule", "injection"]:
                        # Look at previous token
                        if i > 0 and (sent[i-1].pos_ == "PROPN" or sent[i-1].pos_ == "NOUN"):
                             med_entry["name"] = f"{sent[i-1].text} {token.text}"

            # Only add if we found a potential medicine
            if med_entry["name"]:
                data["medicines"].append(med_entry)

    return data

def main():
    # Determine project root
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TRANSCRIPTIONS_DIR = os.path.join(BASE_DIR, "transcriptions")
    
    # Ensure directory exists even if we just want to read (good practice)
    if not os.path.exists(TRANSCRIPTIONS_DIR):
         os.makedirs(TRANSCRIPTIONS_DIR, exist_ok=True)

    input_file = os.path.join(TRANSCRIPTIONS_DIR, "transcription_output.txt")
    output_file = os.path.join(TRANSCRIPTIONS_DIR, "medical_data.json")
    
    # Allow command line arg for file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    print(f"📄 Reading from: {input_file}")
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    print("🧩 Extracting medical info...")
    info = extract_medical_info(text)
    
    output_json = json.dumps(info, indent=2)
    print("\n✅ Extraction Complete:")
    print(output_json)
    
    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_json)
    print(f"\n💾 Saved to '{output_file}'")

if __name__ == "__main__":
    main()
