import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Dengue Expert System & Health Checker",
    page_icon="🩺",
    layout="centered",
)

# Custom styling
st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)

# Initialize step tracker in session state
if "step" not in st.session_state:
    st.session_state.step = 1


def classify_age_group(age: int) -> str:
    if age < 1:
        return "Infant (<12 months)"
    elif age <= 12:
        return "Pediatric (1 - 12 years)"
    elif age <= 60:
        return "Adolescent/Adult (13-60)"
    else:
        return "Elderly (>60 years)"


def classify_fever_status(max_temp_f: float, has_fever: bool) -> str:
    if not has_fever or max_temp_f < 100.4:
        return "No Fever / Defervescence (<100.4F / <38.0C)"
    elif max_temp_f <= 102.0:
        return "Moderate Fever (100.4 - 102.0F)"
    else:
        return "High Fever (>= 102.1F / >= 39.0C)"


def classify_fever_phase(days: int) -> str:
    if days <= 3:
        return "Febrile Phase (1 - 3 days)"
    elif days <= 7:
        return "Critical Phase (4 - 7 days)"
    else:
        return "Recovery Phase (>7 days)"


def classify_wbc(wbc: int) -> str:
    if wbc < 4000:
        return "Leukopenia (<4000 / uL)"
    elif wbc <= 11000:
        return "Normal (4000 - 11,000 /uL)"
    else:
        return "Leukocytosis (>11,000 / uL)"


def classify_platelet(platelet: int) -> str:
    if platelet < 50000:
        return "Severe Thrombocytopenia (<50000 / uL)"
    elif platelet <= 100000:
        return "Moderate Low / Warning (50,000 - 100,000 /uL)"
    elif platelet <= 150000:
        return "Low Normal (100,001-150,000 / uL)"
    else:
        return "Normal (>150,000 / uL)"


