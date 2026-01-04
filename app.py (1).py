%%writefile app.py
import streamlit as st
import requests

st.set_page_config(page_title="Hindi Voice Agent", page_icon="🎙️")

st.title("🎙️ हिंदी वॉइस एजेंट")
st.write("Hindi/Haryanvi Speaking Assistant")

# Sidebar
with st.sidebar:
    st.header("🔑 API Settings")
    api_key = st.text_input("ElevenLabs API Key", type="password")
    voice_id = st.text_input("Voice ID", value="XrExE9yKIg1WjnnlVkGX")

# Simple AI responses
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

# Main app
st.markdown("### 💬 Chat")

user_input = st.text_input("Type your message (Hindi/English):", key="user_msg")

if st.button("Send") and user_input:
    if not api_key:
        st.error("⚠️ Please enter API Key in sidebar!")
    else:
        # Get response
        response = get_response(user_input)
        
        # Display
        st.info(f"**You:** {user_input}")
        st.success(f"**Agent:** {response}")
        
        # Text to speech
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

# Footer
st.markdown("---")
st.markdown("🎤 **Try these:** नमस्ते | कैसे हो | समय क्या है | धन्यवाद")
```

---

## 🔄 **Steps to Fix:**

1. **Go to your Streamlit app**
2. Click **"Manage app"** (bottom right)
3. Click **"⋮"** (three dots) → **"Delete app"**
4. **Re-deploy with new files**

---

## 📤 **Or Quick Re-deploy:**

1. **Edit your GitHub files:**
   - Go to your repo
   - Click on `app.py` → Edit (pencil icon)
   - Replace with code above
   - Commit changes

2. **Edit `requirements.txt`:**
   - Click on it → Edit
   - Replace with just:
```
   streamlit
   requests