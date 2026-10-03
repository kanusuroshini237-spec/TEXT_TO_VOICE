"""
Text to Voice (Text-to-Speech) App
Converts text into natural speech in many languages (incl. Indian
languages) using Google Text-to-Speech (gTTS). Needs internet,
but NO API key.
"""
from io import BytesIO

import streamlit as st
from gtts import gTTS

st.set_page_config(page_title="Text to Voice", page_icon="🔊", layout="centered")

# ---------------- Custom CSS ----------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;600&family=Noto+Sans+Telugu:wght@400;600&display=swap');

:root {
    --primary: #0ea5e9;
    --primary-dark: #0284c7;
    --accent: #6366f1;
    --bg: #f0f9ff;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --border: #e2e8f0;
    --radius: 14px;
    --shadow: 0 4px 20px rgba(15, 23, 42, 0.07);
}

/* ---------- Base ---------- */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', 'Noto Sans Devanagari', 'Noto Sans Telugu', sans-serif;
}
.stApp {
    background: linear-gradient(160deg, #e0f2fe 0%, var(--bg) 45%, #eef2ff 100%);
    color: var(--text);
}
.stApp p, .stApp label, .stApp span, .stApp li,
.stApp [data-testid="stMarkdownContainer"] {
    color: var(--text);
}
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 760px;
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

/* ---------- Title ---------- */
h1 {
    font-weight: 700 !important;
    letter-spacing: -0.5px;
    text-align: center;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 0.2rem;
}
.block-container > div > div > div > div[data-testid="stMarkdownContainer"] p {
    text-align: center;
    color: var(--muted);
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] h2 {
    font-size: 1.15rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--primary);
    display: inline-block;
}

/* ---------- Inputs ---------- */
.stTextArea textarea {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    font-size: 1.02rem;
    line-height: 1.6;
    box-shadow: var(--shadow);
    transition: border-color .2s, box-shadow .2s;
}
.stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2) !important;
}
.stTextArea textarea:disabled {
    background: #f8fafc !important;
    -webkit-text-fill-color: var(--muted);
}
div[data-baseweb="select"] > div {
    background: var(--card) !important;
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text) !important;
}

/* ---------- Radio buttons as pills ---------- */
div[role="radiogroup"] label {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 999px;
    padding: 0.3rem 1rem;
    margin-right: 0.4rem;
    transition: all .2s;
    cursor: pointer;
}
div[role="radiogroup"] label:hover {
    border-color: var(--primary);
    background: #e0f2fe;
}
div[role="radiogroup"] label:has(input:checked) {
    border-color: var(--primary);
    background: #e0f2fe;
    font-weight: 600;
}

/* ---------- Checkbox ---------- */
[data-testid="stCheckbox"] label span { font-weight: 500; }

/* ---------- File uploader ---------- */
[data-testid="stFileUploader"] section {
    background: var(--card);
    border: 2px dashed #bae6fd;
    border-radius: var(--radius);
    transition: all .2s;
}
[data-testid="stFileUploader"] section:hover {
    border-color: var(--primary);
    background: #f0f9ff;
}
[data-testid="stFileUploader"] section * { color: var(--text) !important; }

/* ---------- Buttons ---------- */
.stButton > button, .stDownloadButton > button {
    border-radius: 12px;
    padding: 0.65rem 1.6rem;
    font-weight: 600;
    border: 1.5px solid var(--primary);
    background: var(--card);
    color: var(--primary);
    transition: all .2s ease;
}
.stButton > button[kind="primary"] {
    width: 100%;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    color: #fff;
    border: none;
    box-shadow: 0 6px 18px rgba(14, 165, 233, 0.38);
}
.stButton > button[kind="primary"] p { color: #fff !important; }
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(14, 165, 233, 0.32);
}
.stDownloadButton > button { width: 100%; }
.stDownloadButton > button:hover {
    background: var(--primary);
    color: #fff;
}
.stDownloadButton > button:hover p { color: #fff !important; }

/* ---------- Audio player ---------- */
[data-testid="stAudio"], audio {
    width: 100%;
    border-radius: 999px;
}
[data-testid="stAudio"] {
    background: var(--card);
    padding: 0.6rem 0.8rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}

/* ---------- Captions ---------- */
[data-testid="stCaptionContainer"], .stApp small {
    color: var(--muted) !important;
    font-weight: 500;
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {
    border-radius: var(--radius);
    border: none;
    box-shadow: var(--shadow);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

LANGUAGES = {
    "English": "en", "Hindi": "hi", "Telugu": "te", "Tamil": "ta",
    "Bengali": "bn", "Marathi": "mr", "Kannada": "kn", "Malayalam": "ml",
    "Gujarati": "gu", "Urdu": "ur", "French": "fr", "Spanish": "es",
    "German": "de", "Japanese": "ja",
}

ACCENTS = {  # Only applies to English
    "Indian": "co.in",
    "American": "com",
    "British": "co.uk",
    "Australian": "com.au",
}

SAMPLES = {
    "English": "Hello! Welcome to my text to speech project. Have a great day.",
    "Hindi": "नमस्ते! मेरे टेक्स्ट टू स्पीच प्रोजेक्ट में आपका स्वागत है।",
    "Telugu": "నమస్కారం! నా టెక్స్ట్ టు స్పీచ్ ప్రాజెక్ట్‌కు స్వాగతం.",
}


def synthesize(text: str, lang: str, tld: str, slow: bool) -> bytes:
    buf = BytesIO()
    gTTS(text=text, lang=lang, tld=tld, slow=slow).write_to_fp(buf)
    return buf.getvalue()


# ---------------- Sidebar ----------------
st.sidebar.header("Settings")
lang_name = st.sidebar.selectbox("Language", list(LANGUAGES.keys()))
accent = "Indian"
if lang_name == "English":
    accent = st.sidebar.selectbox("Accent", list(ACCENTS.keys()))
slow = st.sidebar.checkbox("Slow speech")
st.sidebar.caption("Tip: type the text in the same language you select.")

# ---------------- Main ----------------
st.title("🔊 Text to Voice")
st.write("Type or upload text and convert it to speech you can play and download.")

source = st.radio("Input type", ["Type text", "Upload .txt"], horizontal=True)
if source == "Type text":
    text = st.text_area(
        "Your text", value=SAMPLES.get(lang_name, ""), height=200, max_chars=5000
    )
else:
    file = st.file_uploader("Upload a .txt file", type=["txt"])
    text = file.read().decode("utf-8", errors="ignore") if file else ""
    if text:
        st.text_area("File content", text, height=200, disabled=True)

st.caption(f"{len(text)} characters")

if st.button("🔊 Convert to speech", type="primary"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating audio..."):
            try:
                audio = synthesize(text, LANGUAGES[lang_name], ACCENTS[accent], slow)
            except Exception as e:
                st.error(f"Failed: {e}. Check your internet connection.")
                st.stop()
        st.success("Done!")
        st.audio(audio, format="audio/mp3")
        st.download_button("⬇️ Download MP3", audio, "speech.mp3", "audio/mpeg")