def evaluate_heuristics_and_triage(data: dict) -> dict:
    fired_rules = []
    notes = []

    early_nausea = data["early_nausea"] == "Yes"
    early_fatigue = data["early_fatigue"] == "Yes"
    early_appetite_loss = data["early_appetite_loss"] == "Yes"
    early_abdominal_pain = data["early_abdominal_pain"] == "Yes"
    early_bleeding = data["early_bleeding"] == "Yes"
    early_rash = data["early_rash"] == "Yes"
    early_chills = data["early_chills"] == "Yes"
    early_diarrhea = data["early_diarrhea"] == "Yes"

    household_exp = data["household_dengue_exposure_14d"] == "Yes"
    stagnant_water = data["stagnant_water"]

    fever_days = data["fever_days"]
    max_temp_f = data["max_temperature_f"]
    fever_bool = data["fever_bool"]

    headache_sev = data["headache_severity"]
    headache_bool = data["headache_bool"] or (headache_sev >= 4)

    retro_orbital = data["retro_orbital_pain"]
    muscle_pain = data["muscle_pain"]
    joint_pain = data["joint_pain"]
    muscle_bool = data["muscle_pain_bool"] or (muscle_pain >= 1)
    joint_bool = joint_pain >= 1

    vomiting_per_day = data["vomiting_per_day"]
    vomiting_bool = data["vomiting_bool"] or (vomiting_per_day > 0)
    rash_bool = early_rash or data["rash_bool"]

    has_labs = data["include_labs"]
    platelet = data["platelet_count"]
    wbc = data["wbc_count"]
    hct_status = data["haematocrit_hct"]

    # --- Dataset 1 & Added Rules (H1 - H15) ---
    if early_nausea and early_fatigue and early_appetite_loss:
        fired_rules.append("H1 / Added H1: Early Nausea + Early Fatigue + Early Appetite Loss -> Flag symptom pattern for dengue assessment.")
    if early_nausea and early_appetite_loss:
        fired_rules.append("H2 / Added H2: Early Nausea + Early Appetite Loss -> Consider both symptoms during assessment.")
    if early_nausea and early_fatigue:
        fired_rules.append("H3 / Added H3: Early Nausea + Early Fatigue -> Identify nausea and fatigue combination for assessment.")
    if household_exp and stagnant_water == "Yes":
        fired_rules.append("H4 / Added H4: Household Dengue Exposure (14d) + Stagnant Water -> Environmental and exposure risk factors identified.")
    if early_nausea and early_abdominal_pain:
        fired_rules.append("H5 / Added H5: Early Nausea + Early Abdominal Pain -> Flag symptom combination for further assessment.")
    if fever_days > 0 and max_temp_f is not None:
        fired_rules.append("H6 / Added H6: Fever Days > 0 and Max Temperature available -> Include fever duration and temperature in assessment.")
    if headache_sev > 0 and muscle_pain > 0 and joint_pain > 0:
        fired_rules.append("H7 / Added H7: Headache Severity, Muscle Pain, and Joint Pain recorded -> Include pain symptoms in evaluation.")
    if early_fatigue and early_appetite_loss:
        fired_rules.append("Added H8: Early Fatigue + Early Appetite Loss -> Consider combination during assessment.")
    if early_nausea and early_abdominal_pain and early_fatigue:
        fired_rules.append("Added H9: Early Nausea + Early Abdominal Pain + Early Fatigue -> Multiple early symptoms require further assessment.")
    if early_appetite_loss and early_abdominal_pain:
        fired_rules.append("Added H10: Early Appetite Loss + Early Abdominal Pain -> Consider both symptoms during assessment.")
    if household_exp:
        fired_rules.append("Added H11: Household Dengue Exposure within 14 Days -> Recent household exposure is a relevant risk factor.")
    if stagnant_water == "Yes":
        fired_rules.append("Added H12: Stagnant Water = Yes -> Possible mosquito breeding environment recorded as risk info.")
    if not early_nausea and not early_fatigue:
        fired_rules.append("Added H13: Early Nausea = No and Early Fatigue = No -> Absence of both symptoms recorded.")
    if not early_appetite_loss and not early_abdominal_pain:
        fired_rules.append("Added H14: Early Appetite Loss = No and Early Abdominal Pain = No -> Absence of both symptoms recorded.")
    if early_nausea and not early_fatigue:
        fired_rules.append("Added H15: Early Nausea = Yes and Early Fatigue = No -> Nausea without fatigue noted.")

    # --- Dataset 2 & Added Rules (H8-H14 / Added H16 - H30) ---
    if fever_bool and headache_bool and muscle_bool:
        fired_rules.append("H8 / Added H16: Fever + Headache + Muscle Pain -> Symptom pattern associated with positive dengue outcomes.")
    if fever_bool and headache_bool:
        fired_rules.append("H9 / Added H17: Fever + Headache -> Symptom combination associated with dengue assessment.")
    if fever_bool and muscle_bool:
        fired_rules.append("H10 / Added H18: Fever + Muscle Pain -> Flag patient for further clinical assessment.")
    if headache_bool and muscle_bool:
        fired_rules.append("H11 / Added H19: Headache + Muscle Pain -> Pain-related symptom combination identified.")
    if rash_bool and vomiting_bool:
        fired_rules.append("H12 / Added H20: Rash + Vomiting -> Flag patient based on observed symptom combination.")
    if has_labs and platelet is not None and wbc is not None:
        fired_rules.append("H13 / Added H21: Platelet Count and WBC available -> Include both blood test measurements in clinical assessment.")
    if fever_days > 0 and fever_bool:
        fired_rules.append("H14 / Added H22: Duration of Fever > 0 and Fever = True -> Consider duration of fever in evaluation.")
    if fever_bool and rash_bool:
        fired_rules.append("Added H23: Fever = True and Rash = True -> Fever and rash combination considered.")
    if fever_bool and vomiting_bool:
        fired_rules.append("Added H24: Fever = True and Vomiting = True -> Fever and vomiting considered in clinical assessment.")
    if headache_bool and joint_bool:
        fired_rules.append("Added H25: Headache = True and Joint Pain = True -> Pain-related symptom combination identified.")
    if muscle_bool and joint_bool:
        fired_rules.append("Added H26: Muscle Pain = True and Joint Pain = True -> Muscle and joint pain presence considered.")
    if not fever_bool and not headache_bool:
        fired_rules.append("Added H27: Fever = False and Headache = False -> Absence of both symptoms recorded.")
    if fever_bool and not headache_bool:
        fired_rules.append("Added H28: Fever = True and Headache = False -> Fever without headache considered.")
    if not fever_bool and muscle_bool:
        fired_rules.append("Added H29: Fever = False and Muscle Pain = True -> Muscle pain without fever considered.")
    if not rash_bool and not vomiting_bool:
        fired_rules.append("Added H30: Rash = False and Vomiting = False -> Absence of both symptoms recorded.")

    # --- Step 2 Warning Signs & High-Risk Triage ---
    persistent_vomiting = vomiting_per_day >= 3 or (data["vomiting_bool"] and vomiting_per_day == 0)
    persistent_diarrhea = early_diarrhea  # Flagged if present; persistent >=3/day is a warning sign
    warning_signs = []
    if persistent_vomiting:
        warning_signs.append("Persistent / Severe Vomiting (>=3/day or True)")
    if early_abdominal_pain:
        warning_signs.append("Early Abdominal Pain")
    if early_bleeding:
        warning_signs.append("Early Bleeding")
    if has_labs and platelet is not None and platelet <= 100000:
        warning_signs.append(f"Low Platelets ({platelet:,} /uL <= 100,000)")
    if has_labs and hct_status == "Significant Leakage (>=20% rise from baseline)":
        warning_signs.append("Significant HCT Leakage (>=20% rise)")

    high_risk_age = data["age"] < 1 or data["age"] > 60
    if high_risk_age:
        notes.append(f"High-risk age group ({classify_age_group(data['age'])}) requires closer clinical supervision.")

    # Triage & Diagnosis Determination
    severe_lab_or_bleed = early_bleeding or (
        has_labs and (
            (platelet is not None and platelet < 50000)
            or hct_status == "Significant Leakage (>=20% rise from baseline)"
        )
    )

    if severe_lab_or_bleed:
        triage = "Emergency Resuscitation / HDU / ICU"
        diagnosis = "Dengue Positive (High-Risk / Severe Warning)"
        advice = (
            "Urgent warning signs or severe hematological/bleeding indicators detected. "
            "Seek immediate emergency medical care at a hospital right away."
        )
    elif len(warning_signs) > 0 or high_risk_age:
        triage = "Hospital Admission & Daily Monitoring"
        diagnosis = "Dengue Positive (Probable / Warning Signs or High-Risk Group)"
        advice = (
            "Warning signs or high-risk demographic factors (infant <1 yr or elderly >60 yrs) are present. "
            "Hospital admission or strict daily monitoring with FBC/platelet and HCT checks is recommended."
        )
    else:
        positive_indicators = sum([
            fever_bool,
            headache_bool,
            muscle_bool,
            joint_bool,
            retro_orbital >= 4,
            rash_bool,
            early_nausea,
            early_fatigue,
            early_appetite_loss,
            household_exp,
            stagnant_water == "Yes",
        ])
        if positive_indicators >= 3 or (fever_bool and (headache_bool or muscle_bool or retro_orbital >= 4)):
            triage = "Outpatient Management & Home Care"
            diagnosis = "Dengue Positive (Probable - No Warning Signs)"
            advice = (
                "Symptoms align with probable dengue without immediate warning signs. "
                "Maintain oral hydration, rest, monitor temperature/fever phase (especially days 4–7), "
                "and return immediately if warning signs appear."
            )
        else:
            triage = "Outpatient Management & Home Care"
            diagnosis = "Dengue Negative (Low Clinical Suspicion)"
            advice = (
                "Few dengue-associated indicators are present. Continue standard rest, hydration, "
                "and symptom monitoring; consult a healthcare provider if new symptoms develop."
            )

    return {
        "diagnosis": diagnosis,
        "triage": triage,
        "advice": advice,
        "warning_signs": warning_signs,
        "notes": notes,
        "fired_rules": fired_rules,
    }


