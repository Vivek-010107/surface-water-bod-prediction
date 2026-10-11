from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st


# --------------------------------------------------
# CPCB BOD REFERENCE CRITERIA (5-day BOD at 20 °C)
# BOD-only comparisons; these do not assign designated-use water classes.
# --------------------------------------------------
BOD_BOUNDARIES = (2.0, 3.0)
BOD_DISPLAY_MAX = 6.0  # Visual scale limit, not a classification boundary.

FEATURES = [
    "Temperature", "DO", "pH", "Conductivity", "Nitrate_Nitrite",
    "Fecal_Coliform", "Total_Coliform", "Year",
]
MODEL_PATH = Path(__file__).resolve().parent / "final_bod_random_forest_model.joblib"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def validate(values):
    if not all(np.isfinite(v) for v in values.values()):
        return "Please enter a finite numeric value for every parameter."
    if not 0 <= values["pH"] <= 14:
        return "pH must be between 0 and 14."
    if not -5 <= values["Temperature"] <= 60:
        return "Enter a surface-water temperature between −5 and 60 °C."
    for name in FEATURES:
        if name not in ("Temperature", "pH", "Year") and values[name] < 0:
            return f"{name.replace('_', ' ')} cannot be negative."
    year = values["Year"]
    if not float(year).is_integer():
        return "Year must be a whole number."
    return None


def show_indicator(bod):
    low, high = BOD_BOUNDARIES
    if not 0 < low < high < BOD_DISPLAY_MAX:
        st.error("The BOD reference indicator configuration is invalid.")
        return
    a, b = low / BOD_DISPLAY_MAX * 100, high / BOD_DISPLAY_MAX * 100
    position = min(max(bod / BOD_DISPLAY_MAX * 100, 0), 100)
    if bod <= low:
        interpretation = "Within the BOD criterion used for CPCB Class A"
    elif bod <= high:
        interpretation = "Within the BOD criterion used for CPCB Classes B/C, but above the Class A BOD criterion"
    else:
        interpretation = "Above the BOD criterion specified for CPCB Classes A-C"
    st.markdown("#### BOD Reference Indicator")
    st.write(interpretation)
    st.markdown(
        f'''<div role="img" aria-label="BOD reference indicator: {bod:.2f} mg/L"
        style="margin:24px 8px 14px;position:relative;height:18px;border-radius:6px;
        background:linear-gradient(to right,#43a66f 0%,#43a66f {a}%,
        #f2cf4a {a}%,#f2cf4a {b}%,#df6262 {b}%,#df6262 100%);">
        <div style="position:absolute;left:clamp(5px,{position}%,calc(100% - 5px));transform:translateX(-50%);
        top:-7px;width:5px;height:32px;background:#142d40;border:2px solid white;
        box-shadow:0 1px 4px #142d4040;border-radius:4px;"></div></div>
        <div style="display:grid;grid-template-columns:{a}fr {b-a}fr {100-b}fr;
        margin:0 8px 16px;text-align:center;font-size:0.85rem;font-weight:600;">
        <span>≤ {low:g} mg/L</span><span>{low:g}–{high:g} mg/L</span>
        <span>&gt; {high:g} mg/L</span></div>''', unsafe_allow_html=True,
    )
    st.caption(
        "CPCB designated-use water-quality classes are determined using multiple "
        "parameters such as BOD, dissolved oxygen, pH and coliform measurements. "
        "Therefore, this indicator compares only the predicted BOD value with CPCB "
        "BOD criteria and does not assign an official CPCB water-quality class."
    )
    st.caption(f"Visual scale: 0–{BOD_DISPLAY_MAX:g} mg/L. The middle section represents BOD > 2 and ≤ 3 mg/L.")
    if bod > BOD_DISPLAY_MAX:
        st.caption("Prediction exceeds the displayed scale; marker is shown at its upper end.")
    st.caption(
        "Reference: Central Pollution Control Board (CPCB), "
        "[CPCB Designated Best Use Water Quality Criteria]"
        "(https://cpcb.nic.in/wqm/Designated_Best_Use_Water_Quality_Criteria.pdf)."
    )


