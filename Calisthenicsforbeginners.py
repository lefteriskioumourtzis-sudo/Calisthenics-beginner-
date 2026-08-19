import streamlit as st
import random
import pandas as pd
from datetime import datetime
import gspread

# --- ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Pro Calisthenics", page_icon="⚡", layout="centered")

# --- SIDEBAR: ΕΠΙΛΟΓΗ ΘΕΜΑΤΟΣ & ΓΛΩΣΣΑΣ ---
st.sidebar.title("🎨 Προσαρμογή")
theme = st.sidebar.selectbox("Επίλεξε Θέμα Design", ["Cyberpunk Neon", "Sunset Gold", "Matrix Green", "Ocean Breeze"])
lang = st.sidebar.selectbox("🌐 Language / Γλώσσα", ["EL", "EN"])

# --- ΔΥΝΑΜΙΚΑ CSS ΘΕΜΑΤΑ ---
themes_css = {
    "Cyberpunk Neon": """
        .stApp {
            background: linear-gradient(-45deg, #0f172a, #2e1065, #3b0764, #0284c7);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #f8fafc;
        }
        .exercise-card {
            background: rgba(15, 23, 42, 0.75);
            border-left: 6px solid #f43f5e;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 0 15px rgba(244, 63, 94, 0.3);
            backdrop-filter: blur(12px);
        }
        .exercise-title { font-size: 1.2rem; font-weight: 700; color: #38bdf8; }
        .badge { background: #f43f5e; color: white; padding: 4px 10px; border-radius: 20px; font-weight: bold; }
        .stButton>button { background: linear-gradient(90deg, #f43f5e, #a855f7); color: white; border-radius: 12px; font-weight: bold; border: none; }
    """,
    "Sunset Gold": """
        .stApp {
            background: linear-gradient(-45deg, #1c1917, #451a03, #78350f, #292524);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #fef3c7;
        }
        .exercise-card {
            background: rgba(41, 37, 36, 0.8);
            border-left: 6px solid #f59e0b;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);
            backdrop-filter: blur(10px);
        }
        .exercise-title { font-size: 1.2rem; font-weight: 700; color: #fbbf24; }
        .badge { background: #d97706; color: white; padding: 4px 10px; border-radius: 20px; font-weight: bold; }
        .stButton>button { background: linear-gradient(90deg, #f59e0b, #ea580c); color: white; border-radius: 12px; font-weight: bold; border: none; }
    """,
    "Matrix Green": """
        .stApp {
            background: #052e16;
            color: #4ade80;
        }
        .exercise-card {
            background: rgba(20, 83, 45, 0.6);
            border: 1px solid #22c55e;
            border-left: 6px solid #4ade80;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
        }
        .exercise-title { font-size: 1.2rem; font-weight: 700; color: #86efac; }
        .badge { background: #15803d; color: #f0fdf4; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
        .stButton>button { background: #22c55e; color: #052e16; border-radius: 6px; font-weight: bold; border: none; }
    """,
    "Ocean Breeze": """
        .stApp {
            background: linear-gradient(-45deg, #0f172a, #0c4a6e, #0369a1, #0284c7);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #f0f9ff;
        }
        .exercise-card {
            background: rgba(15, 23, 42, 0.75);
            border-left: 6px solid #38bdf8;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2);
            backdrop-filter: blur(12px);
        }
        .exercise-title { font-size: 1.2rem; font-weight: 700; color: #7dd3fc; }
        .badge { background: #0284c7; color: white; padding: 4px 10px; border-radius: 20px; font-weight: bold; }
        .stButton>button { background: linear-gradient(90deg, #0284c7, #2563eb); color: white; border-radius: 12px; font-weight: bold; border: none; }
    """
}

# Εφαρμογή του επιλεγμένου CSS + animation
st.markdown(f"""
    <style>
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    {themes_css[theme]}
    .stButton>button:hover {{
        transform: translateY(-2px);
        filter: brightness(1.2);
    }}
    </style>
""", unsafe_allow_html=True)

# --- ΣΥΝΔΕΣΗ ΜΕ GOOGLE SHEETS ---
def get_gsheet_worksheet():
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    gc = gspread.public_connector()
    sh = gc.open_by_url(url)
    return sh.get_worksheet(0)