st.title("🩺 Dengue Expert System & Health Checker")
st.caption("Aligned with Step 1 (Facts & Heuristic Rules: Dataset 1 & Dataset 2) and Step 2 (Expert Triage Table)")

progress_val = min(st.session_state.step, 4) / 4.0
st.progress(progress_val)
st.write(f"**Step {min(st.session_state.step, 4)} of 4**")

# ==================== STEP 1: DEMOGRAPHICS & EXPOSURE ====================
if st.session_state.step == 1:
    st.subheader("👤 Step 1: Demographics & Exposure Factors")

    age = st.number_input(
        "Age (Years) [Dataset 1: 14–71 | Dataset 2: 1–87]",
        min_value=0,
        max_value=120,
        value=st.session_state.get("age", 25),
    )
    gender = st.selectbox(
        "Gender",
        options=["Male", "Female"],
        index=0 if st.session_state.get("gender", "Male") == "Male" else 1,
    )
    district = st.text_input(
        "District / Location",
        value=st.session_state.get("district", "Kuala Lumpur"),
    )
    area_type = st.selectbox(
        "Area Type (Dataset 1 & Step 2)",
        options=["Urban", "Semi-urban", "Rural"],
        index=["Urban", "Semi-urban", "Rural"].index(st.session_state.get("area_type", "Urban")),
    )
    ever_dengue = st.selectbox(
        "Ever Dengue (Previous Dengue Infection?)",
        options=["No", "Yes"],
        index=0 if st.session_state.get("ever_dengue", "No") == "No" else 1,
    )
    household_exp = st.selectbox(
        "Household Dengue Exposure within 14 Days?",
        options=["No", "Yes"],
        index=0 if st.session_state.get("household_exp", "No") == "No" else 1,
    )
    stagnant_water = st.selectbox(
        "Stagnant Water Present?",
        options=["No", "Yes", "Unknown"],
        index=["No", "Yes", "Unknown"].index(st.session_state.get("stagnant_water", "No")),
    )

    st.session_state.age = age
    st.session_state.gender = gender
    st.session_state.district = district
    st.session_state.area_type = area_type
    st.session_state.ever_dengue = ever_dengue
    st.session_state.household_exp = household_exp
    st.session_state.stagnant_water = stagnant_water

    st.markdown("---")
    if st.button("Next: Fever & Pain Symptoms ➡️"):
        st.session_state.step = 2
        st.rerun()

