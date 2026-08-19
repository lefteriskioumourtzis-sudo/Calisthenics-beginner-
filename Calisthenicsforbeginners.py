import streamlit as st
import random
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Pro Calisthenics", page_icon="⚡", layout="centered")

# --- SIDEBAR: ΕΠΙΛΟΓΕΣ DESIGN, ΓΛΩΣΣΑΣ & ΤΟΠΟΘΕΣΙΑΣ ---
st.sidebar.title("⚙️ Ρυθμίσεις / Settings")
location = st.sidebar.radio("📍 Τοποθεσία Προπόνησης", ["🏠 Σπίτι (Bodyweight)", "🌳 Πάρκο (Full Equipment)"])
theme = st.sidebar.selectbox("🎨 Θέμα Design", ["Cyberpunk Neon", "Sunset Gold", "Matrix Green", "Ocean Breeze"])
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

# --- ΣΥΝΔΕΣΗ ΜΕ GOOGLE SHEETS (ΜΕΣΩ SERVICE ACCOUNT) ---
def get_gsheet_worksheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], 
        scopes=scopes
    )
    gc = gspread.authorize(creds)
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    sh = gc.open_by_url(url)
    return sh.get_worksheet(0)

# --- ΓΛΩΣΣΙΚΗ ΒΑΣΗ ---
i18n = {
    "EL": {
        "title": "⚡ Pro Calisthenics Generator",
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
        "title": "⚡ Pro Calisthenics Generator",
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

# --- DATABASE (Διαχωρισμός Home vs Park) ---
exercises_db = {
    "🏠 Σπίτι (Bodyweight)": {
        1: {
            "Push": ["Wall Push-ups", "Knee Push-ups", "Wall Sit", "Plank Shoulder Taps", "Incline Push-ups (Chair)"],
            "Pull": ["Door Rows", "Towel Rows", "Wall Angels", "Prone Cobra", "Shadow Boxing"],
            "Legs": ["Bodyweight Squats", "Lunges", "Glute Bridges", "Calf Raises", "Side Lunges"],
            "Core": ["Deadbug", "Plank (on knees)", "Bird-Dog", "Crunch", "Pelvic Tilt"]
        },
        3: {
            "Push": ["Standard Push-ups", "Wide Push-ups", "Pike Push-ups", "Diamond Push-ups", "Decline Push-ups"],
            "Pull": ["Doorframe Rows", "Towel Door Rows", "Superman Holds", "Reverse Snow Angels", "Prone Y-Raises"],
            "Legs": ["Jump Squats", "Bulgarian Split Squats (Chair)", "Pistol Squat Prep", "Calf Raises", "Wall Sit"],
            "Core": ["Leg Raises", "Plank", "Hollow Body Hold", "Side Plank", "Russian Twists"]
        },
        5: {
            "Push": ["Pike Push-ups (Elevated)", "Archer Push-ups", "Pseudo Planche Push-ups", "Handstand Hold (Wall)", "Diamond Push-ups"],
            "Pull": ["Towel Door Rows (Single Arm)", "Superman Pulls", "Back Bridge Holds", "L-Sit (Floor)", "Reverse Plank"],
            "Legs": ["Bulgarian Split Squats", "Jumping Lunges", "Pistol Squats (Chair Assisted)", "Single Leg Glute Bridges", "Wall Sit"],
            "Core": ["Hanging Knee Raises", "Plank (Weighted/Backpack)", "Hollow Body Hold", "Dragon Flag Prep", "V-Ups"]
        },
        10: {
            "Push": ["One Arm Push-ups", "Handstand Push-ups (Wall)", "Planche Push-ups (Tuck)", "Wall HSPU", "Pseudo Planche"],
            "Pull": ["Doorframe One Arm Rows", "Advanced Back Bridge", "Floor L-Sit to Straddle", "Dragon Flag Holds (Floor)", "Prone Cobra Holds"],
            "Legs": ["Pistol Squats", "Shrimp Squats", "Sissy Squats", "Dragon Pistol Squats", "Jump Lunges"],
            "Core": ["Dragon Flags (Floor)", "V-Sit Holds", "Strict Hollow Body", "Ab Wheel Rollouts", "Floor L-Sit"]
        }
    },
    "🌳 Πάρκο (Full Equipment)": {
        1: {
            "Push": ["Incline Push-ups (Low Bar)", "Bench Dips", "Plank Shoulder Taps", "Wall Sit", "Knee Push-ups"],
            "Pull": ["Australian Rows (High Bar)", "Dead Hang", "Scapular Pulls", "Ring Holds", "Band Pull-aparts"],
            "Legs": ["Bodyweight Squats", "Box Step-ups", "Lunges", "Calf Raises", "Glute Bridges"],
            "Core": ["Hanging Knee Holds", "Plank", "Bird-Dog", "Deadbug", "Side Plank"]
        },
        3: {
            "Push": ["Standard Push-ups", "Dips (Parallel Bars)", "Pike Push-ups", "Explosive Push-ups", "Decline Push-ups"],
            "Pull": ["Australian Rows (Low Bar)", "Pull-up Negatives", "Chin-up Negatives", "Ring Rows", "Dead Hangs"],
            "Legs": ["Jump Squats", "Bulgarian Split Squats", "Box Jumps", "Pistol Squat Prep", "Calf Raises"],
            "Core": ["Hanging Knee Raises", "Plank", "Hollow Body Hold", "Side Plank", "Russian Twists"]
        },
        5: {
            "Push": ["Dips (Parallel Bars)", "Elevated Pike Push-ups", "Archer Push-ups", "Handstand Hold", "Straight Bar Dips"],
            "Pull": ["Strict Pull-ups", "Chin-ups", "L-Sit Hang", "Tuck Front Lever Hold", "Ring Pull-ups"],
            "Legs": ["Pistol Squats", "Jumping Lunges", "Bulgarian Split Squats", "High Box Jumps", "Sprints"],
            "Core": ["Hanging Leg Raises", "Tuck Dragon Flag", "L-Sit on Dip Bars", "Toes to Bar (Prep)", "V-Ups"]
        },
        10: {
            "Push": ["Muscle-ups (Push Phase)", "Handstand Push-ups (Free)", "Full Planche Push-ups", "Weighted Dips", "90 Degree Push-ups"],
            "Pull": ["Bar Muscle-ups", "Ring Muscle-ups", "Front Lever Pull-ups", "One Arm Pull-ups", "Human Flag"],
            "Legs": ["Pistol Squats (Weighted)", "Explosive Box Jumps", "Shrimp Squats", "Sprints", "Dragon Pistol Squats"],
            "Core": ["Dragon Flags (Strict)", "Front Lever Holds", "Toes-to-Bar", "Human Flag Holds", "Bar L-Sit to RDL"]
        }
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
    loc_db = exercises_db[location]
    
    available_levels = sorted(loc_db.keys())
    db_level = max([k for k in available_levels if k <= level], default=min(available_levels))
    
    current_pool = loc_db[db_level]
    
    routine = [
        random.choice(current_pool["Push"]),
        random.choice(current_pool["Pull"]),
        random.choice(current_pool["Legs"]),
        random.choice(current_pool["Core"])
    ]
    st.session_state.current_routine = list(dict.fromkeys(routine))
    
    rest_seconds = max(45, 120 - (level * 5))
    hold_seconds = 15 + (level * 3)
    
    st.session_state.calculated_time = {
        "rest": rest_seconds,
        "hold": hold_seconds
    }

# --- DISPLAY CARDS ---
if st.session_state.current_routine:
    st.subheader(f"{t['plan']} ({location})")
    
    rest_t = st.session_state.calculated_time.get("rest", 60)
    hold_t = st.session_state.calculated_time.get("hold", 20)
    
    st.info(f"💡 {t['rest']}: **{rest_t}s** ανάμεσα στα σετ")

    for idx, ex in enumerate(st.session_state.current_routine, 1):
        is_hold = any(word in ex.lower() for word in ["hold", "plank", "hang", "flag", "sit", "bridge"])
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
                    ws.append_row(["Date", "User", "Location", "Level", "Reps/Hold", "Rest Time (s)", "Routine"])
                
                row = [
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    username,
                    location,
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

# --- MEDICAL DISCLAIMER ---
st.caption("⚠️ **Αποποίηση Ευθύνης / Disclaimer:** Η εφαρμογή παρέχει προτεινόμενα προγράμματα γυμναστικής για ενημερωτικούς σκοπούς. Συμβουλευτείτε έναν γιατρό ή επαγγελματία γυμναστή πριν ξεκινήσετε οποιοδήποτε πρόγραμμα.")