# --- ΓΛΩΣΣΙΚΗ ΒΑΣΗ ---
i18n = {
    "EL": {
        "title": "⚡ Pro Calisthenics Routine",
        "username": "👤 Όνομα Αθλητή",
        "level": "🎯 Επίπεδο Δυσκολίας (1-10)",
        "reps": "🔢 Επαναλήψεις ανά σετ",
        "generate": "🚀 Δημιουργία Προγράμματος",
        "save": "💾 Αποθήκευση στο Google Sheet",
        "history": "📜 Ιστορικό Προπονήσεων",
        "plan": "📋 Το Πρόγραμμά σου",
        "rest": "⏱️ Προτεινόμενη Ξεκούραση",
        "no_history": "Δεν υπάρχουν καταγεγραμμένες προπονήσεις.",
        "enter_name": "Παρακαλώ εισάγετε όνομα χρήστη.",
        "success_save": "Η προπόνηση αποθηκεύτηκε επιτυχώς!"
    },
    "EN": {
        "title": "⚡ Pro Calisthenics Routine",
        "username": "👤 Athlete Name",
        "level": "🎯 Difficulty Level (1-10)",
        "reps": "🔢 Reps per set",
        "generate": "🚀 Generate Routine",
        "save": "💾 Save to Google Sheet",
        "history": "📜 Workout History",
        "plan": "📋 Your Routine",
        "rest": "⏱️ Suggested Rest Time",
        "no_history": "No workouts recorded yet.",
        "enter_name": "Please enter a username.",
        "success_save": "Workout successfully saved!"
    }
}

t = i18n[lang]
st.title(t["title"])

# --- DATABASE (10 Επίπεδα) ---
exercises_db = {
    1: {
        "Push": ["Wall Push-ups", "Knee Push-ups", "Wall Sit", "Plank Shoulder Taps", "Incline Push-ups"],
        "Pull": ["Door Rows", "Towel Rows", "Dead Hang", "Wall Angels", "Scapular Pulls"],
        "Legs": ["Bodyweight Squats", "Lunges", "Glute Bridges", "Calf Raises", "Side Lunges"],
        "Core": ["Deadbug", "Plank (on knees)", "Bird-Dog", "Crunch", "Pelvic Tilt"]
    },
    2: {
        "Push": ["Standard Push-ups", "Pike Push-ups (knees)", "Diamond Push-ups (knees)", "Plank to Push-up", "Bench Dips"],
        "Pull": ["Australian Rows (low)", "Chin-up Negatives", "Towel Pull-ups", "Dead Hangs (active)", "Ring Rows (easy)"],
        "Legs": ["Split Squats", "Reverse Lunges", "Sumo Squats", "Step-ups", "Frog Squats"],
        "Core": ["Leg Raises (flat)", "Plank (standard)", "Mountain Climbers", "Bicycle Crunches", "Side Plank"]
    },
    3: {
        "Push": ["Standard Push-ups", "Wide Push-ups", "Pike Push-ups", "Diamond Push-ups", "Decline Push-ups"],
        "Pull": ["Australian Rows", "Pull-up Negatives", "Chin-up Negatives", "Scapular Pull-ups", "Ring Rows"],
        "Legs": ["Jump Squats", "Bulgarian Split Squats", "Pistol Squat Prep", "Calf Raises", "Box Jumps"],
        "Core": ["Leg Raises", "Plank", "Hollow Body Hold", "Side Plank", "Russian Twists"]
    },
    4: {
        "Push": ["Dips (bench)", "Pike Push-ups", "Archer Push-ups", "Pseudo Planche", "Incline Dips"],
        "Pull": ["Pull-ups (assisted)", "Chin-ups (assisted)", "Australian Rows (hard)", "L-sit Hang", "Ring Rows"],
        "Legs": ["Bulgarian Split Squats", "Jumping Lunges", "Sumo Squats", "Box Jumps", "Side Lunge"],
        "Core": ["Hanging Knee Raises", "Plank (weighted)", "Hollow Body Hold", "Flutter Kicks", "V-Ups"]
    },
    5: {
        "Push": ["Dips (parallel bars)", "Pike Push-ups (elevated)", "Archer Push-ups", "Handstand Hold (wall)", "Pseudo Planche"],
        "Pull": ["Pull-ups", "Chin-ups", "L-sit Hang", "Tuck Front Lever", "Negative Muscle-up"],
        "Legs": ["Jumping Lunges", "Bulgarian Split Squats", "Pistol Squat Prep", "Pistol Squats", "Box Jumps"],
        "Core": ["Hanging Leg Raises", "Plank (weighted)", "Hollow Body Hold", "Dragon Flag (prep)", "V-Ups"]
    },
    6: {
        "Push": ["Dips", "Handstand Push-up (wall)", "Archer Push-ups", "Pseudo Planche", "Handstand Hold"],
        "Pull": ["Pull-ups", "Chin-ups", "Negative Muscle-up", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "Box Jumps", "Sprints"],
        "Core": ["Hanging Leg Raises", "Dragon Flag (prep)", "Hollow Body Hold", "Side Plank", "V-Ups"]
    },
    7: {
        "Push": ["Dips", "Handstand Push-up", "Archer Push-ups", "Pseudo Planche", "Handstand Hold"],
        "Pull": ["Pull-ups", "Chin-ups", "Negative Muscle-up", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "Box Jumps", "Sprints"],
        "Core": ["Hanging Leg Raises", "Dragon Flag", "Hollow Body Hold", "Side Plank", "V-Ups"]
    },
    8: {
        "Push": ["Dips", "Handstand Push-up", "Archer Push-ups", "Pseudo Planche", "Handstand Hold"],
        "Pull": ["Pull-ups", "Chin-ups", "Negative Muscle-up", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "Box Jumps", "Sprints"],
        "Core": ["Hanging Leg Raises", "Dragon Flag", "Hollow Body Hold", "Side Plank", "V-Ups"]
    },
    9: {
        "Push": ["Dips", "Handstand Push-up", "Archer Push-ups", "Pseudo Planche", "Handstand Hold"],
        "Pull": ["Pull-ups", "Chin-ups", "Negative Muscle-up", "Tuck Front Lever", "Chin-up Holds"],
        "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "Box Jumps", "Sprints"],
        "Core": ["Hanging Leg Raises", "Dragon Flag", "Hollow Body Hold", "Side Plank", "V-Ups"]
    },
    10: {
        "Push": ["Muscle-ups (push phase)", "One Arm Push-ups", "Planche Push-ups", "Handstand Push-ups", "Full Planche Hold"],
        "Pull": ["Muscle-ups", "Front Lever Pull-ups", "One Arm Pull-ups", "Weighted Pull-ups", "Human Flag"],
        "Legs": ["Pistol Squats (weighted)", "Jump Lunges (explosive)", "Sissy Squats", "Dragon Pistol Squat", "Sprints"],
        "Core": ["Dragon Flags (strict)", "Front Lever Holds", "Toes-to-Bar", "Human Flag", "Ab Wheel Rollouts"]
    }
}

