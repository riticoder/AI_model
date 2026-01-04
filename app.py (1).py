%%writefile app.py
import streamlit as st
import requests

st.set_page_config(page_title="Hindi Voice Agent", page_icon="🎙️")

st.title("🎙️ हिंदी वॉइस एजेंट")
st.write("Hindi/Haryanvi Speaking Assistant")


with st.sidebar:
    st.header("🔑 API Settings")
    api_key = st.text_input("ElevenLabs API Key", type="password")
    voice_id = st.text_input("Voice ID", value="XrExE9yKIg1WjnnlVkGX")


def get_response(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ['hello', 'hi', 'नमस्ते', 'हलो']):
        return "नमस्ते! कैसे हो? मैं आपकी मदद के लिए यहाँ हूँ।"
    elif any(w in text_lower for w in ['कैसे हो', 'how are you', 'क्या हाल']):
        return "मैं बिल्कुल बढ़िया हूँ! आप कैसे हैं?"
    elif any(w in text_lower for w in ['name', 'नाम']):
        return "मेरा नाम हिंदी वॉइस एजेंट है।"
    elif any(w in text_lower for w in ['time', 'समय']):
        from datetime import datetime
        return f"अभी {datetime.now().strftime('%I:%M %p')} बजे हैं।"
    elif any(w in text_lower for w in ['thank', 'धन्यवाद']):
        return "आपका स्वागत है!"
    return f"मैंने सुना: '{text}' - और बताओ?"


st.markdown("### 💬 Chat")

user_input = st.text_input("Type your message (Hindi/English):", key="user_msg")

if st.button("Send") and user_input:
    if not api_key:
        st.error("⚠️ Please enter API Key in sidebar!")
    else:
        
        response = get_response(user_input)
        
       
        st.info(f"**You:** {user_input}")
        st.success(f"**Agent:** {response}")
        
        
        with st.spinner("🔊 Generating speech..."):
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": response,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8
                }
            }
            
            r = requests.post(url, headers=headers, json=data)
            
            if r.status_code == 200:
                st.audio(r.content, format="audio/mp3")
            else:
                st.error(f"❌ Speech generation failed: {r.status_code}")


st.markdown("---")
st.markdown("🎤 **Try these:** नमस्ते | कैसे हो | समय क्या है | धन्यवाद")

   streamlit

   requests