# ==================== STEP 2: FEVER & PAIN SYMPTOMS ====================
elif st.session_state.step == 2:
    st.subheader("🌡️ Step 2: Fever & Pain Symptoms")

    fever_bool = st.checkbox(
        "Fever Present (Clinical Fever = True/False)",
        value=st.session_state.get("fever_bool", True),
    )
    fever_days = st.number_input(
        "Fever Days / Duration of Fever (Days)",
        min_value=0,
        max_value=30,
        value=st.session_state.get("fever_days", 2),
    )
    max_temperature_f = st.number_input(
        "Maximum Temperature (°F)",
        min_value=95.0,
        max_value=110.0,
        step=0.1,
        value=st.session_state.get("max_temperature_f", 100.4),
    )

    headache_bool = st.checkbox(
        "Headache Present (Clinical Headache = True/False)",
        value=st.session_state.get("headache_bool", False),
    )
    headache_severity = st.slider(
        "Headache Severity (0–10)",
        min_value=0,
        max_value=10,
        value=st.session_state.get("headache_severity", 0),
    )
    retro_orbital_pain = st.slider(
        "Retro-orbital Pain (Pain Behind Eyes, 0–10)",
        min_value=0,
        max_value=10,
        value=st.session_state.get("retro_orbital_pain", 0),
    )
    muscle_pain_bool = st.checkbox(
        "Muscle Pain Present (Clinical Muscle_Pain = True/False)",
        value=st.session_state.get("muscle_pain_bool", False),
    )
    muscle_pain = st.slider(
        "Muscle Pain Severity (0–10)",
        min_value=0,
        max_value=10,
        value=st.session_state.get("muscle_pain", 0),
    )
    joint_pain = st.slider(
        "Joint Pain Severity (0–10)",
        min_value=0,
        max_value=10,
        value=st.session_state.get("joint_pain", 0),
    )

    st.session_state.fever_bool = fever_bool
    st.session_state.fever_days = fever_days
    st.session_state.max_temperature_f = max_temperature_f
    st.session_state.headache_bool = headache_bool
    st.session_state.headache_severity = headache_severity
    st.session_state.retro_orbital_pain = retro_orbital_pain
    st.session_state.muscle_pain_bool = muscle_pain_bool
    st.session_state.muscle_pain = muscle_pain
    st.session_state.joint_pain = joint_pain

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next: Other Symptoms & Labs ➡️"):
            st.session_state.step = 3
            st.rerun()

