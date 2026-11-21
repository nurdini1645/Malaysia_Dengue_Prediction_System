import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="Malaysia Dengue Health Checker", page_icon="🇲🇾", layout="centered")

# Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #dc3545;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        height: 45px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #b02a37;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Load trained model
@st.cache_resource
def load_model():
    return joblib.load('dengue_model.pkl')

model = load_model()

# Initialize step tracker in session state
if 'step' not in st.session_state:
    st.session_state.step = 1

st.title("🇲🇾 Malaysian Dengue Health Checker")

# Progress indicator
progress_val = st.session_state.step / 5 if st.session_state.step <= 4 else 1.0
st.progress(progress_val)
st.write(f"**Step {min(st.session_state.step, 4)} of 4**")

def get_val(choice):
    return 1 if choice == "Yes" else 2

# ==================== STEP 1: PERSONAL INFORMATION ====================
if st.session_state.step == 1:
    st.subheader("👤 Step 1: Your Information")
    st.markdown("Let's start with a few basic details about you.")
    
    patient_age = st.number_input("How old are you? (Tahun)", min_value=1, max_value=120, value=st.session_state.get('patient_age', 25))
    sex = st.selectbox("Gender / Jantina", options=[0, 1], format_func=lambda x: "Female 👩" if x == 0 else "Male 👨", index=st.session_state.get('sex', 0))
    
    malaysian_states = [
        "W.P. Kuala Lumpur", "Selangor", "Johor", "Pulau Pinang", "Perak", 
        "Kedah", "Kelantan", "Terengganu", "Pahang", "Negeri Sembilan", 
        "Melaka", "Perlis", "Sabah", "Sarawak", "W.P. Putrajaya", "W.P. Labuan"
    ]
    selected_state = st.selectbox("Which State (Negeri) are you currently in?", options=malaysian_states)
    
    st.session_state.patient_age = patient_age
    st.session_state.sex = sex
    st.session_state.state_code = malaysian_states.index(selected_state) + 1
    st.session_state.race = 1

    st.markdown("---")
    if st.button("Next: Common Symptoms ➡️"):
        st.session_state.step = 2
        st.rerun()

# ==================== STEP 2: COMMON SYMPTOMS ====================
elif st.session_state.step == 2:
    st.subheader("🌡️ Step 2: Common Symptoms")
    st.markdown("Are you experiencing any of these primary signs?")
    
    fever_c = st.selectbox("Are you having a High Fever? (Demam panas)", options=["No", "Yes"], index=0 if st.session_state.get('fever', 2)==2 else 1)
    headache_c = st.selectbox("Are you experiencing Headaches? (Sakit kepala)", options=["No", "Yes"], index=0 if st.session_state.get('headache', 2)==2 else 1)
    myalgia_c = st.selectbox("Are you feeling Muscle / Body Pains? (Sakit otot/badan)", options=["No", "Yes"], index=0 if st.session_state.get('myalgia', 2)==2 else 1)
    day_count = st.number_input("How many days have you had these symptoms?", min_value=1, max_value=30, value=st.session_state.get('day_count', 2))
    
    st.session_state.fever = get_val(fever_c)
    st.session_state.headache = get_val(headache_c)
    st.session_state.myalgia = get_val(myalgia_c)
    st.session_state.day_count = day_count

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next: Detailed Symptoms ➡️"):
            st.session_state.step = 3
            st.rerun()

# ==================== STEP 3: DETAILED SYMPTOMS ====================
elif st.session_state.step == 3:
    st.subheader("🔍 Step 3: Detailed Symptoms")
    st.markdown("Please check any other specific signs or discomforts you might feel:")
    
    rash_c = st.selectbox("Skin Rash? (Ruam pada kulit)", options=["No", "Yes"])
    vomiting_c = st.selectbox("Vomiting? (Muntah)", options=["No", "Yes"])
    nausea_c = st.selectbox("Nausea / Queasiness? (Rasa loya)", options=["No", "Yes"])
    back_pain_c = st.selectbox("Back Pain? (Sakit belakang)", options=["No", "Yes"])
    conjunctivitis_c = st.selectbox("Red or Watery Eyes?", options=["No", "Yes"])
    arthritis_c = st.selectbox("Joint Stiffness / Arthritis?", options=["No", "Yes"])
    artralgia_c = st.selectbox("Joint Pains? (Sakit sendi)", options=["No", "Yes"])
    petechiae_c = st.selectbox("Tiny Red Spots on Skin (Petechiae)?", options=["No", "Yes"])
    tourniquet_test_c = st.selectbox("Tourniquet Test Positive?", options=["No", "Yes"])
    retroorbital_pain_c = st.selectbox("Pain Behind Eyes?", options=["No", "Yes"])
    
    st.session_state.rash = get_val(rash_c)
    st.session_state.vomiting = get_val(vomiting_c)
    st.session_state.nausea = get_val(nausea_c)
    st.session_state.back_pain = get_val(back_pain_c)
    st.session_state.conjunctivitis = get_val(conjunctivitis_c)
    st.session_state.arthritis = get_val(arthritis_c)
    st.session_state.artralgia = get_val(artralgia_c)
    st.session_state.petechiae = get_val(petechiae_c)
    st.session_state.tourniquet_test = get_val(tourniquet_test_c)
    st.session_state.retroorbital_pain = get_val(retroorbital_pain_c)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next: Medical History ➡️"):
            st.session_state.step = 4
            st.rerun()

