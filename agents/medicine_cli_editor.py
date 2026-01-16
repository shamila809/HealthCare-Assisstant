# medicine_cli_editor.py
import json
import os
import sys

# Try to import TUI library, fallback if missing
try:
    import questionary
    from questionary import Choice, Style
    HAS_TUI = True
except ImportError:
    HAS_TUI = False
    print("⚠️  'questionary' library not found. Running in basic text mode.")

# File Constants
# Determine project root (parent of 'agents' dir)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSCRIPTIONS_DIR = os.path.join(BASE_DIR, "transcriptions")
INPUT_FILE = os.path.join(TRANSCRIPTIONS_DIR, "medical_data.json")
OUTPUT_FILE = os.path.join(TRANSCRIPTIONS_DIR, "final_prescription.json")

# Custom Style (Only used if HAS_TUI)
if HAS_TUI:
    custom_style = Style([
        ('qmark', 'fg:#5f819d bold'),
        ('question', 'bold'),
        ('answer', 'fg:#f44336 bold'),
        ('pointer', 'fg:#673ab7 bold'),
        ('highlighted', 'fg:#673ab7 bold'),
        ('selected', 'fg:#cc5454'),
        ('separator', 'fg:#cc5454'),
        ('instruction', ''),
        ('text', ''),
        ('disabled', 'fg:#858585 italic')
    ])

def load_data(filename):
    """Loads JSON data from the given file."""
    if not os.path.exists(filename):
        print(f"⚠️  File '{filename}' not found. Looking in: {BASE_DIR}")
        return {"medicines": []}
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "medicines" not in data:
                data["medicines"] = []
            return data
    except json.JSONDecodeError:
        print(f"❌ Error: Failed to decode '{filename}'.")
        return {"medicines": []}

def save_data(data, filename):
    """Saves the data dictionary to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"\n✅ Successfully saved to '{filename}'")
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def format_medicine_label(med):
    """Formats a medicine dictionary into a string for selection lists."""
    name = med.get("name", "Unknown")[:20]
    dosage = med.get("dosage", "-")[:10]
    freq = med.get("frequency", "-")[:15]
    return f"{name:<20} | {dosage:<10} | {freq:<15}"

# ------------------------------------------------------------------
# Input Helpers (TUI vs Basic)
# ------------------------------------------------------------------

def get_text_input(prompt, default=""):
    """Wrapper to get text input using TUI or basic input."""
    if HAS_TUI:
        return questionary.text(prompt, default=default).ask()
    else:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default

def get_choice_input(prompt, choices):
    """Wrapper to get a selection from a list."""
    if HAS_TUI:
        # TUI Mode
        q_choices = []
        for c in choices:
            q_choices.append(Choice(title=c['title'], value=c['value']))
            
        return questionary.select(prompt, choices=q_choices, style=custom_style).ask()
    else:
        # Basic Mode
        print(f"\n{prompt}")
        for idx, c in enumerate(choices):
            print(f"{idx + 1}. {c['title']}")
            
        selection = input("Select Number: ").strip()
        try:
            sel_idx = int(selection) - 1
            if 0 <= sel_idx < len(choices):
                return choices[sel_idx]['value']
        except ValueError:
            pass
        return None

def confirm_action(prompt):
    """Wrapper for yes/no confirmation."""
    if HAS_TUI:
        return questionary.confirm(prompt).ask()
    else:
        return input(f"{prompt} (y/n): ").lower() == 'y'

# ------------------------------------------------------------------
# Core Logic
# ------------------------------------------------------------------

def get_medicine_input(default_data=None):
    """Interactive form to get medicine details."""
    if default_data is None:
        default_data = {}

    name = get_text_input("Medicine Name:", default_data.get("name", ""))
    if not name: return None 

    dosage = get_text_input("Dosage (e.g., 500mg):", default_data.get("dosage", ""))
    frequency = get_text_input("Frequency (e.g., 1-0-1):", default_data.get("frequency", ""))
    timing = get_text_input("Timing (e.g., after food):", default_data.get("timing", ""))
    duration = get_text_input("Duration (e.g., 5 days):", default_data.get("duration", ""))
    notes = get_text_input("Notes:", default_data.get("notes", ""))

    return {
        "name": name,
        "dosage": dosage,
        "frequency": frequency,
        "timing": timing,
        "duration": duration,
        "notes": notes,
        "source": "manual"
    }

def add_medicine(medicines):
    """Adds a new medicine."""
    print("\n➕ Add New Medicine")
    new_med = get_medicine_input()
    if new_med:
        medicines.append(new_med)
        print("✅ Medicine added.")

def edit_medicine(medicines):
    """Select and edit a medicine."""
    if not medicines:
        print("⚠️ No medicines to edit.")
        return

    choices = [{'title': format_medicine_label(m), 'value': idx} for idx, m in enumerate(medicines)]
    choices.append({'title': "Cancel", 'value': -1})

    idx = get_choice_input("Select medicine to edit:", choices)

    if idx == -1 or idx is None:
        return

    print(f"\n✏️  Editing: {medicines[idx].get('name')}")
    updated_med = get_medicine_input(medicines[idx])
    
    if updated_med:
        medicines[idx] = updated_med
        print("✅ Medicine updated.")

def delete_medicine(medicines):
    """Select and delete a medicine."""
    if not medicines:
        print("⚠️ No medicines to delete.")
        return

    choices = [{'title': format_medicine_label(m), 'value': idx} for idx, m in enumerate(medicines)]
    choices.append({'title': "Cancel", 'value': -1})

    idx = get_choice_input("Select medicine to delete:", choices)

    if idx == -1 or idx is None:
        return

    if confirm_action(f"Are you sure you want to delete '{medicines[idx].get('name')}'?"):
        deleted = medicines.pop(idx)
        print(f"🗑️  Deleted: {deleted.get('name')}")

def main():
    print("💊 Medicine CLI Editor")
    
    full_data = load_data(INPUT_FILE)
    medicines = full_data.get("medicines", [])

    while True:
        # Show specific table via print for overview (Source Hidden)
        print("\n" + "="*95)
        print(f"{'Name':<20} | {'Dosage':<10} | {'Frequency':<15} | {'Timing':<15} | {'Duration':<10}")
        print("-" * 95)
        for m in medicines:
            print(f"{m.get('name','')[:20]:<20} | {m.get('dosage','')[:10]:<10} | {m.get('frequency','')[:15]:<15} | {m.get('timing','')[:15]:<15} | {m.get('duration','')[:10]:<10}")
        print("-" * 95 + "\n")

        action = get_choice_input(
            "What would you like to do?",
            [
                {'title': "Add Medicine", 'value': "add"},
                {'title': "Edit Medicine", 'value': "edit"},
                {'title': "Delete Medicine", 'value': "delete"},
                {'title': "Save & Exit", 'value': "save"},
                {'title': "Quit without Saving", 'value': "quit"},
            ]
        )

        if action == "add":
            add_medicine(medicines)
        elif action == "edit":
            edit_medicine(medicines)
        elif action == "delete":
            delete_medicine(medicines)
        elif action == "save":
            if confirm_action(f"Save to '{OUTPUT_FILE}'?"):
                full_data["medicines"] = medicines
                if save_data(full_data, OUTPUT_FILE):
                    break
        elif action == "quit":
            print("Exiting without saving.")
            break
        elif action is None:
            # Basic mode might return None on invalid input, or TUI on cancel with Ctrl+C
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