# ==================== STEP 3: OTHER SYMPTOMS & CLINICAL LABS ====================
elif st.session_state.step == 3:
    st.subheader("🔍 Step 3: Other Symptoms & Blood Test Results")

    col_a, col_b = st.columns(2)
    with col_a:
        early_nausea = st.selectbox("Early Nausea", ["No", "Yes"], index=0 if st.session_state.get("early_nausea", "No") == "No" else 1)
        early_fatigue = st.selectbox("Early Fatigue", ["No", "Yes"], index=0 if st.session_state.get("early_fatigue", "No") == "No" else 1)
        early_appetite_loss = st.selectbox("Early Appetite Loss", ["No", "Yes"], index=0 if st.session_state.get("early_appetite_loss", "No") == "No" else 1)
        early_abdominal_pain = st.selectbox("Early Abdominal Pain", ["No", "Yes"], index=0 if st.session_state.get("early_abdominal_pain", "No") == "No" else 1)
        early_bleeding = st.selectbox("Early Bleeding", ["No", "Yes"], index=0 if st.session_state.get("early_bleeding", "No") == "No" else 1)
    with col_b:
        early_rash = st.selectbox("Early Rash", ["No", "Yes"], index=0 if st.session_state.get("early_rash", "No") == "No" else 1)
        early_chills = st.selectbox("Early Chills", ["No", "Yes"], index=0 if st.session_state.get("early_chills", "No") == "No" else 1)
        early_diarrhea = st.selectbox("Early Diarrhea", ["No", "Yes"], index=0 if st.session_state.get("early_diarrhea", "No") == "No" else 1)
        rash_bool = st.checkbox("Clinical Rash (True/False)", value=st.session_state.get("rash_bool", False))
        vomiting_bool = st.checkbox("Clinical Vomiting (True/False)", value=st.session_state.get("vomiting_bool", False))

    vomiting_per_day = st.number_input(
        "Vomiting per Day (Episodes/Day)",
        min_value=0,
        max_value=20,
        value=st.session_state.get("vomiting_per_day", 0),
    )

    st.markdown("#### 🧪 Clinical Blood Test Results (Optional - Dataset 2 & Step 2)")
    include_labs = st.checkbox(
        "Include Platelet Count, WBC, and Haematocrit (HCT)",
        value=st.session_state.get("include_labs", False),
    )
    platelet_count = st.session_state.get("platelet_count", 180000)
    wbc_count = st.session_state.get("wbc_count", 6000)
    haematocrit_hct = st.session_state.get("haematocrit_hct", "Normal Baseline (<=40% female, <=46% male)")

    if include_labs:
        platelet_count = st.number_input(
            "Platelet Count (/uL)",
            min_value=1000,
            max_value=1000000,
            step=1000,
            value=platelet_count,
        )
        wbc_count = st.number_input(
            "WBC Count (/uL)",
            min_value=500,
            max_value=50000,
            step=100,
            value=wbc_count,
        )
        haematocrit_hct = st.selectbox(
            "Haematocrit (HCT) Status",
            options=[
                "Normal Baseline (<=40% female, <=46% male)",
                "Moderate Hemoconcentration (10 - 19% rise)",
                "Significant Leakage (>=20% rise from baseline)",
            ],
            index=0,
        )

    st.session_state.early_nausea = early_nausea
    st.session_state.early_fatigue = early_fatigue
    st.session_state.early_appetite_loss = early_appetite_loss
    st.session_state.early_abdominal_pain = early_abdominal_pain
    st.session_state.early_bleeding = early_bleeding
    st.session_state.early_rash = early_rash
    st.session_state.early_chills = early_chills
    st.session_state.early_diarrhea = early_diarrhea
    st.session_state.rash_bool = rash_bool
    st.session_state.vomiting_bool = vomiting_bool
    st.session_state.vomiting_per_day = vomiting_per_day
    st.session_state.include_labs = include_labs
    st.session_state.platelet_count = platelet_count
    st.session_state.wbc_count = wbc_count
    st.session_state.haematocrit_hct = haematocrit_hct

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("📊 Run Expert Evaluation", type="primary"):
            st.session_state.step = 4
            st.rerun()

