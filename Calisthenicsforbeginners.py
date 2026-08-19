import streamlit as st
import random
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Pro Calisthenics", page_icon="💪")

# --- ΣΥΝΔΕΣΗ ΜΕ GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ΓΛΩΣΣΙΚΗ ΒΑΣΗ (Localization) ---
i18n = {
    "EL": {
        "title": "💪 Pro Calisthenics 1-10",
        "username": "Όνομα Χρήστη / Athlete Name",
        "level": "Επίπεδο Δυσκολίας (1-10)",
        "reps": "Επαναλήψεις ανά σετ",
        "generate": "🚀 Δημιουργία Προγράμματος",
        "save": "💾 Αποθήκευση στο Google Sheet",
        "history": "📜 Ιστορικό Προπονήσεων",
        "plan": "📋 Πρόγραμμα Προπόνησης",
        "no_history": "Δεν υπάρχουν καταγεγραμμένες προπονήσεις.",
        "enter_name": "Παρακαλώ εισάγετε όνομα χρήστη για αποθήκευση.",
        "success_save": "Η προπόνηση αποθηκεύτηκε επιτυχώς στο Google Sheet!"
    },
    "EN": {
        "title": "💪 Pro Calisthenics 1-10",
        "username": "Athlete Name / Username",
        "level": "Difficulty Level (1-10)",
        "reps": "Reps per set",
        "generate": "🚀 Generate Routine",
        "save": "💾 Save to Google Sheet",
        "history": "📜 Workout History",
        "plan": "📋 Daily Workout Plan",
        "no_history": "No workouts recorded yet.",
        "enter_name": "Please enter a username to save.",
        "success_save": "Workout successfully saved to Google Sheet!"
    }
}

# --- INITIALIZATION ---
if 'current_routine' not in st.session_state:
    st.session_state.current_routine = []

# --- SIDEBAR (Language) ---
lang = st.sidebar.selectbox("Language / Γλώσσα", ["EL", "EN"])
t = i18n[lang]

st.title(t["title"])

