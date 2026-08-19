import streamlit as st

st.set_page_config(page_title="Hero Calisthenics", page_icon="🏋️")

st.title("🏋️ Hero Calisthenics Engine")
st.write("Προσαρμοσμένο πρόγραμμα για 1.77m / 88kg")

# Είσοδοι από τον χρήστη
energy = st.slider("Επίπεδο Ενέργειας (1-5)", 1, 5, 3)
minutes = st.number_input("Διαθέσιμα Λεπτά", min_value=15, max_value=120, value=45, step=5)

if st.button("🔥 Δημιουργία Προγράμματος"):
    if energy >= 4:
        sets = 4
        rest = "60 sec"
        intensity = "Υψηλή 🔥"
    elif energy == 3:
        sets = 3
        rest = "90 sec"
        intensity = "Μεσαία ⚡"
    else:
        sets = 2
        rest = "120 sec"
        intensity = "Χαμηλή / Recovery 🧘"

    st.success(f"**Ένταση:** {intensity} | **Σετ:** {sets} | **Διάλειμμα:** {rest}")

    st.subheader("📋 Ασκήσεις Ημέρας:")
    
    exercises = [
        ("1. Australian Push-ups", "8-12 reps", "Πλάτη & Δικέφαλοι (Βάση για Pull-ups)"),
        ("2. Standard Push-ups", "8-10 reps", "Στήθος & Τρικέφαλοι"),
        ("3. Bodyweight Squats", "12-15 reps", "Πόδια & Γλουτοί"),
        ("4. Reverse Lunges", "10 reps / πόδι", "Πόδια & Ισορροπία"),
        ("5. Plank (Σανίδα)", "30-45 sec", "Πυρήνας")
    ]

    if minutes < 30:
        exercises = exercises[:3]

    for name, reps, target in exercises:
        st.markdown(f"**{name}** — *{reps}*  \n└ Στόχος: {target}")
