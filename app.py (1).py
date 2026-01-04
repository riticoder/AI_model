import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Hindi Voice Agent", page_icon="🎙️")

st.title("🎙️ हिंदी / हरियाणवी Voice Agent")

with st.sidebar:
    st.header("🔑 ElevenLabs Settings")
    api_key = st.text_input("ElevenLabs API Key", type="password")
    voice_id = st.text_input("Voice ID", value="XrExE9yKIg1WjnnlVkGX")

def get_reply(text):
    t = text.lower()
    if "नमस्ते" in t or "hello" in t:
        return "राम राम भाई! कैसे हो?"
    if "कैसे" in t:
        return "मैं बढ़िया हूँ, तू बता!"
    if "समय" in t or "time" in t:
        return f"अभी {datetime.now().strftime('%I:%M %p')} बजे हैं"
    if "धन्यवाद" in t or "thanks" in t:
        return "कोई बात नहीं भाई!"
    return "ठीक है, और बताओ?"

msg = st.text_input("💬 बोल या लिख:")

if st.button("Send"):
    if not api_key:
        st.error("⚠️ API Key डाल भाई")
    elif msg:
        reply = get_reply(msg)
        st.success(reply)

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": reply,
            "model_id": "eleven_multilingual_v2"
        }

        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            st.audio(r.content, format="audio/mp3")
        else:
            st.error("❌ Voice generate नहीं हुई")