# --- DATABASE (Τα 10 επίπεδα) ---
exercises_db = {
    1: {
        "Push": ["Wall Push-ups", "Knee Push-ups", "Wall Sit", "Plank Shoulder Taps", "Incline Push-ups (Hands on chair)", "Bear Crawl", "Superman", "Cat-Cow", "Plank", "Bird-Dog"],
        "Pull": ["Door Rows", "Towel Rows", "Dead Hang", "Wall Angels", "Scapular Pulls", "Y-Raises", "Reverse Snow Angels", "Pole Holds", "Prone Cobra", "Shadow Boxing"],
        "Legs": ["Bodyweight Squats", "Lunges", "Glute Bridges", "Calf Raises", "Wall Sit", "Side Lunges", "Box Step-ups", "High Knees", "Butt Kicks", "Chair Sit-to-Stand"],
        "Core": ["Deadbug", "Plank (on knees)", "Bird-Dog", "Leg Raises (easy)", "Crunch", "Toe Touches", "Pelvic Tilt", "Heel Slides", "Bridge Hold", "Cat Stretch"]
    },
    2: {
        "Push": ["Standard Push-ups", "Pike Push-ups (knees)", "Diamond Push-ups (knees)", "Plank to Push-up", "Mountain Climbers", "Inchworms", "Bench Dips", "Elevated Push-ups", "Cobra Push-ups", "Tricep Extensions (wall)"],
        "Pull": ["Australian Rows (low)", "Scapular Pulls", "Chin-up Negatives", "Pole Assisted Rows", "Towel Pull-ups", "Superman Pulls", "Band Pull-aparts", "Dead Hangs (active)", "Ring Rows (easy)", "Negative Pull-ups"],
        "Legs": ["Split Squats", "Reverse Lunges", "Sumo Squats", "Jumping Squats (easy)", "Step-ups", "Calf Raises (single leg)", "Glute Bridge (single leg)", "Side Lunge", "Wall Sit", "Frog Squats"],
        "Core": ["Leg Raises (flat)", "Plank (standard)", "Mountain Climbers", "Bicycle Crunches", "Hollow Body Hold (knees)", "Side Plank", "Flutter Kicks", "Russian Twists", "Reverse Crunches", "V-Ups (easy)"]
    },
    3: {
        "Push": ["Standard Push-ups", "Wide Push-ups", "Pike Push-ups", "Diamond Push-ups", "Explosive Push-ups", "Decline Push-ups", "Clap Push-ups", "Archer Push-ups", "Pseudo Planche Push-ups", "Hindu Push-ups"],
        "Pull": ["Australian Rows", "Pull-up Negatives", "Chin-up Negatives", "L-sit Hang (knees)", "Scapular Pull-ups", "Superman Pulls", "Pole Climbs", "Dead Hangs", "Ring Rows", "Negative Pull-ups"],
        "Legs": ["Jump Squats", "Bulgarian Split Squats", "Step-ups", "Pistol Squat Prep", "Calf Raises", "Side Lunge", "Glute Bridge", "Wall Sit", "Frog Jumps", "Box Jumps"],
        "Core": ["Leg Raises", "Plank", "Mountain Climbers", "Bicycle Crunches", "Hollow Body Hold", "Side Plank", "Flutter Kicks", "Russian Twists", "V-Ups", "Reverse Crunches"]
    },
    4: {
        "Push": ["Dips (bench)", "Pike Push-ups", "Archer Push-ups", "Deficit Push-ups", "Pseudo Planche", "Diamond Push-ups", "Wide Push-ups", "Explosive Push-ups", "Incline Dips", "Knee Tuck Push-ups"],
        "Pull": ["Pull-ups (assisted)", "Chin-ups (assisted)", "Australian Rows (hard)", "L-sit Hang", "Scapular Shrugs", "Negative Muscle-up", "Pole Rows", "Ring Rows", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Bulgarian Split Squats", "Jumping Lunges", "Sumo Squats", "Step-ups", "Pistol Squat Prep", "Calf Raises", "Side Lunge", "Glute Bridge", "Wall Sit", "Box Jumps"],
        "Core": ["Hanging Knee Raises", "Plank (weighted)", "Mountain Climbers", "Bicycle Crunches", "Hollow Body Hold", "Side Plank", "Flutter Kicks", "Russian Twists", "V-Ups", "Reverse Crunches"]
    },
    5: {
        "Push": ["Dips (parallel bars)", "Pike Push-ups (elevated)", "Archer Push-ups", "Pseudo Planche", "Diamond Push-ups", "Wide Push-ups", "Explosive Push-ups", "Incline Dips", "Knee Tuck Push-ups", "Handstand Hold (wall)"],
        "Pull": ["Pull-ups", "Chin-ups", "Australian Rows (hard)", "L-sit Hang", "Scapular Shrugs", "Negative Muscle-up", "Pole Rows", "Ring Rows", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Jumping Lunges", "Bulgarian Split Squats", "Step-ups", "Pistol Squat Prep", "Calf Raises", "Side Lunge", "Glute Bridge", "Wall Sit", "Box Jumps", "Pistol Squats"],
        "Core": ["Hanging Leg Raises", "Plank (weighted)", "Mountain Climbers", "Bicycle Crunches", "Hollow Body Hold", "Side Plank", "Flutter Kicks", "Russian Twists", "V-Ups", "Dragon Flag (prep)"]
    },
    6: {
        "Push": ["Dips", "Handstand Push-up (wall)", "Archer Push-ups", "Pseudo Planche", "Diamond Push-ups", "Wide Push-ups", "Explosive Push-ups", "Incline Dips", "Knee Tuck Push-ups", "Handstand Hold"],
        "Pull": ["Pull-ups", "Chin-ups", "Australian Rows (hard)", "L-sit Hang", "Scapular Shrugs", "Negative Muscle-up", "Pole Rows", "Ring Rows", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "Step-ups", "Calf Raises", "Side Lunge", "Glute Bridge", "Wall Sit", "Box Jumps", "Sprints"],
        "Core": ["Hanging Leg Raises", "Dragon Flag (prep)", "Plank (weighted)", "Mountain Climbers", "Bicycle Crunches", "Hollow Body Hold", "Side Plank", "Flutter Kicks", "Russian Twists", "V-Ups"]
    },
    7: {
        "Push": ["Dips", "Handstand Push-up", "Archer Push-ups", "Pseudo Planche", "Diamond Push-ups", "Wide Push-ups", "Explosive Push-ups", "Incline Dips", "Knee Tuck Push-ups", "Handstand Hold"],
        "Pull": ["Pull-ups", "Chin-ups", "Australian Rows (hard)", "L-sit Hang", "Scapular Shrugs", "Negative Muscle-up", "Pole Rows", "Ring Rows", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "Step-ups", "Calf Raises", "Side Lunge", "Glute Bridge", "Wall Sit", "Box Jumps", "Sprints"],
        "Core": ["Hanging Leg Raises", "Dragon Flag", "Plank (weighted)", "Mountain Climbers", "Bicycle Crunches", "Hollow Body Hold", "Side Plank", "Flutter Kicks", "Russian Twists", "V-Ups"]
    },
    8: {
        "Push": ["Dips", "Handstand Push-up", "Archer Push-ups", "Pseudo Planche", "Diamond Push-ups", "Wide Push-ups", "Explosive Push-ups", "Incline Dips", "Knee Tuck Push-ups", "Handstand Hold"],
        "Pull": ["Pull-ups", "Chin-ups", "Australian Rows (hard)", "L-sit Hang", "Scapular Shrugs", "Negative Muscle-up", "Pole Rows", "Ring Rows", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "Step-ups", "Calf Raises", "Side Lunge", "Glute Bridge", "Wall Sit", "Box Jumps", "Sprints"],
        "Core": ["Hanging Leg Raises", "Dragon Flag", "Plank (weighted)", "Mountain Climbers", "Bicycle Crunches", "Hollow Body Hold", "Side Plank", "Flutter Kicks", "Russian Twists", "V-Ups"]
    },
    9: {
        "Push": ["Dips", "Handstand Push-up", "Archer Push-ups", "Pseudo Planche", "Diamond Push-ups", "Wide Push-ups", "Explosive Push-ups", "Incline Dips", "Knee Tuck Push-ups", "Handstand Hold"],
        "Pull": ["Pull-ups", "Chin-ups", "Australian Rows (hard)", "L-sit Hang", "Scapular Shrugs", "Negative Muscle-up", "Pole Rows", "Ring Rows", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "Step-ups", "Calf Raises", "Side Lunge", "Glute Bridge", "Wall Sit", "Box Jumps", "Sprints"],
        "Core": ["Hanging Leg Raises", "Dragon Flag", "Plank (weighted)", "Mountain Climbers", "Bicycle Crunches", "Hollow Body Hold", "Side Plank", "Flutter Kicks", "Russian Twists", "V-Ups"]
    },
    10: {
        "Push": ["Muscle-ups (push phase)", "One Arm Push-ups", "Planche Push-ups", "Handstand Push-ups", "Full Planche Hold", "Aztec Push-ups", "Dips (weighted)", "Archer Pull-ups", "Fingertip Push-ups", "Clap Dips"],
        "Pull": ["Muscle-ups", "Front Lever Pull-ups", "One Arm Pull-ups", "Dragon Flag Pull-ups", "Weighted Pull-ups", "Archer Pull-ups", "Front Lever Hold", "Back Lever", "Pole Flag", "Human Flag"],
        "Legs": ["Pistol Squats (weighted)", "Jump Lunges (explosive)", "Sissy Squats", "Shrimp Squats", "Bulgarian Split Squats (weighted)", "Box Jumps (high)", "Calf Raises (weighted)", "Dragon Pistol Squat", "Explosive Box Jumps", "Sprints (full speed)"],
        "Core": ["Dragon Flags (strict)", "Front Lever Holds", "Toes-to-Bar", "Hanging Windshield Wipers", "Human Flag", "V-Sit", "Planche Holds", "L-Sit (full)", "Russian Twist (weighted)", "Ab Wheel Rollouts"]
    }
}

# --- INPUTS ---
username = st.text_input(t["username"], value="Guest")

col1, col2 = st.columns(2)
with col1:
    level = st.slider(t["level"], 1, 10, 1)
with col2:
    reps = st.number_input(t["reps"], min_value=1, max_value=100, value=10)

# --- ENGINE ---
if st.button(t["generate"]):
    db_level = level if level in exercises_db else max([k for k in exercises_db.keys() if k <= level])
    current_pool = exercises_db[db_level]
    
    routine = [
        random.choice(current_pool["Push"]),
        random.choice(current_pool["Pull"]),
        random.choice(current_pool["Legs"]),
        random.choice(current_pool["Core"])
    ]
    all_ex = current_pool["Push"] + current_pool["Pull"] + current_pool["Legs"] + current_pool["Core"]
    routine.append(random.choice(all_ex))
    
    st.session_state.current_routine = list(dict.fromkeys(routine))

if st.session_state.current_routine:
    st.subheader(t["plan"])
    for ex in st.session_state.current_routine:
        st.markdown(f"✅ **{ex}** - {reps} reps")

    # --- SAVE BUTTON (GOOGLE SHEETS) ---
    if st.button(t["save"]):
        if not username or username == "Guest":
            st.warning(t["enter_name"])
        else:
            try:
                # Διαβάζουμε τα δεδομένα από το Sheet
                existing_data = conn.read(ttl=0)
            except Exception:
                existing_data = pd.DataFrame(columns=["Date", "User", "Level", "Reps", "Routine"])
            
            # Δημιουργούμε τη νέα εγγραφή
            new_entry = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "User": username,
                "Level": level,
                "Reps": reps,
                "Routine": ", ".join(st.session_state.current_routine)
            }])
            
            # Ενώνουμε και αποθηκεύουμε
            updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
            conn.update(data=updated_df)
            st.success(t["success_save"])

# --- ΙΣΤΟΡΙΚΟ (Από το Google Sheet) ---
st.divider()
st.subheader(t["history"])

try:
    data = conn.read(ttl=0)
    if not data.empty:
        # Φιλτράρισμα ανά χρήστη αν το επιλέξει
        filter_user = st.checkbox("Show only my workouts / Εμφάνιση μόνο των δικών μου")
        if filter_user and username:
            data = data[data["User"] == username]
        st.dataframe(data, use_container_width=True)
    else:
        st.write(t["no_history"])
except Exception:
    st.write(t["no_history"])
