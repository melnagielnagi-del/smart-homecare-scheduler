# Smart Homecare Scheduler (Streamlit Web App)
# All Rights Reserved © Dr. Yousra Abdelatti

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# -------------------------------
# Initial Setup
# -------------------------------
if "patients" not in st.session_state:
    st.session_state.patients = []
if "doctors" not in st.session_state:
    st.session_state.doctors = ["Dr. A", "Dr. B", "Dr. C"]
if "schedule" not in st.session_state:
    st.session_state.schedule = pd.DataFrame()

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# -------------------------------
# Functions
# -------------------------------
def generate_schedule():
    if not st.session_state.patients or not st.session_state.doctors:
        return pd.DataFrame()

    schedule = []
    start_date = datetime.today()

    for i, patient in enumerate(st.session_state.patients):
        assigned_day = DAYS[i % 7]
        assigned_doctor = random.choice(st.session_state.doctors)
        visit_date = start_date + timedelta(days=i % 7)

        schedule.append({
            "Patient": patient,
            "Doctor": assigned_doctor,
            "Day": assigned_day,
            "Date": visit_date.strftime("%Y-%m-%d"),
        })

    return pd.DataFrame(schedule)

def add_patient(name):
    if name and name not in st.session_state.patients:
        st.session_state.patients.append(name)

def add_doctor(name):
    if name and name not in st.session_state.doctors:
        st.session_state.doctors.append(name)

def remove_patient(name):
    if name in st.session_state.patients:
        st.session_state.patients.remove(name)

def remove_doctor(name):
    if name in st.session_state.doctors:
        st.session_state.doctors.remove(name)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Smart Homecare Scheduler", page_icon="💖", layout="wide")

st.title("💖 Smart Homecare Scheduler")
st.markdown("Plan and manage your homecare visits with style — All Rights Reserved © Dr. Yousra Abdelatti")

menu = st.sidebar.radio("📌 Menu", [
    "Add Patients", "Edit Patients",
    "Add Doctors", "Edit Doctors",
    "Generate Schedule", "View Schedule", "Reschedule"
])

# -------------------------------
# Patients
# -------------------------------
if menu == "Add Patients":
    st.subheader("➕ Add Patient")
    patient_name = st.text_input("Enter patient name:")
    if st.button("Add Patient"):
        add_patient(patient_name)
        st.success(f"✅ Patient {patient_name} added")

elif menu == "Edit Patients":
    st.subheader("✏️ Edit Patients")
    if st.session_state.patients:
        patient_to_remove = st.selectbox("Select patient to remove:", st.session_state.patients)
        if st.button("Remove Patient"):
            remove_patient(patient_to_remove)
            st.warning(f"❌ Patient {patient_to_remove} removed")
    else:
        st.info("No patients available.")

# -------------------------------
# Doctors
# -------------------------------
elif menu == "Add Doctors":
    st.subheader("➕ Add Doctor")
    doctor_name = st.text_input("Enter doctor name:")
    if st.button("Add Doctor"):
        add_doctor(doctor_name)
        st.success(f"✅ Doctor {doctor_name} added")

elif menu == "Edit Doctors":
    st.subheader("✏️ Edit Doctors")
    if st.session_state.doctors:
        doctor_to_remove = st.selectbox("Select doctor to remove:", st.session_state.doctors)
        if st.button("Remove Doctor"):
            remove_doctor(doctor_to_remove)
            st.warning(f"❌ Doctor {doctor_to_remove} removed")
    else:
        st.info("No doctors available.")

# -------------------------------
# Schedule
# -------------------------------
elif menu == "Generate Schedule":
    st.subheader("📅 Generate Weekly Schedule")
    st.session_state.schedule = generate_schedule()
    if not st.session_state.schedule.empty:
        st.success("✅ Schedule generated successfully!")

elif menu == "View Schedule":
    st.subheader("📖 Current Schedule")
    if not st.session_state.schedule.empty:
        st.dataframe(st.session_state.schedule, use_container_width=True)
    else:
        st.info("No schedule available. Please generate first.")

elif menu == "Reschedule":
    st.subheader("🔄 Reschedule")
    if not st.session_state.schedule.empty:
        patient_to_reschedule = st.selectbox("Select patient to reschedule:", st.session_state.schedule["Patient"])
        new_day = st.selectbox("Select new day:", DAYS)
        if st.button("Reschedule"):
            idx = st.session_state.schedule[st.session_state.schedule["Patient"] == patient_to_reschedule].index[0]
            new_date = datetime.today() + timedelta(days=DAYS.index(new_day))
            st.session_state.schedule.at[idx, "Day"] = new_day
            st.session_state.schedule.at[idx, "Date"] = new_date.strftime("%Y-%m-%d")
            st.success(f"🔄 {patient_to_reschedule} rescheduled to {new_day}")
    else:
        st.info("No schedule available to edit.")