# ==================== STEP 4: EVALUATION RESULTS ====================
elif st.session_state.step == 4:
    st.subheader("📋 Expert System Evaluation & Triage")

    payload = {
        "age": st.session_state.get("age", 25),
        "gender": st.session_state.get("gender", "Male"),
        "district": st.session_state.get("district", "Kuala Lumpur"),
        "area_type": st.session_state.get("area_type", "Urban"),
        "ever_dengue": st.session_state.get("ever_dengue", "No"),
        "household_dengue_exposure_14d": st.session_state.get("household_exp", "No"),
        "stagnant_water": st.session_state.get("stagnant_water", "No"),
        "fever_bool": st.session_state.get("fever_bool", True),
        "fever_days": st.session_state.get("fever_days", 2),
        "max_temperature_f": st.session_state.get("max_temperature_f", 100.4),
        "headache_bool": st.session_state.get("headache_bool", False),
        "headache_severity": st.session_state.get("headache_severity", 0),
        "retro_orbital_pain": st.session_state.get("retro_orbital_pain", 0),
        "muscle_pain_bool": st.session_state.get("muscle_pain_bool", False),
        "muscle_pain": st.session_state.get("muscle_pain", 0),
        "joint_pain": st.session_state.get("joint_pain", 0),
        "early_nausea": st.session_state.get("early_nausea", "No"),
        "early_fatigue": st.session_state.get("early_fatigue", "No"),
        "early_appetite_loss": st.session_state.get("early_appetite_loss", "No"),
        "early_abdominal_pain": st.session_state.get("early_abdominal_pain", "No"),
        "early_bleeding": st.session_state.get("early_bleeding", "No"),
        "early_rash": st.session_state.get("early_rash", "No"),
        "early_chills": st.session_state.get("early_chills", "No"),
        "early_diarrhea": st.session_state.get("early_diarrhea", "No"),
        "rash_bool": st.session_state.get("rash_bool", False),
        "vomiting_bool": st.session_state.get("vomiting_bool", False),
        "vomiting_per_day": st.session_state.get("vomiting_per_day", 0),
        "include_labs": st.session_state.get("include_labs", False),
        "platelet_count": st.session_state.get("platelet_count", 180000),
        "wbc_count": st.session_state.get("wbc_count", 6000),
        "haematocrit_hct": st.session_state.get("haematocrit_hct", "Normal Baseline (<=40% female, <=46% male)"),
    }

    result = evaluate_heuristics_and_triage(payload)

    st.info(f"**Target Class Output:** {result['diagnosis']}")
    st.warning(f"**Triage Recommendation:** {result['triage']}")
    st.write(result["advice"])

    # Derived Step 2 Categories Summary
    summary_rows = [
        {"Variable": "age_group", "Derived Category": classify_age_group(payload["age"])},
        {"Variable": "fever_status / max_temperature_f", "Derived Category": classify_fever_status(payload["max_temperature_f"], payload["fever_bool"])},
        {"Variable": "fever_duration", "Derived Category": classify_fever_phase(payload["fever_days"])},
    ]
    if payload["include_labs"]:
        summary_rows.append({"Variable": "wbc_count", "Derived Category": classify_wbc(payload["wbc_count"])})
        summary_rows.append({"Variable": "platelet_count", "Derived Category": classify_platelet(payload["platelet_count"])})
        summary_rows.append({"Variable": "haematocrit_hct", "Derived Category": payload["haematocrit_hct"]})

    st.markdown("#### 📌 Derived Step 2 Classifications")
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    if result["warning_signs"]:
        st.error("**Warning Signs Present:** " + ", ".join(result["warning_signs"]))
    for note in result["notes"]:
        st.caption(f"ℹ️ {note}")

    with st.expander(f"Triggered Heuristic Rules ({len(result['fired_rules'])})"):
        for r in result["fired_rules"]:
            st.write(f"- {r}")

    st.markdown("---")
    if st.button("🔄 Start Over"):
        st.session_state.step = 1
        st.rerun()