# ==================== STEP 4: MEDICAL HISTORY ====================
elif st.session_state.step == 4:
    st.subheader("📋 Step 4: Medical History & Comorbidities")
    st.markdown("Do you have any pre-existing health conditions?")
    
    diabetes_c = st.selectbox("Diabetes? (Kencing manis)", options=["No", "Yes"])
    hypertension_c = st.selectbox("High Blood Pressure? (Darah tinggi)", options=["No", "Yes"])
    hematological_c = st.selectbox("Blood Disorders?", options=["No", "Yes"])
    liver_c = st.selectbox("Liver Condition?", options=["No", "Yes"])
    kidney_c = st.selectbox("Kidney Condition?", options=["No", "Yes"])
    peptic_c = st.selectbox("Acidity / Stomach Ulcer?", options=["No", "Yes"])
    autoimmune_c = st.selectbox("Autoimmune Condition?", options=["No", "Yes"])
    
    st.session_state.diabetes = get_val(diabetes_c)
    st.session_state.hypertension = get_val(hypertension_c)
    st.session_state.hematological = get_val(hematological_c)
    st.session_state.liver = get_val(liver_c)
    st.session_state.kidney = get_val(kidney_c)
    st.session_state.peptic = get_val(peptic_c)
    st.session_state.autoimmune = get_val(autoimmune_c)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🔍 Check My Dengue Risk Now", type="primary"):
            st.session_state.step = 5
            st.rerun()

# ==================== STEP 5: RESULTS ====================
elif st.session_state.step == 5:
    st.subheader("📊 Your Health Evaluation Results")
    
    input_data = pd.DataFrame([[
        st.session_state.get('sex', 0),
        st.session_state.get('race', 1),
        st.session_state.get('state_code', 1),
        st.session_state.get('fever', 2),
        st.session_state.get('myalgia', 2),
        st.session_state.get('headache', 2),
        st.session_state.get('rash', 2),
        st.session_state.get('vomiting', 2),
        st.session_state.get('nausea', 2),
        st.session_state.get('back_pain', 2),
        st.session_state.get('conjunctivitis', 2),
        st.session_state.get('arthritis', 2),
        st.session_state.get('artralgia', 2),
        st.session_state.get('petechiae', 2),
        st.session_state.get('tourniquet_test', 2),
        st.session_state.get('retroorbital_pain', 2),
        st.session_state.get('diabetes', 2),
        st.session_state.get('hematological', 2),
        st.session_state.get('liver', 2),
        st.session_state.get('kidney', 2),
        st.session_state.get('hypertension', 2),
        st.session_state.get('peptic', 2),
        st.session_state.get('autoimmune', 2),
        st.session_state.get('day_count', 2),
        st.session_state.get('patient_age', 25)
    ]], columns=[
        'Sex', 'Race', 'Residence_Area', 'Fever', 'Myalgia', 'Headache',
        'Rash', 'Vomiting', 'Nausea', 'Back_Pain', 'Conjunctivitis', 'Arthritis',
        'Artralgia', 'Petechiae', 'Tourniquet_Test', 'Retroorbital_Pain', 'Diabetes',
        'Hematological_Disease', 'Liver_Disease', 'Kidney_Disease', 'Hypertension',
        'Peptic_Acid_Disease', 'Auto_Immune_Disease', 'Day_Count_of_Symptoms', 'Patient_Age_Years'
    ])
    
    try:
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_data)[0][1]
        else:
            proba = float(model.predict(input_data)[0])
            
        # Count how many symptoms the user answered "Yes" to (where value == 1)
        symptom_flags = [
            st.session_state.get('fever'), st.session_state.get('headache'), 
            st.session_state.get('myalgia'), st.session_state.get('rash'), 
            st.session_state.get('vomiting'), st.session_state.get('nausea'), 
            st.session_state.get('back_pain'), st.session_state.get('conjunctivitis'), 
            st.session_state.get('arthritis'), st.session_state.get('artralgia'), 
            st.session_state.get('petechiae'), st.session_state.get('tourniquet_test'), 
            st.session_state.get('retroorbital_pain')
        ]
        yes_count = symptom_flags.count(1)

        # Smart Clinical Override: If fever is present and multiple critical symptoms are checked, elevate risk accordingly
        if st.session_state.get('fever') == 1 and yes_count >= 8:
            risk_level = "Critical"
        elif proba >= 0.6 or (st.session_state.get('fever') == 1 and yes_count >= 5):
            risk_level = "High"
        elif proba >= 0.3 or (st.session_state.get('fever') == 1 and yes_count >= 2):
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        # Display appropriate risk message
        if risk_level == "Low":
            st.success("🟢 **Low Risk (Risiko Rendah)**\n\nYour symptoms currently show a low probability of dengue. Make sure to drink plenty of water (*banyakkan minum air suam*), get enough rest, and monitor your temperature.")
        elif risk_level == "Moderate":
            st.warning("🟡 **Moderate Risk (Risiko Sederhana)**\n\nYou are showing some symptoms associated with viral infections. Please monitor your condition closely. If fever persists for more than 2 days, kindly visit the nearest *Klinik Kesihatan* for a blood test (*NS1/IPD test*).")
        elif risk_level == "High":
            st.error("🟠 **High Risk (Risiko Tinggi)**\n\nYour profile indicates a strong likelihood of dengue risk. Please do not wait—go to the nearest clinic or hospital immediately for a proper medical examination and platelet check.")
        else:
            st.error("🔴 **Critical / Severe Risk (Risiko Kritis)**\n\n⚠️ **Urgent Warning:** You have reported a high fever alongside multiple severe warning signs. Please seek emergency medical care at a hospital right away!")
            
    except Exception as e:
        st.error(f"An error occurred during evaluation: {e}")
        
    st.markdown("---")
    if st.button("🔄 Start Over / Check Again"):
        st.session_state.step = 1
        st.rerun()