import streamlit as st
import random

st.set_page_config(page_title="Universal Calisthenics", page_icon="💪")

st.title("💪 Dynamic Calisthenics Engine")
st.write("Προσαρμοσμένο πρόγραμμα ανάλογα με τον εξοπλισμό, την ενέργεια και τον χρόνο σου!")

# 1. Επιλογή Εξοπλισμού
location = st.selectbox(
    "📍 Πού θα κάνεις προπόνηση;",
    ["🏠 Σπίτι (Μόνο Σωματικό Βάρος)", "🌳 Πάρκο Καλισθενικής (Full Equipment)"]
)

# 2. Inputs Ενέργειας & Χρόνου
energy = st.slider("Επίπεδο Ενέργειας (1-5)", 1, 5, 3)
time_available = st.number_input("Διαθέσιμος Χρόνος (λεπτά)", min_value=10, max_value=90, value=30)

if st.button("🚀 Δημιουργία Προγράμματος"):

    # --- ΔΕΞΑΜΕΝΕΣ ΑΣΚΗΣΕΩΝ ---
    
    # Α) ΣΠΙΤΙ (Χωρίς εξοπλισμό)
    home_db = {
        "Easy": {
            "Push": ["Knee Push-ups", "Incline Push-ups (σε καρέκλα)"],
            "Pull": ["Doorframe Rows", "Towel Door Resistance Rows"],
            "Legs": ["Bodyweight Squats", "Glute Bridges", "Wall Sits"],
            "Core": ["Plank (Γόνατα)", "Bird-Dog", "Deadbug"]
        },
        "Standard": {
            "Push": ["Standard Push-ups", "Wide Push-ups", "Pike Push-ups (Easy)"],
            "Pull": ["Australian Rows (κάτω από τραπέζι)", "Doorframe L-Sits"],
            "Legs": ["Standard Squats", "Reverse Lunges", "Sumo Squats"],
            "Core": ["Standard Plank", "Mountain Climbers", "Leg Raises"]
        },
        "Hard": {
            "Push": ["Diamond Push-ups", "Decline Push-ups (πόδια σε καρέκλα)", "Pike Push-ups"],
            "Pull": ["Table Inverted Rows (Single Arm)", "Doorframe Isometric Holds"],
            "Legs": ["Jump Squats", "Bulgarian Split Squats", "Lunges with Jump"],
            "Core": ["Side Plank", "Hollow Body Hold", "V-Ups"]
        }
    }

    # Β) ΠΑΡΚΟ (Pull-up bars, Parallel bars, Push-up bars, Monkey bars, Pole)
    park_db = {
        "Easy": {
            "Push": ["Push-up Bars (Standard)", "Parallel Bar Knee Holds", "Incline Push-ups (Low Bar)"],
            "Pull": ["Australian Rows (High Bar)", "Dead Hang (Pull-up Bar)", "Pole Assisted Rows"],
            "Legs": ["Bodyweight Squats", "Walking Lunges", "Bench Step-ups"],
            "Core": ["Plank on Push-up Bars", "Hanging Knee Tucks (Pull-up Bar)", "Pole Knee Raises"]
        },
        "Standard": {
            "Push": ["Push-up Bars (Deep Range)", "Parallel Bar Dips (Assisted/Negative)", "Straight Bar Dips"],
            "Pull": ["Pull-up Negatives (Pull-up Bar)", "Australian Rows (Mid Bar)", "Monkey Bar Swings / Traversing"],
            "Legs": ["Standard Squats", "Jumping Lunges", "Bench Box Jumps"],
            "Core": ["Hanging Leg Raises (Pull-up Bar)", "Parallel Bar Knee Raises", "Pole Flag Hold (Attempt/Prep)"]
        },
        "Hard": {
            "Push": ["Parallel Bar Dips", "Push-up Bars (Pike Dips)", "Single Bar Dips"],
            "Pull": ["Strict Pull-ups", "Chin-ups", "Monkey Bar Pull-up Traverses", "Pole Climbs"],
            "Legs": ["Jump Squats", "Bulgarian Split Squats (on Bench)", "Pistol Squat Prep"],
            "Core": ["Hanging Toes-to-Bar", "Parallel Bar L-Sit", "Pole Human Flag Holds"]
        }
    }

    # Επιλογή της σωστής βάσης δεδομένων
    db = home_db if "Σπίτι" in location else park_db

    # 3. Επιλογή επιπέδου δυσκολίας
    level = "Easy" if energy <= 2 else ("Standard" if energy == 3 else "Hard")
    pool = db[level]

    # 4. Επιλογή ασκήσεων (1 Push, 1 Pull, 1 Legs, 1 Core + 1 Bonus)
    selected_routine = [
        random.choice(pool["Push"]),
        random.choice(pool["Pull"]),
        random.choice(pool["Legs"]),
        random.choice(pool["Core"])
    ]

    all_exercises = pool["Push"] + pool["Pull"] + pool["Legs"] + pool["Core"]
    bonus = random.choice([ex for ex in all_exercises if ex not in selected_routine])
    selected_routine.append(bonus)

    # 5. Υπολογισμός Σετ βάσει Χρόνου
    sets = 2 if time_available < 25 else (3 if time_available < 50 else 4)
    rest = "60-90 sec"

    # Εμφάνιση αποτελεσμάτων
    st.success(f"📍 **Τοποθεσία:** {location.split(' ')[1]} | ⚡ **Επίπεδο:** {level} | 🔄 **Σετ:** {sets} | ⏱️ **Διάλειμμα:** {rest}")

    st.subheader("📋 Το σημερινό σου πλάνο (5 Ασκήσεις):")

    for i, ex in enumerate(selected_routine, 1):
        st.markdown(f"**{i}. {ex}**")

    st.info("💡 Tip: Αν κάποια άσκηση πάρκου είναι κατειλημμένη, πάτα ξανά το κουμπί για να σου βγάλει εναλλακτική!")