if 'current_routine' not in st.session_state:
    st.session_state.current_routine = []
if 'calculated_time' not in st.session_state:
    st.session_state.calculated_time = {}

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
    st.session_state.current_routine = list(dict.fromkeys(routine))
    
    # Αυτόματος υπολογισμός χρόνου
    rest_seconds = max(45, 120 - (level * 5))
    hold_seconds = 15 + (level * 3)
    
    st.session_state.calculated_time = {
        "rest": rest_seconds,
        "hold": hold_seconds
    }

# --- DISPLAY CARDS ---
if st.session_state.current_routine:
    st.subheader(t["plan"])
    
    rest_t = st.session_state.calculated_time.get("rest", 60)
    hold_t = st.session_state.calculated_time.get("hold", 20)
    
    st.info(f"💡 {t['rest']}: **{rest_t}s** ανάμεσα στα σετ")

    for idx, ex in enumerate(st.session_state.current_routine, 1):
        is_hold = any(word in ex.lower() for word in ["hold", "plank", "hang", "flag", "sit"])
        metric = f"{hold_t} sec hold" if is_hold else f"{reps} reps"
        
        st.markdown(f"""
            <div class="exercise-card">
                <div class="exercise-title">#{idx} {ex}</div>
                <div style="margin-top: 8px;">
                    <span class="badge">{metric}</span> &nbsp; • &nbsp; 3-4 Sets
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- SAVE BUTTON ---
    if st.button(t["save"]):
        if not username or username == "Guest":
            st.warning(t["enter_name"])
        else:
            try:
                ws = get_gsheet_worksheet()
                if len(ws.get_all_values()) == 0:
                    ws.append_row(["Date", "User", "Level", "Reps/Hold", "Rest Time (s)", "Routine"])
                
                row = [
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    username,
                    str(level),
                    f"{reps} reps / {hold_t}s hold",
                    str(rest_t),
                    ", ".join(st.session_state.current_routine)
                ]
                ws.append_row(row)
                st.success(t["success_save"])
            except Exception as e:
                st.error(f"Error: {e}")

# --- HISTORY ---
st.divider()
st.subheader(t["history"])

try:
    ws = get_gsheet_worksheet()
    records = ws.get_all_records()
    if records:
        df = pd.DataFrame(records)
        filter_user = st.checkbox("Show only my workouts / Εμφάνιση μόνο των δικών μου")
        if filter_user and username:
            df = df[df["User"] == username]
        st.dataframe(df, use_container_width=True)
    else:
        st.write(t["no_history"])
except Exception:
    st.write(t["no_history"])          
