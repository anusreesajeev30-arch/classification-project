
import streamlit as st
import pickle
import numpy as np
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- BACKGROUND IMAGE FUNCTION ----------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        /* Background Image */
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Dark Overlay */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.45);
            z-index: -1;
        }}

        /* Main Container */
        .main-container {{
            background: rgba(0,0,0,0.75);
            padding: 35px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0px 8px 25px rgba(0,0,0,0.5);
            color: white;
        }}

        /* Title */
        h1 {{
            text-align: center;
            color: #ff4b2b;
            font-size: 42px !important;
            font-weight: bold;
        }}

        /* Button */
        .stButton>button {{
            width: 100%;
            background: linear-gradient(90deg, #ff416c, #ff4b2b);
            color: white;
            border-radius: 10px;
            height: 3em;
            font-size: 18px;
            font-weight: bold;
            border: none;
        }}

        .stButton>button:hover {{
            background: linear-gradient(90deg, #ff4b2b, #ff416c);
            color: white;
        }}

        /* Labels */
        label {{
            color: white !important;
            font-weight: 600;
        }}

        /* Input Fields */
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] {{
            background-color: rgba(0,0,0,0.6) !important;
            color: white !important;
            border: 1px solid white;
            border-radius: 10px;
        }}

        /* Slider */
        .stSlider {{
            color: white;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- ADD BACKGROUND ----------------
add_bg_from_local(r"C:\Users\ACER\OneDrive\Desktop\Project\background.png\18005.jpg")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))
le = pickle.load(open("encoder.pkl", "rb"))

# ---------------- UI ----------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🛡️ Fraud Detection App")

st.markdown(
    """
    <p style='text-align:center; color:white; font-size:18px;'>
    AI Powered Secure Transaction Verification System
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------- INPUTS ----------------
amount = st.number_input("💰 Amount", min_value=0.0)

transaction_hour = st.slider("⏰ Transaction Hour", 0, 23)

merchant_category = st.selectbox(
    "🏪 Merchant Category",
    le.classes_
)

foreign_transaction = st.selectbox(
    "🌍 Foreign Transaction",
    ["No", "Yes"]
)

location_mismatch = st.selectbox(
    "📍 Location Mismatch",
    ["No", "Yes"]
)

device_trust_score = st.slider(
    "📱 Device Trust Score",
    0.0, 100.0
)

velocity_last_24h = st.number_input(
    "⚡ Velocity Last 24h",
    min_value=0.0
)

cardholder_age = st.number_input(
    "👤 Cardholder Age",
    min_value=18
)

# ---------------- VALUE CONVERSION ----------------
foreign_transaction = 1 if foreign_transaction == "Yes" else 0
location_mismatch = 1 if location_mismatch == "Yes" else 0

# Encode merchant category
merchant_category = le.transform([merchant_category])[0]

# ---------------- PREDICTION ----------------
if st.button("🔍 Predict Transaction"):

    data = np.array([[
        amount,
        transaction_hour,
        merchant_category,
        foreign_transaction,
        location_mismatch,
        device_trust_score,
        velocity_last_24h,
        cardholder_age
    ]])

    result = model.predict(data)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- RESULT DISPLAY ----------------
    if result[0] == 1:
        st.markdown(
            """
            <div style="
                background-color:white;
                padding:20px;
                border-radius:15px;
                text-align:center;
                font-size:24px;
                font-weight:bold;
                color:red;
                box-shadow:0px 4px 15px rgba(0,0,0,0.3);
            ">
            🚨 Fraudulent Transaction Detected
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            """
            <div style="
                background-color:white;
                padding:20px;
                border-radius:15px;
                text-align:center;
                font-size:24px;
                font-weight:bold;
                color:green;
                box-shadow:0px 4px 15px rgba(0,0,0,0.3);
            ">
            ✅ Legitimate Transaction
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)
