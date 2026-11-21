import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Dengue Expert System & Health Checker | Sistem Pemeriksaan Denggi",
    page_icon="🏥",
    layout="centered",
)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

# Hospital-grade custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f8fb;
    }
    .hospital-header {
        background: linear-gradient(135deg, #005b96 0%, #008080 100%);
        color: white;
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 4px 10px rgba(0, 91, 150, 0.15);
    }
    .hospital-header h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
    }
    .hospital-header p {
        margin: 6px 0 0 0;
        font-size: 14px;
        opacity: 0.95;
    }
    .step-card {
        background-color: #ffffff;
        padding: 16px 20px;
        border-left: 5px solid #008080;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .triage-red {
        background-color: #fdecea;
        border-left: 6px solid #d32f2f;
        color: #7f1d1d;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .triage-orange {
        background-color: #fff4e5;
        border-left: 6px solid #ed6c02;
        color: #7c2d12;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .triage-yellow {
        background-color: #fefce8;
        border-left: 6px solid #eab308;
        color: #713f12;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .triage-green {
        background-color: #ecfdf5;
        border-left: 6px solid #10b981;
        color: #064e3b;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .help-box {
        background-color: #ffffff;
        border: 2px solid #d32f2f;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 14px;
        margin-bottom: 16px;
    }
    .stButton>button {
        background-color: #006680;
        color: white;
        font-size: 16px;
        font-weight: 600;
        border-radius: 8px;
        height: 46px;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004c60;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== BILINGUAL DICTIONARY ====================
TEXT = {
    "EN": {
        "title": "🏥 Dengue Health Checker & Hospital Triage",
        "subtitle": "Easy self-check tool to understand your symptoms and know when to see a doctor.",
        "step_label": "Step {step} of 4",
        "step1_title": "👤 Step 1: Basic Details & Surroundings",
        "step1_desc": "Tell us a little about yourself and your living environment.",
        "age": "Age in Years (Enter 0 for babies under 1 year old)",
        "gender": "Gender",
        "gender_opts": ["Male", "Female"],
        "district": "District / Area Name (e.g., Petaling Jaya, Cheras, Shah Alam)",
        "area_type": "Type of Neighbourhood",
        "area_opts": ["Urban (City / Town)", "Semi-urban (Suburb)", "Rural (Village / Kampung)"],
        "ever_dengue": "Have you ever had dengue fever before?",
        "household_exp": "Has anyone in your house or next door had dengue in the last 14 days?",
        "stagnant_water": "Is there stagnant (still) water near your home (flower pots, drains, containers)?",
        "yes_no": ["No", "Yes"],
        "yes_no_unk": ["No", "Yes", "Not Sure"],
        "next_step2": "Next: Fever & Body Aches ➡️",
        "step2_title": "🌡️ Step 2: Fever & Body Aches",
        "step2_desc": "Check the symptoms you are currently feeling.",
        "fever_bool": "Do you have a fever or feel hot?",
        "fever_days": "How many days have you had a fever? (Enter 0 if no fever)",
        "max_temp": "Highest Body Temperature in °F (Normal is ~98.6°F, Fever is 100.4°F+. Enter 0 if not measured)",
        "headache_bool": "Do you have a headache?",
        "headache_sev": "How bad is your headache? (0 = No pain, 10 = Worst pain)",
        "retro_pain": "Pain behind your eyes, especially when moving them (0 = None, 10 = Very painful)",
        "muscle_bool": "Do you have muscle aches or body pain?",
        "muscle_sev": "How bad is your muscle pain? (0 = None, 10 = Very painful)",
        "joint_sev": "How bad is your joint / bone pain? (0 = None, 10 = Very painful)",
        "back": "⬅️ Back",
        "next_step3": "Next: Stomach, Skin & Blood Tests ➡️",
        "step3_title": "🔍 Step 3: Other Symptoms & Blood Test (Optional)",
        "step3_desc": "Select any other symptoms you noticed in the past few days.",
        "nausea": "Feeling sick / wanting to vomit (Nausea)",
        "fatigue": "Extreme tiredness or weakness (Fatigue)",
        "appetite": "Loss of appetite (Not wanting to eat/drink)",
        "abdominal": "⚠️ Stomach or tummy pain (Abdominal pain)",
        "bleeding": "⚠️ Any bleeding (bleeding gums, nosebleed, red spots, or dark stool)",
        "rash": "Skin rash or red patches",
        "chills": "Shivering or feeling cold (Chills)",
        "diarrhea": "Loose watery stools (Diarrhea)",
        "rash_bool": "Doctor or family noticed a dengue-like skin rash",
        "vomit_bool": "Have you been vomiting?",
        "vomit_day": "How many times did you vomit in the last 24 hours? (Enter 0 if none)",
        "lab_header": "🧪 Blood Test Results (Optional — Only if you already visited a clinic)",
        "include_labs": "I have my blood test (FBC) results to enter",
        "platelet": "Platelet Count (/uL) (Normal: 150,000 – 450,000 | Enter 0 if unknown)",
        "wbc": "White Blood Cell / WBC Count (/uL) (Normal: 4,000 – 11,000 | Enter 0 if unknown)",
        "hct": "Haematocrit (HCT) Blood Thickness Status",
        "hct_opts": [
            "Normal Baseline (<=40% female, <=46% male)",
            "Slightly Thick / Moderate Rise (10% - 19% rise)",
            "⚠️ Very Thick Blood / Significant Leakage (>=20% rise)",
        ],
        "run_eval": "🩺 Check My Health Result",
        "step4_title": "📋 Your Dengue Health Assessment & Next Steps",
        "result_label": "Assessment Result",
        "triage_label": "Recommended Action",
        "warning_header": "⚠️ Important Warning Signs Detected:",
        "help_title": "🚑 Where to Get Immediate Medical Help (Malaysia)",
        "help_body": """
        <ul>
            <li><b>🚨 Emergency Ambulance (24 Hours):</b> Call <b>999</b> immediately if there is bleeding, severe tummy pain, constant vomiting, or drowsiness.</li>
            <li><b>🏥 Nearest Government Hospital Emergency Department (Jabatan Kecemasan & Trauma):</b> Go straight to the Red/Yellow Zone (e.g., Hospital Kuala Lumpur, Hospital Putrajaya, Hospital Sungai Buloh, Hospital Sultanah Aminah, or your nearest state/district hospital).</li>
            <li><b>🩺 Klinik Kesihatan (KKM Health Clinic):</b> Walk in immediately and inform the triage nurse: <i>"Suspected Dengue with Warning Signs"</i> for urgent blood tests (FBC & Dengue NS1/IgM/IgG).</li>
            <li><b>📞 KKM CPRC Hotline (Dengue & Infectious Disease Info):</b> <b>03-8881 0200 / 03-8881 0600</b></li>
        </ul>
        """,
        "summary_header": "📌 Easy Health Summary",
        "col_item": "Health Check Item",
        "col_status": "Your Status",
        "rules_expander": "🔬 View Clinical Rules Checked ({count} rules matched)",
        "start_over": "🔄 Check Another Person / Start Over",
        "disclaimer": "⚕️ Medical Note: This tool provides educational guidance based on clinical dengue guidelines and does not replace a doctor's physical examination or blood test.",
    },
    "MS": {
        "title": "🏥 Pemeriksa Kesihatan & Saringan Denggi",
        "subtitle": "Alat saringan mudah untuk memahami gejala anda dan tahu bila perlu berjumpa doktor.",
        "step_label": "Langkah {step} daripada 4",
        "step1_title": "👤 Langkah 1: Maklumat Asas & Persekitaran",
        "step1_desc": "Beritahu sedikit tentang diri anda dan keadaan persekitaran rumah.",
        "age": "Umur dalam Tahun (Masukkan 0 untuk bayi bawah 1 tahun)",
        "gender": "Jantina",
        "gender_opts": ["Lelaki", "Perempuan"],
        "district": "Daerah / Nama Kawasan (cth: Petaling Jaya, Cheras, Shah Alam)",
        "area_type": "Jenis Kawasan Kediaman",
        "area_opts": ["Bandar (Urban)", "Pinggir Bandar (Semi-urban)", "Luar Bandar / Kampung (Rural)"],
        "ever_dengue": "Pernahkah anda menghidap demam denggi sebelum ini?",
        "household_exp": "Adakah ahli keluarga serumah atau jiran terdekat menghidap denggi dalam 14 hari lepas?",
        "stagnant_water": "Adakah terdapat air bertakung berhampiran rumah (pasu bunga, longkang, bekas terbiar)?",
        "yes_no": ["Tidak", "Ya"],
        "yes_no_unk": ["Tidak", "Ya", "Tidak Pasti"],
        "next_step2": "Seterusnya: Demam & Sakit Badan ➡️",
        "step2_title": "🌡️ Langkah 2: Demam & Sakit Badan",
        "step2_desc": "Tandakan gejala yang sedang anda alami sekarang.",
        "fever_bool": "Adakah anda mengalami demam atau badan terasa panas?",
        "fever_days": "Sudah berapa hari anda demam? (Masukkan 0 jika tiada demam)",
        "max_temp": "Suhu Badan Tertinggi dalam °F (Normal ~98.6°F, Demam 100.4°F+. Masukkan 0 jika tidak disukat)",
        "headache_bool": "Adakah anda mengalami sakit kepala?",
        "headache_sev": "Tahap kesakitan kepala anda (0 = Tiada sakit, 10 = Sangat sakit)",
        "retro_pain": "Sakit di belakang biji mata, terutama apabila menggerakkan mata (0 = Tiada, 10 = Sangat sakit)",
        "muscle_bool": "Adakah anda mengalami sakit otot atau lenguh-lenguh badan?",
        "muscle_sev": "Tahap sakit otot anda (0 = Tiada, 10 = Sangat sakit)",
        "joint_sev": "Tahap sakit sendi atau tulang anda (0 = Tiada, 10 = Sangat sakit)",
        "back": "⬅️ Kembali",
        "next_step3": "Seterusnya: Perut, Kulit & Ujian Darah ➡️",
        "step3_title": "🔍 Langkah 3: Gejala Lain & Ujian Darah (Pilihan)",
        "step3_desc": "Pilih gejala lain yang anda perasan sejak beberapa hari lepas.",
        "nausea": "Rasa loya atau mual (Nausea)",
        "fatigue": "Terlalu letih atau tidak bermaya (Fatigue)",
        "appetite": "Hilang selera makan atau minum",
        "abdominal": "⚠️ Sakit perut atau memulas (Abdominal pain)",
        "bleeding": "⚠️ Sebarang pendarahan (gusi berdarah, hidung berdarah, bintik merah, atau najis hitam)",
        "rash": "Ruam kulit atau tompok merah",
        "chills": "Menggigil atau berasa sejuk (Chills)",
        "diarrhea": "Cirit-birit / najis cair",
        "rash_bool": "Doktor atau keluarga perasan ruam denggi pada kulit",
        "vomit_bool": "Adakah anda muntah-muntah?",
        "vomit_day": "Berapa kali anda muntah dalam tempoh 24 jam lepas? (Masukkan 0 jika tiada)",
        "lab_header": "🧪 Keputusan Ujian Darah (Pilihan — Jika anda sudah ke klinik)",
        "include_labs": "Saya ada keputusan ujian darah (FBC) untuk dimasukkan",
        "platelet": "Bacaan Platelet (/uL) (Normal: 150,000 – 450,000 | Masukkan 0 jika tidak tahu)",
        "wbc": "Bacaan Sel Darah Putih / WBC (/uL) (Normal: 4,000 – 11,000 | Masukkan 0 jika tidak tahu)",
        "hct": "Status Kepekatan Darah / Haematocrit (HCT)",
        "hct_opts": [
            "Paras Normal (<=40% wanita, <=46% lelaki)",
            "Sedikit Pekat / Peningkatan Sederhana (naik 10% - 19%)",
            "⚠️ Darah Sangat Pekat / Kebocoran Plasma Ketara (naik >=20%)",
        ],
        "run_eval": "🩺 Semak Keputusan Kesihatan Saya",
        "step4_title": "📋 Keputusan Saringan Denggi & Langkah Seterusnya",
        "result_label": "Keputusan Saringan",
        "triage_label": "Tindakan Disyorkan",
        "warning_header": "⚠️ Tanda-Tanda Amaran Penting Dikesan:",
        "help_title": "🚑 Di Mana Untuk Mendapatkan Bantuan Segera (Malaysia)",
        "help_body": """
        <ul>
            <li><b>🚨 Ambulans Kecemasan (24 Jam):</b> Hubungi <b>999</b> dengan segera jika terdapat pendarahan, sakit perut teruk, muntah berterusan, atau terlalu lemah/mengantuk.</li>
            <li><b>🏥 Jabatan Kecemasan & Trauma Hospital Kerajaan Terdekat:</b> Terus ke Zon Merah/Kuning (cth: Hospital Kuala Lumpur, Hospital Putrajaya, Hospital Sungai Buloh, Hospital Sultanah Aminah, atau hospital daerah/negeri terdekat).</li>
            <li><b>🩺 Klinik Kesihatan (KKM):</b> Hadir terus dan maklumkan kepada jururawat saringan: <i>"Disyaki Denggi dengan Tanda Amaran"</i> untuk ujian darah segera (FBC & Denggi NS1/IgM/IgG).</li>
            <li><b>📞 Talian CPRC KKM (Info Denggi & Penyakit Berjangkit):</b> <b>03-8881 0200 / 03-8881 0600</b></li>
        </ul>
        """,
        "summary_header": "📌 Ringkasan Kesihatan Anda",
        "col_item": "Perkara Diperiksa",
        "col_status": "Status Anda",
        "rules_expander": "🔬 Lihat Peraturan Klinikal Yang Sepadan ({count} peraturan aktif)",
        "start_over": "🔄 Semak Individu Lain / Mula Semula",
        "disclaimer": "⚕️ Nota Perubatan: Alat ini memberi panduan pendidikan berdasarkan garis panduan klinikal denggi dan tidak menggantikan pemeriksaan doktor atau ujian darah.",
    },
}

lang = st.session_state.lang
t = TEXT[lang]

# ==================== CLASSIFICATION HELPERS ====================
def classify_age_group(age: int, lang: str) -> str:
    if age < 1:
        return "Infant (<12 months) — High Risk" if lang == "EN" else "Bayi (<12 bulan) — Risiko Tinggi"
    elif age <= 12:
        return "Child (1 – 12 years)" if lang == "EN" else "Kanak-kanak (1 – 12 tahun)"
    elif age <= 60:
        return "Teen / Adult (13 – 60 years)" if lang == "EN" else "Remaja / Dewasa (13 – 60 tahun)"
    else:
        return "Senior / Elderly (>60 years) — High Risk" if lang == "EN" else "Warga Emas (>60 tahun) — Risiko Tinggi"


def classify_fever_status(max_temp_f: float, has_fever: bool, lang: str) -> str:
    if not has_fever or max_temp_f == 0.0 or max_temp_f < 100.4:
        return "No High Fever (<100.4°F / <38.0°C)" if lang == "EN" else "Tiada Demam Tinggi (<100.4°F / <38.0°C)"
    elif max_temp_f <= 102.0:
        return "Moderate Fever (100.4 – 102.0°F)" if lang == "EN" else "Demam Sederhana (100.4 – 102.0°F)"
    else:
        return "High Fever (≥102.1°F / ≥39.0°C)" if lang == "EN" else "Demam Panas Tinggi (≥102.1°F / ≥39.0°C)"


def classify_fever_phase(days: int, lang: str) -> str:
    if days == 0:
        return "No Fever Days Recorded (0 days)" if lang == "EN" else "Tiada Hari Demam Direkodkan (0 hari)"
    elif days <= 3:
        return "Early Fever Phase (Days 1–3)" if lang == "EN" else "Fasa Demam Awal (Hari 1–3)"
    elif days <= 7:
        return "⚠️ Critical Watch Phase (Days 4–7)" if lang == "EN" else "⚠️ Fasa Kritikal Perlu Dipantau (Hari 4–7)"
    else:
        return "Recovery Phase (>7 days)" if lang == "EN" else "Fasa Pemulihan (>7 hari)"


def classify_wbc(wbc: int, lang: str) -> str:
    if wbc == 0:
        return "Not Entered (0)" if lang == "EN" else "Tidak Dimasukkan (0)"
    elif wbc < 4000:
        return "Low White Blood Cells / Leukopenia (<4,000 /uL)" if lang == "EN" else "Sel Darah Putih Rendah / Leukopenia (<4,000 /uL)"
    elif wbc <= 11000:
        return "Normal (4,000 – 11,000 /uL)" if lang == "EN" else "Normal (4,000 – 11,000 /uL)"
    else:
        return "High White Blood Cells (>11,000 /uL)" if lang == "EN" else "Sel Darah Putih Tinggi (>11,000 /uL)"


def classify_platelet(platelet: int, lang: str) -> str:
    if platelet == 0:
        return "Not Entered (0)" if lang == "EN" else "Tidak Dimasukkan (0)"
    elif platelet < 50000:
        return "🚨 Dangerously Low Platelets (<50,000 /uL)" if lang == "EN" else "🚨 Platelet Sangat Rendah (<50,000 /uL)"
    elif platelet <= 100000:
        return "⚠️ Warning: Low Platelets (50,000 – 100,000 /uL)" if lang == "EN" else "⚠️ Amaran: Platelet Rendah (50,000 – 100,000 /uL)"
    elif platelet <= 150000:
        return "Slightly Low / Borderline (100,001 – 150,000 /uL)" if lang == "EN" else "Sedikit Rendah (100,001 – 150,000 /uL)"
    else:
        return "Normal (>150,000 /uL)" if lang == "EN" else "Normal (>150,000 /uL)"


# ==================== EVALUATION ENGINE ====================
def evaluate_heuristics_and_triage(data: dict, lang: str) -> dict:
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
    hct_idx = data["haematocrit_hct_idx"]

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
    if fever_days > 0 and max_temp_f > 0:
        fired_rules.append("H6 / Added H6: Fever Days > 0 and Max Temperature recorded -> Include fever duration and temperature in assessment.")
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
    if has_labs and platelet > 0 and wbc > 0:
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
    if fever_bool and not muscle_bool:
        fired_rules.append("Added H29: Fever = True and Muscle Pain = False -> Muscle pain without fever considered.")
    if not rash_bool and not vomiting_bool:
        fired_rules.append("Added H30: Rash = False and Vomiting = False -> Absence of both symptoms recorded.")

    # --- Warning Signs & High-Risk Triage ---
    persistent_vomiting = vomiting_per_day >= 3 or (data["vomiting_bool"] and vomiting_per_day == 0)
    warning_signs = []
    if persistent_vomiting:
        warning_signs.append(
            "Frequent Vomiting (3 or more times/day)" if lang == "EN" else "Muntah Berterusan (3 kali atau lebih sehari)"
        )
    if early_abdominal_pain:
        warning_signs.append("Stomach / Tummy Pain" if lang == "EN" else "Sakit Perut")
    if early_bleeding:
        warning_signs.append("Bleeding (Gums, Nose, or Skin)" if lang == "EN" else "Pendarahan (Gusi, Hidung, atau Kulit)")
    if has_labs and platelet > 0 and platelet <= 100000:
        warning_signs.append(
            f"Low Platelets ({platelet:,} /uL)" if lang == "EN" else f"Platelet Rendah ({platelet:,} /uL)"
        )
    if has_labs and hct_idx == 2:
        warning_signs.append("Thickened Blood / HCT Leakage (>=20%)" if lang == "EN" else "Darah Pekat / Kebocoran HCT (>=20%)")

    high_risk_age = data["age"] < 1 or data["age"] > 60
    if high_risk_age:
        notes.append(
            "Babies under 1 year and adults over 60 need closer doctor supervision."
            if lang == "EN"
            else "Bayi bawah 1 tahun dan warga emas melebihi 60 tahun memerlukan pemantauan doktor yang lebih rapi."
        )

    severe_lab_or_bleed = early_bleeding or (
        has_labs and ((platelet > 0 and platelet < 50000) or hct_idx == 2)
    )

    is_high_risk = False

    if severe_lab_or_bleed:
        is_high_risk = True
        color_class = "triage-red"
        if lang == "EN":
            diagnosis = "🚨 HIGH RISK: Possible Severe Dengue Warning"
            triage = "Go to Hospital Emergency Department Immediately (Red/Yellow Zone)"
            advice = (
                "You have serious warning signs (such as bleeding, very low platelets, or thickened blood). "
                "Do NOT wait at home. Go to the nearest Hospital Emergency Department right away or call 999."
            )
        else:
            diagnosis = "🚨 RISIKO TINGGI: Kemungkinan Amaran Denggi Teruk"
            triage = "Segera ke Jabatan Kecemasan Hospital (Zon Merah/Kuning)"
            advice = (
                "Anda mempunyai tanda amaran serius (seperti pendarahan, platelet sangat rendah, atau darah pekat). "
                "JANGAN tunggu di rumah. Terus ke Jabatan Kecemasan Hospital terdekat sekarang atau hubungi 999."
            )
    elif len(warning_signs) > 0 or high_risk_age:
        is_high_risk = True
        color_class = "triage-orange"
        if lang == "EN":
            diagnosis = "⚠️ MODERATE-HIGH RISK: Probable Dengue with Warning Signs / High-Risk Age"
            triage = "Visit Hospital or Klinik Kesihatan Today for Admission / Daily Monitoring"
            advice = (
                "Because you have warning signs (like tummy pain, frequent vomiting, or low platelets) or are in a vulnerable age group, "
                "a doctor needs to examine you today and check your blood count regularly."
            )
        else:
            diagnosis = "⚠️ RISIKO SEDERHANA-TINGGI: Disyaki Denggi dengan Tanda Amaran / Umur Berisiko"
            triage = "Ke Hospital atau Klinik Kesihatan Hari Ini untuk Pemantauan Rapi"
            advice = (
                "Oleh kerana anda mempunyai tanda amaran (seperti sakit perut, muntah kerap, atau platelet rendah) atau berada dalam kumpulan umur berisiko, "
                "doktor perlu memeriksa anda hari ini dan memantau ujian darah anda secara berkala."
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
            color_class = "triage-yellow"
            if lang == "EN":
                diagnosis = "🟡 PROBABLE DENGUE (No Immediate Danger Signs)"
                triage = "See a Doctor at Klinik Kesihatan / Clinic for a Dengue Blood Test"
                advice = (
                    "Your symptoms match typical dengue fever, though no severe danger signs are present right now. "
                    "Visit a clinic for a dengue test, drink plenty of water/ORS, rest well, and watch closely for danger signs—especially on Days 4 to 7 of fever."
                )
            else:
                diagnosis = "🟡 KEMUNGKINAN DENGGI (Tiada Tanda Bahaya Segera)"
                triage = "Jumpa Doktor di Klinik Kesihatan / Klinik Swasta untuk Ujian Darah Denggi"
                advice = (
                    "Gejala anda sepadan dengan demam denggi biasa, namun tiada tanda bahaya serius buat masa ini. "
                    "Sila ke klinik untuk ujian darah denggi, minum air kosong/ORS dengan banyak, berehat, dan pantau tanda bahaya—terutamanya pada Hari ke-4 hingga ke-7 demam."
                )
        else:
            color_class = "triage-green"
            if lang == "EN":
                diagnosis = "🟢 LOW DENGUE SUSPICION"
                triage = "Home Care, Rest & Stay Hydrated"
                advice = (
                    "Your current symptoms show a low likelihood of dengue. Rest at home, drink plenty of fluids, "
                    "and see a doctor if a high fever or new symptoms develop over the next few days."
                )
            else:
                diagnosis = "🟢 RISIKO DENGGI RENDAH"
                triage = "Penjagaan di Rumah, Rehat & Minum Air Secukupnya"
                advice = (
                    "Gejala semasa anda menunjukkan kebarangkalian denggi yang rendah. Berehat di rumah, minum air secukupnya, "
                    "dan berjumpa doktor jika demam tinggi atau gejala baharu muncul dalam beberapa hari akan datang."
                )

    return {
        "diagnosis": diagnosis,
        "triage": triage,
        "advice": advice,
        "warning_signs": warning_signs,
        "notes": notes,
        "fired_rules": fired_rules,
        "color_class": color_class,
        "is_high_risk": is_high_risk,
    }


# ==================== TOP BAR & LANGUAGE SWITCHER ====================
top_col1, top_col2 = st.columns([3, 1.3])
with top_col2:
    if lang == "EN":
        if st.button("🇲🇾 Bahasa Melayu"):
            st.session_state.lang = "MS"
            st.rerun()
    else:
        if st.button("🇬🇧 English"):
            st.session_state.lang = "EN"
            st.rerun()

st.markdown(
    f"""
    <div class="hospital-header">
        <h1>{t['title']}</h1>
        <p>{t['subtitle']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

progress_val = min(st.session_state.step, 4) / 4.0
st.progress(progress_val)
st.write(f"**{t['step_label'].format(step=min(st.session_state.step, 4))}**")

# ==================== STEP 1: DEMOGRAPHICS & EXPOSURE ====================
if st.session_state.step == 1:
    st.markdown(f"<div class='step-card'><h3>{t['step1_title']}</h3><p>{t['step1_desc']}</p></div>", unsafe_allow_html=True)

    age = st.number_input(
        t["age"],
        min_value=0,
        max_value=120,
        value=st.session_state.get("age", 25),
    )
    gender_idx = st.selectbox(
        t["gender"],
        options=[0, 1],
        format_func=lambda i: t["gender_opts"][i],
        index=st.session_state.get("gender_idx", 0),
    )
    district = st.text_input(
        t["district"],
        value=st.session_state.get("district", "Kuala Lumpur"),
    )
    area_idx = st.selectbox(
        t["area_type"],
        options=[0, 1, 2],
        format_func=lambda i: t["area_opts"][i],
        index=st.session_state.get("area_idx", 0),
    )
    ever_dengue_idx = st.selectbox(
        t["ever_dengue"],
        options=[0, 1],
        format_func=lambda i: t["yes_no"][i],
        index=st.session_state.get("ever_dengue_idx", 0),
    )
    household_exp_idx = st.selectbox(
        t["household_exp"],
        options=[0, 1],
        format_func=lambda i: t["yes_no"][i],
        index=st.session_state.get("household_exp_idx", 0),
    )
    stagnant_water_idx = st.selectbox(
        t["stagnant_water"],
        options=[0, 1, 2],
        format_func=lambda i: t["yes_no_unk"][i],
        index=st.session_state.get("stagnant_water_idx", 0),
    )

    st.session_state.age = age
    st.session_state.gender_idx = gender_idx
    st.session_state.district = district
    st.session_state.area_idx = area_idx
    st.session_state.ever_dengue_idx = ever_dengue_idx
    st.session_state.household_exp_idx = household_exp_idx
    st.session_state.stagnant_water_idx = stagnant_water_idx

    st.markdown("---")
    if st.button(t["next_step2"]):
        st.session_state.step = 2
        st.rerun()

# ==================== STEP 2: FEVER & PAIN SYMPTOMS ====================
elif st.session_state.step == 2:
    st.markdown(f"<div class='step-card'><h3>{t['step2_title']}</h3><p>{t['step2_desc']}</p></div>", unsafe_allow_html=True)

    fever_bool = st.checkbox(
        t["fever_bool"],
        value=st.session_state.get("fever_bool", True),
    )
    fever_days = st.number_input(
        t["fever_days"],
        min_value=0,
        max_value=30,
        value=st.session_state.get("fever_days", 2),
    )
    max_temperature_f = st.number_input(
        t["max_temp"],
        min_value=0.0,
        max_value=110.0,
        step=0.1,
        value=float(st.session_state.get("max_temperature_f", 100.4)),
    )

    headache_bool = st.checkbox(
        t["headache_bool"],
        value=st.session_state.get("headache_bool", False),
    )
    headache_severity = st.slider(
        t["headache_sev"],
        min_value=0,
        max_value=10,
        value=st.session_state.get("headache_severity", 0),
    )
    retro_orbital_pain = st.slider(
        t["retro_pain"],
        min_value=0,
        max_value=10,
        value=st.session_state.get("retro_orbital_pain", 0),
    )
    muscle_pain_bool = st.checkbox(
        t["muscle_bool"],
        value=st.session_state.get("muscle_pain_bool", False),
    )
    muscle_pain = st.slider(
        t["muscle_sev"],
        min_value=0,
        max_value=10,
        value=st.session_state.get("muscle_pain", 0),
    )
    joint_pain = st.slider(
        t["joint_sev"],
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
        if st.button(t["back"]):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button(t["next_step3"]):
            st.session_state.step = 3
            st.rerun()

# ==================== STEP 3: OTHER SYMPTOMS & CLINICAL LABS ====================
elif st.session_state.step == 3:
    st.markdown(f"<div class='step-card'><h3>{t['step3_title']}</h3><p>{t['step3_desc']}</p></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        early_nausea_idx = st.selectbox(t["nausea"], [0, 1], format_func=lambda i: t["yes_no"][i], index=st.session_state.get("early_nausea_idx", 0))
        early_fatigue_idx = st.selectbox(t["fatigue"], [0, 1], format_func=lambda i: t["yes_no"][i], index=st.session_state.get("early_fatigue_idx", 0))
        early_appetite_idx = st.selectbox(t["appetite"], [0, 1], format_func=lambda i: t["yes_no"][i], index=st.session_state.get("early_appetite_idx", 0))
        early_abdominal_idx = st.selectbox(t["abdominal"], [0, 1], format_func=lambda i: t["yes_no"][i], index=st.session_state.get("early_abdominal_idx", 0))
        early_bleeding_idx = st.selectbox(t["bleeding"], [0, 1], format_func=lambda i: t["yes_no"][i], index=st.session_state.get("early_bleeding_idx", 0))
    with col_b:
        early_rash_idx = st.selectbox(t["rash"], [0, 1], format_func=lambda i: t["yes_no"][i], index=st.session_state.get("early_rash_idx", 0))
        early_chills_idx = st.selectbox(t["chills"], [0, 1], format_func=lambda i: t["yes_no"][i], index=st.session_state.get("early_chills_idx", 0))
        early_diarrhea_idx = st.selectbox(t["diarrhea"], [0, 1], format_func=lambda i: t["yes_no"][i], index=st.session_state.get("early_diarrhea_idx", 0))
        rash_bool = st.checkbox(t["rash_bool"], value=st.session_state.get("rash_bool", False))
        vomiting_bool = st.checkbox(t["vomit_bool"], value=st.session_state.get("vomiting_bool", False))

    vomiting_per_day = st.number_input(
        t["vomit_day"],
        min_value=0,
        max_value=20,
        value=st.session_state.get("vomiting_per_day", 0),
    )

    st.markdown(f"#### {t['lab_header']}")
    include_labs = st.checkbox(
        t["include_labs"],
        value=st.session_state.get("include_labs", False),
    )
    platelet_count = st.session_state.get("platelet_count", 0)
    wbc_count = st.session_state.get("wbc_count", 0)
    haematocrit_hct_idx = st.session_state.get("haematocrit_hct_idx", 0)

    if include_labs:
        platelet_count = st.number_input(
            t["platelet"],
            min_value=0,
            max_value=1000000,
            step=1000,
            value=platelet_count,
        )
        wbc_count = st.number_input(
            t["wbc"],
            min_value=0,
            max_value=50000,
            step=100,
            value=wbc_count,
        )
        haematocrit_hct_idx = st.selectbox(
            t["hct"],
            options=[0, 1, 2],
            format_func=lambda i: t["hct_opts"][i],
            index=haematocrit_hct_idx,
        )

    st.session_state.early_nausea_idx = early_nausea_idx
    st.session_state.early_fatigue_idx = early_fatigue_idx
    st.session_state.early_appetite_idx = early_appetite_idx
    st.session_state.early_abdominal_idx = early_abdominal_idx
    st.session_state.early_bleeding_idx = early_bleeding_idx
    st.session_state.early_rash_idx = early_rash_idx
    st.session_state.early_chills_idx = early_chills_idx
    st.session_state.early_diarrhea_idx = early_diarrhea_idx
    st.session_state.rash_bool = rash_bool
    st.session_state.vomiting_bool = vomiting_bool
    st.session_state.vomiting_per_day = vomiting_per_day
    st.session_state.include_labs = include_labs
    st.session_state.platelet_count = platelet_count
    st.session_state.wbc_count = wbc_count
    st.session_state.haematocrit_hct_idx = haematocrit_hct_idx

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["back"]):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button(t["run_eval"]):
            st.session_state.step = 4
            st.rerun()

# ==================== STEP 4: EVALUATION RESULTS ====================
elif st.session_state.step == 4:
    st.subheader(t["step4_title"])

    yn_map = ["No", "Yes"]
    ynu_map = ["No", "Yes", "Unknown"]

    payload = {
        "age": st.session_state.get("age", 25),
        "household_dengue_exposure_14d": yn_map[st.session_state.get("household_exp_idx", 0)],
        "stagnant_water": ynu_map[st.session_state.get("stagnant_water_idx", 0)],
        "fever_bool": st.session_state.get("fever_bool", True),
        "fever_days": st.session_state.get("fever_days", 2),
        "max_temperature_f": st.session_state.get("max_temperature_f", 100.4),
        "headache_bool": st.session_state.get("headache_bool", False),
        "headache_severity": st.session_state.get("headache_severity", 0),
        "retro_orbital_pain": st.session_state.get("retro_orbital_pain", 0),
        "muscle_pain_bool": st.session_state.get("muscle_pain_bool", False),
        "muscle_pain": st.session_state.get("muscle_pain", 0),
        "joint_pain": st.session_state.get("joint_pain", 0),
        "early_nausea": yn_map[st.session_state.get("early_nausea_idx", 0)],
        "early_fatigue": yn_map[st.session_state.get("early_fatigue_idx", 0)],
        "early_appetite_loss": yn_map[st.session_state.get("early_appetite_idx", 0)],
        "early_abdominal_pain": yn_map[st.session_state.get("early_abdominal_idx", 0)],
        "early_bleeding": yn_map[st.session_state.get("early_bleeding_idx", 0)],
        "early_rash": yn_map[st.session_state.get("early_rash_idx", 0)],
        "early_chills": yn_map[st.session_state.get("early_chills_idx", 0)],
        "early_diarrhea": yn_map[st.session_state.get("early_diarrhea_idx", 0)],
        "rash_bool": st.session_state.get("rash_bool", False),
        "vomiting_bool": st.session_state.get("vomiting_bool", False),
        "vomiting_per_day": st.session_state.get("vomiting_per_day", 0),
        "include_labs": st.session_state.get("include_labs", False),
        "platelet_count": st.session_state.get("platelet_count", 0),
        "wbc_count": st.session_state.get("wbc_count", 0),
        "haematocrit_hct_idx": st.session_state.get("haematocrit_hct_idx", 0),
    }

    result = evaluate_heuristics_and_triage(payload, lang)

    # Color-coded Hospital Triage Card
    st.markdown(
        f"""
        <div class="{result['color_class']}">
            <h3 style="margin-top:0;">{result['diagnosis']}</h3>
            <p style="font-size:16px; font-weight:bold; margin-bottom:8px;">🩺 {t['triage_label']}: {result['triage']}</p>
            <p style="font-size:15px; margin-bottom:0;">{result['advice']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result["warning_signs"]:
        st.error(f"**{t['warning_header']}** " + " | ".join(result["warning_signs"]))

    for note in result["notes"]:
        st.info(f"ℹ️ {note}")

    # High-Risk Medical Help Directory
    if result["is_high_risk"]:
        st.markdown(
            f"""
            <div class="help-box">
                <h4 style="color:#d32f2f; margin-top:0;">{t['help_title']}</h4>
                {t['help_body']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Patient-Friendly Summary Table
    summary_rows = [
        {
            t["col_item"]: "👤 Age Group" if lang == "EN" else "👤 Kumpulan Umur",
            t["col_status"]: classify_age_group(payload["age"], lang),
        },
        {
            t["col_item"]: "🌡️ Fever Level" if lang == "EN" else "🌡️ Tahap Demam",
            t["col_status"]: classify_fever_status(payload["max_temperature_f"], payload["fever_bool"], lang),
        },
        {
            t["col_item"]: "📅 Fever Stage" if lang == "EN" else "📅 Fasa Demam",
            t["col_status"]: classify_fever_phase(payload["fever_days"], lang),
        },
    ]
    if payload["include_labs"]:
        summary_rows.append({
            t["col_item"]: "🩸 White Blood Cells (WBC)" if lang == "EN" else "🩸 Sel Darah Putih (WBC)",
            t["col_status"]: classify_wbc(payload["wbc_count"], lang),
        })
        summary_rows.append({
            t["col_item"]: "🩹 Platelet Level" if lang == "EN" else "🩹 Paras Platelet",
            t["col_status"]: classify_platelet(payload["platelet_count"], lang),
        })
        summary_rows.append({
            t["col_item"]: "🧪 Blood Thickness (HCT)" if lang == "EN" else "🧪 Kepekatan Darah (HCT)",
            t["col_status"]: t["hct_opts"][payload["haematocrit_hct_idx"]],
        })

    st.markdown(f"#### {t['summary_header']}")
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    with st.expander(t["rules_expander"].format(count=len(result["fired_rules"]))):
        for r in result["fired_rules"]:
            st.write(f"- {r}")

    st.caption(t["disclaimer"])
    st.markdown("---")
    if st.button(t["start_over"]):
        st.session_state.step = 1
        st.rerun()