def main():
    st.set_page_config(page_title="Surface Water Organic Pollution Prediction", page_icon="💧", layout="centered")
    st.markdown("""
<style>
.stApp {background:#101215;color:#e1e5ea;color-scheme:dark;border-top:0;}
[data-testid="stHeader"] {background:#101215;color:#e1e5ea;}
[data-testid="stMain"], [data-testid="stBottom"] {background:#101215;}
.stApp h1,.stApp h2,.stApp h3,.stApp h4 {color:#f5f7fa;}
.stApp [data-testid="stMarkdownContainer"],.stApp label {color:#e1e5ea;}
.stApp [data-testid="stCaptionContainer"] {color:#a7b0bc;}
.stApp a {color:#8ec9d3;}
.stApp a:focus-visible {outline:2px solid #8ec9d3;outline-offset:3px;}
.block-container {max-width:920px;padding-top:2.2rem;padding-bottom:1.5rem;}
[data-testid="stForm"],.st-key-prediction-result {border-radius:14px;
    background:#191d23;border:1px solid #343d47;color:#e1e5ea;
    box-shadow:0 3px 14px #00000020;transition:border-color .18s ease,box-shadow .18s ease;}
[data-testid="stForm"]:hover,.st-key-prediction-result:hover {border-color:#52626f;}
[data-testid="stNumberInput"] [data-baseweb="input"] {
    background:#11151a;border:1px solid #46515e;border-radius:8px;
    transition:border-color .18s ease,box-shadow .18s ease;}
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
    border-color:#8ec9d3;box-shadow:0 0 0 2px #8ec9d330;}
[data-testid="stNumberInput"] input {background:#11151a;color:#f0f3f7;caret-color:#8ec9d3;}
[data-testid="stNumberInput"] button {background:#252d36;color:#dce4ec;border-color:#46515e;}
[data-testid="stNumberInput"] button:hover {background:#36434f;}
[data-testid="stNumberInput"] button:focus-visible {outline:2px solid #8ec9d3;outline-offset:-2px;}
[data-testid="stForm"] {padding:1.3rem;}
[data-testid="stFormSubmitButton"] button {background:#b92e38;color:white;
    border:1px solid #d14b55;min-height:2.9rem;border-radius:8px;font-weight:650;
    cursor:pointer;transition:background .18s ease,border-color .18s ease;}
[data-testid="stFormSubmitButton"] button:hover {background:#cf3541;border-color:#ee7b84;}
[data-testid="stFormSubmitButton"] button:focus-visible {outline:3px solid #ee9098;outline-offset:3px;}
.st-key-prediction-result {border-color:#527d86;}
.st-key-prediction-result [data-testid="stMetric"] {padding:.75rem 0 1.1rem;}
.st-key-prediction-result [data-testid="stMetricValue"] {font-size:clamp(2.3rem,6vw,3.2rem);
    font-weight:650;letter-spacing:-.035em;color:#f5f7fa;}
[data-testid="stMetricLabel"] {color:#b5bec9;}
[data-testid="stAlert"] {border-radius:10px;font-size:.9rem;background:#202e38;
    border:1px solid #3e586a;color:#e1e5ea;}
[data-testid="stExpander"] details {background:#191d23;border:1px solid #343d47;
    border-radius:12px;color:#e1e5ea;}
[data-testid="stExpander"] summary {color:#e1e5ea;border-radius:10px;
    transition:background .18s ease;}
[data-testid="stExpander"] summary:hover {background:#252d36;}
[data-testid="stExpander"] summary:focus-visible {outline:2px solid #8ec9d3;outline-offset:2px;}
.bod-footer {text-align:center;font-size:.76rem;color:#a7b0bc;padding:1.5rem .5rem .25rem;
    margin-top:1rem;border-top:1px solid #343d47;}
@media(prefers-reduced-motion:reduce) {
    .stApp *, .stApp *::before, .stApp *::after {transition:none !important;}
}
@media(max-width:600px) {
    .block-container {padding-top:1.3rem;}
    [data-testid="stForm"] {padding:1rem;}
}
</style>
""", unsafe_allow_html=True)
    st.title("Surface Water Organic Pollution Prediction")
    st.subheader("Machine Learning-Based BOD Estimation")
    st.write("Estimate Biochemical Oxygen Demand (BOD) from water-quality parameters using a trained Random Forest regression model.")
    st.caption("ML-Based Decision Support Prototype")
    with st.form("water_parameters"):
        st.subheader("Water Quality Parameters")
        st.write("Enter the measured water-quality parameters below.")
        st.caption("Accepted temperature range: −5–60 °C. Enter Year as a whole number.")
        left, right = st.columns(2)
        with left:
            temperature = st.number_input("Temperature (°C)", value=25.0)
            ph = st.number_input("pH", value=7.0)
            nitrate = st.number_input("Nitrate + Nitrite (mg/L)", value=1.0)
            total = st.number_input("Total Coliform (MPN/100 mL)", value=100.0)
        with right:
            dissolved = st.number_input("Dissolved Oxygen - DO (mg/L)", value=6.0)
            conductivity = st.number_input("Conductivity (µmhos/cm)", value=300.0)
            fecal = st.number_input("Fecal Coliform (MPN/100 mL)", value=50.0)
            year = st.number_input("Year", value=2026, step=1)
        submitted = st.form_submit_button("Predict BOD", type="primary", use_container_width=True)

    if submitted:
        values = dict(zip(FEATURES, [temperature, dissolved, ph, conductivity, nitrate, fecal, total, year]))
        error = validate(values)
        if error:
            st.error(error)
        else:
            try:
                model = load_model()
            except FileNotFoundError:
                st.error("Model file is missing. Place final_bod_random_forest_model.joblib beside app.py.")
            except Exception:
                st.error("The saved model could not be loaded. Check that it is intact and install the packages in requirements.txt, including scikit-learn 1.6.1.")
            else:
                try:
                    input_df = pd.DataFrame([values], columns=FEATURES)
                    predicted_log_bod = model.predict(input_df)[0]
                    with np.errstate(over="raise", invalid="raise"):
                        predicted_bod = float(np.expm1(predicted_log_bod))
                    if not np.isfinite(predicted_bod):
                        raise ValueError("Non-finite prediction")
                    predicted_bod = max(0.0, predicted_bod)
                except Exception:
                    st.error("A valid prediction could not be produced. Please check your inputs and model compatibility.")
                else:
                    with st.container(border=True, key="prediction-result"):
                        st.subheader("Prediction Result")
                        st.metric("Predicted BOD", f"{predicted_bod:.2f} mg/L")
                        show_indicator(predicted_bod)
                        st.write("Generally, higher BOD indicates greater biodegradable organic load and oxygen demand. BOD alone does not describe all forms of water pollution.")
                        st.info("Important: This prediction is a machine-learning estimate intended for preliminary assessment and decision support. It does not replace laboratory BOD testing and should not be used alone to determine overall water safety.")

    with st.expander("About the Model"):
        st.markdown("""
**Model:** Tuned Random Forest Regressor  
**Target:** Biochemical Oxygen Demand (BOD)  
**Input features:** Temperature, Dissolved Oxygen, pH, Conductivity,
Nitrate + Nitrite, Fecal Coliform, Total Coliform, Year  
**Dataset:** Indian Water Quality Data  
**Dataset Source:** Kaggle  
**Supervised observations with BOD:** 1,948  
**Target transformation:** log1p(BOD)  
**Final model selection:** Random Forest selected based primarily on training
cross-validation performance and course suitability.  
**5-fold CV R²:** approximately 0.651  
**Held-out test log-space R²:** approximately 0.644  
**Held-out original-scale MAE:** approximately 3.85 mg/L

**Important limitation:** The model can substantially underpredict rare extreme
BOD observations, so predictions should be treated as preliminary estimates rather
than replacements for laboratory testing.

Model details and evaluation figures are supplied by the project author.
""")
    st.markdown('<footer class="bod-footer">Academic Machine Learning Prototype | Surface Water BOD Estimation</footer>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
