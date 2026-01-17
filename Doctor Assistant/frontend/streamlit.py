import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="Doctor's Assistant", page_icon="🩺", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        /* Background and general styling */
        body {
            background-color: #f3f6fa;
        }
        .stApp {
            background: linear-gradient(120deg, #e0f7fa, #e1bee7);
            color: #222;
            font-family: 'Segoe UI', sans-serif;
        }
        /* Header */
        .main-title {
            text-align: center;
            font-size: 40px !important;
            color: #4a148c;
            font-weight: bold;
            text-shadow: 1px 1px 2px #b39ddb;
            margin-bottom: 20px;
        }
        /* Text area */
        .stTextArea textarea {
            background-color: #ffffff;
            border-radius: 10px;
            border: 1px solid #8e24aa;
            color: #333;
            font-size: 16px;
            padding: 15px;
        }
        /* Button */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #8e24aa, #6a1b9a);
            color: white;
            border-radius: 10px;
            border: none;
            font-size: 18px;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #ab47bc, #8e24aa);
            transform: scale(1.05);
        }
        /* Subheaders */
        .subheader {
            color: #4a148c;
            margin-top: 25px;
            font-weight: 600;
        }
        /* Result boxes */
        .result-box {
            background-color: #f8f9fa;
            border-left: 6px solid #8e24aa;
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("<h1 class='main-title'>🩺 Doctor's Assistant</h1>", unsafe_allow_html=True)

# --- Input Area ---
input_text = st.text_area(
    "Enter the Patient History Here please!",
    height=250,
    placeholder="Enter patient summary here..."
)

# --- Summarise Button ---
if st.button("Summarise"):
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some patient history first!")
    else:
        with st.spinner("Analysing patient history..."):
            try:
                response = requests.post("http://localhost:8000/summarise", json={"text": input_text})
                if response.status_code == 200:
                    result = response.json().get('result')

                    st.markdown("<h3 class='subheader'>Summary of the Patient</h3>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-box'>{result['summary']}</div>", unsafe_allow_html=True)

                    if result['summary'] != "I cannot help you with that":
                        st.markdown("<h3 class='subheader'>Latest Blood Pressure</h3>", unsafe_allow_html=True)
                        st.markdown(f"<div class='result-box'>{result['Blood_pressure']}</div>", unsafe_allow_html=True)

                        st.markdown("<h3 class='subheader'>Latest Diabetes Result</h3>", unsafe_allow_html=True)
                        st.markdown(f"<div class='result-box'>{result['diabetes']}</div>", unsafe_allow_html=True)

                        st.markdown("<h3 class='subheader'>Diseases of the Patient</h3>", unsafe_allow_html=True)
                        if result['disease']:
                         for i in result['disease']:
                            st.markdown(f"<div class='result-box'>{i}</div>", unsafe_allow_html=True)

                        st.markdown("<h3 class='subheader'>Diagnosis so far</h3>", unsafe_allow_html=True)
                        if result['diagnosis']:
                         for i in result['diagnosis']:
                            st.markdown(f"<div class='result-box'>{i}</div>", unsafe_allow_html=True)
                else:
                    st.error("❌ Server error! Could not get a response from the backend.")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")
