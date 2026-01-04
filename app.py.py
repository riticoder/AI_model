#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip install PyPDF2 ipywidgets')


# In[3]:


get_ipython().system('pip install SpeechRecognition gtts google-generativeai pyaudio')


# In[6]:


import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
from IPython.display import display, HTML, clear_output, Audio
import tempfile
import os
import time

class VoiceAgent:
    def __init__(self, api_key):
        """Initialize the Voice Agent with Google Gemini API"""
        self.recognizer = sr.Recognizer()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.is_active = False

        # Display initial interface
        self.display_interface()

    def display_interface(self):
        """Display the agent interface in Jupyter"""
        html = """
        <style>
            .agent-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                padding: 40px;
                color: white;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                margin: 20px 0;
            }
            .agent-face {
                width: 150px;
                height: 150px;
                margin: 0 auto 20px;
                background: white;
                border-radius: 50%;
                position: relative;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .agent-title {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .agent-status {
                font-size: 16px;
                opacity: 0.9;
            }
            .message-box {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                color: #2d3748;
                text-align: left;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .user-msg {
                background: #bee3f8;
                padding: 12px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .agent-msg {
                background: #c6f6d5;
                padding: 12px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .status-badge {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                background: rgba(255,255,255,0.2);
                margin: 10px 0;
                font-weight: 600;
            }
        </style>
        <div class="agent-container">
            <div class="agent-face">
                <svg viewBox="0 0 100 100" style="width: 100%; height: 100%;">
                    <!-- Hair -->
                    <ellipse cx="50" cy="35" rx="45" ry="35" fill="#2d3748"/>
                    <!-- Face -->
                    <circle cx="50" cy="55" r="35" fill="#fbb6ce"/>
                    <!-- Eyes -->
                    <circle cx="40" cy="50" r="5" fill="#2d3748"/>
                    <circle cx="60" cy="50" r="5" fill="#2d3748"/>
                    <!-- Smile -->
                    <path d="M 35 60 Q 50 70 65 60" stroke="#e53e3e" stroke-width="3" fill="none" stroke-linecap="round"/>
                </svg>
            </div>
            <div class="agent-title">🎙️ Voice Agent</div>
            <div class="agent-status">Ready to chat with you!</div>
            <div class="status-badge" id="status">● Ready</div>
        </div>
        """
        display(HTML(html))

    def update_status(self, message, color="#48bb78"):
        """Update status message"""
        display(HTML(f"""
        <div style="padding: 12px; background: {color}20; border-left: 4px solid {color}; 
                    border-radius: 8px; margin: 10px 0; color: #2d3748;">
            <strong style="color: {color};">●</strong> {message}
        </div>
        """))

    def listen(self):
        """Listen to user's voice input"""
        with sr.Microphone() as source:
            self.update_status("🎤 Listening... Please speak!", "#ed8936")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                self.update_status("🔄 Processing your speech...", "#4299e1")

                text = self.recognizer.recognize_google(audio)

                # Display user message
                display(HTML(f"""
                <div class="message-box">
                    <div class="user-msg">
                        <strong>👤 You:</strong> {text}
                    </div>
                </div>
                """))

                return text

            except sr.WaitTimeoutError:
                self.update_status("⏱️ No speech detected. Trying again...", "#fc8181")
                return None
            except sr.UnknownValueError:
                self.update_status("❓ Couldn't understand. Please speak clearly.", "#fc8181")
                return None
            except sr.RequestError as e:
                self.update_status(f"❌ Error: {e}", "#e53e3e")
                return None

    def speak(self, text):
        """Convert text to speech and play it using IPython Audio"""
        try:
            self.update_status("🔊 Speaking...", "#9f7aea")

            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name

            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file)

            # Display audio player (auto-play)
            display(HTML(f"""
            <audio autoplay style="display:none;">
                <source src="{temp_file}" type="audio/mpeg">
            </audio>
            """))

            # Alternative: Use IPython Audio widget
            display(Audio(temp_file, autoplay=True))

            # Wait for audio to finish (approximate)
            # Rough estimate: 150 words per minute, avg 5 chars per word
            duration = len(text) / 5 / 150 * 60
            time.sleep(duration + 1)

            # Clean up
            try:
                os.unlink(temp_file)
            except:
                pass

        except Exception as e:
            self.update_status(f"❌ Speech error: {e}", "#e53e3e")
            print(f"Error details: {e}")

    def get_response(self, user_input):
        """Get AI response from Gemini"""
        try:
            self.update_status("🤖 Thinking...", "#667eea")

            response = self.chat.send_message(user_input)
            ai_response = response.text

            # Display AI message
            display(HTML(f"""
            <div class="message-box">
                <div class="agent-msg">
                    <strong>🤖 Agent:</strong> {ai_response}
                </div>
            </div>
            """))

            return ai_response

        except Exception as e:
            self.update_status(f"❌ AI Error: {e}", "#e53e3e")
            return "I'm sorry, I encountered an error. Please try again."

    def start(self, max_turns=10):
        """Start the voice conversation"""
        self.is_active = True
        self.update_status(f"✅ Voice Agent Started! Say 'goodbye' or 'exit' to stop.", "#48bb78")

        turn = 0
        while self.is_active and turn < max_turns:
            turn += 1

            # Listen to user
            user_input = self.listen()

            if user_input is None:
                continue

            # Check for exit commands
            if any(word in user_input.lower() for word in ['exit', 'quit', 'stop', 'bye', 'goodbye']):
                goodbye = "Goodbye! It was nice talking to you."
                display(HTML(f"""
                <div class="message-box">
                    <div class="agent-msg">
                        <strong>🤖 Agent:</strong> {goodbye}
                    </div>
                </div>
                """))
                self.speak(goodbye)
                self.is_active = False
                break

            # Get and speak AI response
            ai_response = self.get_response(user_input)
            self.speak(ai_response)

        if turn >= max_turns:
            self.update_status(f"⏰ Reached maximum turns ({max_turns}). Conversation ended.", "#ed8936")

        self.update_status("👋 Conversation ended. Run agent.start() to chat again!", "#667eea")


# Display instructions
display(HTML("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 30px; border-radius: 15px; margin: 20px 0;">
    <h2 style="margin: 0 0 15px 0;">🚀 Voice Agent Setup (Windows Compatible)</h2>

    <h3 style="margin: 15px 0 10px 0;">📋 Installation (run once):</h3>
    <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; font-family: monospace;">
        !pip install SpeechRecognition gtts google-generativeai pyaudio
    </div>

    <h3 style="margin: 15px 0 10px 0;">💡 How to Use:</h3>
    <ol style="margin: 10px 0; padding-left: 20px;">
        <li>Replace 'YOUR_API_KEY' with your Google Gemini API key</li>
        <li>Run: <code style="background: rgba(0,0,0,0.2); padding: 3px 8px; border-radius: 4px;">agent = VoiceAgent(api_key='YOUR_API_KEY')</code></li>
        <li>Start chatting: <code style="background: rgba(0,0,0,0.2); padding: 3px 8px; border-radius: 4px;">agent.start()</code></li>
        <li>Click the play button on the audio player when it appears (browser security requirement)</li>
        <li>Speak clearly when prompted</li>
        <li>Say "goodbye" or "exit" to end the conversation</li>
    </ol>

    <h3 style="margin: 15px 0 10px 0;">⚙️ Optional Parameters:</h3>
    <ul style="margin: 10px 0; padding-left: 20px;">
        <li><code style="background: rgba(0,0,0,0.2); padding: 3px 8px; border-radius: 4px;">agent.start(max_turns=20)</code> - Set maximum conversation turns</li>
    </ul>

    <h3 style="margin: 15px 0 10px 0;">⚠️ Requirements:</h3>
    <ul style="margin: 10px 0; padding-left: 20px;">
        <li>Working microphone</li>
        <li>Audio output (speakers/headphones)</li>
        <li>Internet connection</li>
        <li>Google Gemini API key</li>
    </ul>

    <h3 style="margin: 15px 0 10px 0;">📝 Note:</h3>
    <p style="margin: 10px 0;">Audio will play through Jupyter's audio player. You may need to click the play button for the first audio due to browser autoplay restrictions.</p>
</div>
"""))

print("\n" + "="*60)
print("✅ Voice Agent Code Loaded Successfully!")
print("="*60)
print("\n📝 Quick Start:")
print("   agent = VoiceAgent(api_key='YOUR_API_KEY_HERE')")
print("   agent.start()")
print("\n💬 The agent will listen and respond with voice!")
print("="*60)


# In[7]:


agent = VoiceAgent(api_key='AIzaSyA2vBmqhtfcfFo5GBIeQkZEep2e5Qiqa-E')


# In[8]:


agent.start()


# In[9]:


get_ipython().system('pip install SpeechRecognition pyaudio elevenlabs')


# In[11]:


get_ipython().system('pip install SpeechRecognition pyaudio elevenlabs requests')


# In[15]:


get_ipython().system('pip install SpeechRecognition pyaudio requests')


# In[20]:


import speech_recognition as sr
import requests
from IPython.display import display, HTML, Audio
import tempfile
import os
import time

class HindiVoiceAgent:
    def __init__(self, elevenlabs_api_key, voice_id):
        """
        Initialize the Hindi/Haryanvi Voice Agent

        Args:
            elevenlabs_api_key: ElevenLabs API key
            voice_id: ElevenLabs voice ID
        """
        self.recognizer = sr.Recognizer()
        self.voice_id = voice_id
        self.api_key = elevenlabs_api_key
        self.conversation_history = []
        self.is_active = False

        # Display initial interface
        self.display_interface()

    def display_interface(self):
        """Display the agent interface in Jupyter"""
        html = """
        <style>
            .agent-container {
                background: linear-gradient(135deg, #FF9933 0%, #138808 50%, #000080 100%);
                border-radius: 20px;
                padding: 40px;
                color: white;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                margin: 20px 0;
            }
            .agent-face {
                width: 150px;
                height: 150px;
                margin: 0 auto 20px;
                background: white;
                border-radius: 50%;
                position: relative;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .agent-title {
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .agent-status {
                font-size: 18px;
                opacity: 0.95;
            }
            .message-box {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                color: #2d3748;
                text-align: left;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .user-msg {
                background: #bee3f8;
                padding: 12px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 4px solid #3182ce;
            }
            .agent-msg {
                background: #c6f6d5;
                padding: 12px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 4px solid #38a169;
            }
            .status-badge {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                background: rgba(255,255,255,0.3);
                margin: 10px 0;
                font-weight: 600;
            }
        </style>
        <div class="agent-container">
            <div class="agent-face">
                <svg viewBox="0 0 100 100" style="width: 100%; height: 100%;">
                    <!-- Hair -->
                    <ellipse cx="50" cy="35" rx="45" ry="35" fill="#2d3748"/>
                    <!-- Face -->
                    <circle cx="50" cy="55" r="35" fill="#fbb6ce"/>
                    <!-- Eyes -->
                    <circle cx="40" cy="50" r="5" fill="#2d3748"/>
                    <circle cx="60" cy="50" r="5" fill="#2d3748"/>
                    <!-- Smile -->
                    <path d="M 35 60 Q 50 70 65 60" stroke="#e53e3e" stroke-width="3" fill="none" stroke-linecap="round"/>
                    <!-- Bindi -->
                    <circle cx="50" cy="42" r="2" fill="#e53e3e"/>
                </svg>
            </div>
            <div class="agent-title">🎙️ हिंदी वॉइस एजेंट</div>
            <div class="agent-status">Hindi/Haryanvi Speaking Assistant</div>
            <div class="status-badge" id="status">● तैयार है (Ready)</div>
        </div>
        """
        display(HTML(html))

    def update_status(self, message, color="#48bb78"):
        """Update status message"""
        display(HTML(f"""
        <div style="padding: 12px; background: {color}20; border-left: 4px solid {color}; 
                    border-radius: 8px; margin: 10px 0; color: #2d3748;">
            <strong style="color: {color};">●</strong> {message}
        </div>
        """))

    def listen(self, language='hi-IN'):
        """Listen to user's voice input in Hindi/Haryanvi"""
        with sr.Microphone() as source:
            self.update_status("🎤 सुन रहा हूँ... बोलिए! (Listening... Please speak!)", "#ed8936")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                self.update_status("🔄 आपकी बात समझ रहा हूँ... (Processing your speech...)", "#4299e1")

                # Try Hindi recognition first
                try:
                    text = self.recognizer.recognize_google(audio, language='hi-IN')
                except:
                    # Fallback to English if Hindi fails
                    text = self.recognizer.recognize_google(audio, language='en-IN')

                # Display user message
                display(HTML(f"""
                <div class="message-box">
                    <div class="user-msg">
                        <strong>👤 आप (You):</strong> {text}
                    </div>
                </div>
                """))

                return text

            except sr.WaitTimeoutError:
                self.update_status("⏱️ कोई आवाज़ नहीं सुनाई दी। फिर से कोशिश करें। (No speech detected. Try again.)", "#fc8181")
                return None
            except sr.UnknownValueError:
                self.update_status("❓ समझ नहीं आया। कृपया साफ़ बोलें। (Couldn't understand. Please speak clearly.)", "#fc8181")
                return None
            except sr.RequestError as e:
                self.update_status(f"❌ त्रुटि (Error): {e}", "#e53e3e")
                return None

    def get_ai_response(self, user_input):
        """Get AI response - simple conversational system"""
        try:
            self.update_status("🤖 सोच रहा हूँ... (Thinking...)", "#667eea")

            # Simple conversational responses in Hindi/Haryanvi style
            user_lower = user_input.lower()

            # Greeting responses
            if any(word in user_lower for word in ['hello', 'hi', 'नमस्ते', 'नमस्कार', 'हलो', 'हेलो']):
                responses = [
                    "नमस्ते जी! कैसे हो आप? मैं आपकी मदद के लिए तैयार हूँ।",
                    "अरे भाई, राम राम! सब बढ़िया? मैं यहाँ हूँ आपकी सेवा में।",
                    "नमस्कार! बोलो, क्या काम है?"
                ]
                import random
                response = random.choice(responses)

            # How are you responses
            elif any(word in user_lower for word in ['how are you', 'कैसे हो', 'कैसी हो', 'क्या हाल', 'कैसा चल']):
                responses = [
                    "मैं बिल्कुल बढ़िया हूँ! धन्यवाद पूछने के लिए। आप सुनाइए, कैसे हैं?",
                    "अरे भाई, मस्त हूँ! तू सुना, सब ठीक ठाक?",
                    "बिल्कुल चौकस! तेरी मेहरबानी से सब बढ़िया चल रहा है।"
                ]
                import random
                response = random.choice(responses)

            # Name responses
            elif any(word in user_lower for word in ['name', 'नाम', 'naam', 'तुम्हारा नाम', 'आपका नाम']):
                response = "मेरा नाम हिंदी वॉइस एजेंट है। मैं आपकी सहायता के लिए यहाँ हूँ। आप मुझे अपना दोस्त समझ सकते हो!"

            # Help responses
            elif any(word in user_lower for word in ['help', 'मदद', 'सहायता', 'हेल्प']):
                response = "जी हाँ, मैं आपकी मदद कर सकता हूँ। आप मुझसे कुछ भी पूछ सकते हैं। बस हिंदी या अंग्रेजी में बोलिए। मैं यहाँ आपके लिए हूँ!"

            # Thank you responses
            elif any(word in user_lower for word in ['thank', 'thanks', 'धन्यवाद', 'शुक्रिया', 'थैंक्स']):
                responses = [
                    "आपका स्वागत है! मुझे खुशी है कि मैं आपकी मदद कर सका।",
                    "अरे, कोई बात नहीं भाई! बस यूँ ही मदद करते रहो।",
                    "मेरी खुशी है! कभी भी जरूरत हो तो बोलना।"
                ]
                import random
                response = random.choice(responses)

            # Goodbye responses
            elif any(word in user_lower for word in ['bye', 'goodbye', 'अलविदा', 'टाटा', 'चलता हूँ']):
                responses = [
                    "अलविदा! फिर मिलेंगे। आपका दिन शुभ हो!",
                    "ठीक है भाई, जा। ध्यान रखना अपना!",
                    "चलो ठीक है, फिर मिलेंगे। राम राम!"
                ]
                import random
                response = random.choice(responses)

            # Weather query
            elif any(word in user_lower for word in ['weather', 'मौसम', 'वेदर']):
                response = "मुझे अभी वर्तमान मौसम की जानकारी नहीं है, लेकिन मैं आपकी अन्य तरीकों से मदद कर सकता हूँ! कुछ और पूछना है?"

            # Time query
            elif any(word in user_lower for word in ['time', 'समय', 'टाइम', 'कितने बजे']):
                from datetime import datetime
                current_time = datetime.now().strftime("%I:%M %p")
                response = f"अभी का समय {current_time} बजे है भाई।"

            # Date query
            elif any(word in user_lower for word in ['date', 'तारीख', 'डेट', 'आज की तारीख']):
                from datetime import datetime
                current_date = datetime.now().strftime("%d %B %Y")
                response = f"आज की तारीख {current_date} है।"

            # Who are you
            elif any(word in user_lower for word in ['who are you', 'तुम कौन', 'आप कौन', 'तू कौन']):
                response = "मैं एक हिंदी वॉइस एजेंट हूँ। मैं आपसे हिंदी और अंग्रेजी में बात कर सकता हूँ। मैं आपकी मदद के लिए बना हूँ! आप मुझे अपना साथी समझो।"

            # What can you do
            elif any(word in user_lower for word in ['what can you', 'क्या कर सकते', 'तुम क्या', 'क्या कर सकते हो']):
                response = "मैं आपसे बातचीत कर सकता हूँ, आपके सवालों के जवाब दे सकता हूँ, समय और तारीख बता सकता हूँ, और हिंदी तथा अंग्रेजी दोनों में बात कर सकता हूँ। बस आप मुझसे कुछ भी पूछिए!"

            # Love/Like responses
            elif any(word in user_lower for word in ['love', 'like', 'प्यार', 'पसंद', 'अच्छा लगता']):
                response = "अरे वाह! मुझे भी आपसे बात करके बहुत अच्छा लगता है! आप बहुत अच्छे इंसान हैं।"

            # Bad words check (simple)
            elif any(word in user_lower for word in ['बकवास', 'बेवकूफ', 'stupid', 'idiot']):
                response = "अरे भाई, ऐसे मत बोलो। प्यार से बात करो। मैं यहाँ आपकी मदद के लिए हूँ।"

            # Default response
            else:
                responses = [
                    f"मैंने सुना कि आपने कहा: '{user_input}'। समझ गया मैं। और कुछ बताओ?",
                    f"हाँ जी, आपने कहा '{user_input}'। बोलो, और क्या बात करनी है?",
                    f"ठीक है! मैं समझा। आपने कहा '{user_input}'। अब और क्या?"
                ]
                import random
                response = random.choice(responses)

            # Add conversation to history
            self.conversation_history.append({
                "user": user_input,
                "agent": response
            })

            # Display AI message
            display(HTML(f"""
            <div class="message-box">
                <div class="agent-msg">
                    <strong>🤖 एजेंट (Agent):</strong> {response}
                </div>
            </div>
            """))

            return response

        except Exception as e:
            self.update_status(f"❌ AI त्रुटि (AI Error): {e}", "#e53e3e")
            return "माफ़ कीजिए, कुछ गड़बड़ हो गई। (Sorry, something went wrong.)"

    def speak(self, text):
        """Convert text to speech using ElevenLabs REST API"""
        try:
            self.update_status("🔊 बोल रहा हूँ... (Speaking...)", "#9f7aea")

            # ElevenLabs API endpoint
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"

            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }

            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }

            # Make API request
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name
                    fp.write(response.content)

                # Display audio player
                display(Audio(temp_file, autoplay=True))

                # Wait for audio to finish (approximate)
                duration = len(text) / 3 / 150 * 60  # Hindi is faster
                time.sleep(max(duration + 2, 3))

                # Clean up
                try:
                    os.unlink(temp_file)
                except:
                    pass
            else:
                self.update_status(f"❌ Audio generation failed: {response.status_code} - {response.text}", "#e53e3e")

        except Exception as e:
            self.update_status(f"❌ आवाज़ त्रुटि (Speech error): {e}", "#e53e3e")
            print(f"Error details: {e}")

    def start(self, max_turns=20):
        """Start the voice conversation"""
        self.is_active = True
        self.update_status(f"✅ एजेंट शुरू हो गया! 'अलविदा' या 'बाय' बोलकर बंद करें। (Agent started! Say 'goodbye' or 'bye' to stop.)", "#48bb78")

        turn = 0
        while self.is_active and turn < max_turns:
            turn += 1

            # Listen to user
            user_input = self.listen()

            if user_input is None:
                continue

            # Check for exit commands (Hindi and English)
            exit_words = ['exit', 'quit', 'stop', 'bye', 'goodbye', 'अलविदा', 'बाय', 'बंद करो', 'रुको']
            if any(word in user_input.lower() for word in exit_words):
                goodbye = "अलविदा जी! आपसे बात करके बहुत मज़ा आया। धन्यवाद! ध्यान रखना अपना। फिर मिलेंगे!"
                display(HTML(f"""
                <div class="message-box">
                    <div class="agent-msg">
                        <strong>🤖 एजेंट (Agent):</strong> {goodbye}
                    </div>
                </div>
                """))
                self.speak(goodbye)
                self.is_active = False
                break

            # Get and speak AI response
            ai_response = self.get_ai_response(user_input)
            self.speak(ai_response)

        if turn >= max_turns:
            self.update_status(f"⏰ अधिकतम बातचीत पूरी हो गई ({max_turns}). बातचीत समाप्त। (Maximum turns reached. Conversation ended.)", "#ed8936")

        self.update_status("👋 बातचीत समाप्त। agent.start() चलाकर फिर से शुरू करें! (Conversation ended. Run agent.start() to chat again!)", "#667eea")

        return self.conversation_history


# Display instructions
display(HTML("""
<div style="background: linear-gradient(135deg, #FF9933 0%, #138808 50%, #000080 100%); 
            color: white; padding: 30px; border-radius: 15px; margin: 20px 0;">
    <h2 style="margin: 0 0 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
        🚀 हिंदी/हरियाणवी वॉइस एजेंट - NO IMPORT ERRORS!
    </h2>

    <h3 style="margin: 15px 0 10px 0;">📋 इंस्टॉलेशन (Installation) - बस ये 2 चीजें:</h3>
    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; font-family: monospace; font-size: 14px;">
        !pip install SpeechRecognition pyaudio requests
    </div>

    <h3 style="margin: 15px 0 10px 0;">💡 कैसे इस्तेमाल करें (How to Use):</h3>
    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; font-family: monospace; font-size: 13px;">
# एजेंट बनाएं (Create agent)
agent = HindiVoiceAgent(
    elevenlabs_api_key='your_api_key',
    voice_id='XrExE9yKIg1WjnnlVkGX'
)

# बातचीत शुरू करें (Start conversation)
agent.start()
    </div>

    <h3 style="margin: 15px 0 10px 0;">🎤 खासियत (Features):</h3>
    <ul style="margin: 10px 0; padding-left: 20px; font-size: 14px;">
        <li>✨ हिंदी और हरियाणवी में बोलता है (Speaks in Hindi and Haryanvi)</li>
        <li>🎧 हिंदी आवाज़ पहचानता है (Recognizes Hindi voice)</li>
        <li>🔊 ElevenLabs की शानदार आवाज़ (Premium ElevenLabs voice)</li>
        <li>💬 स्मार्ट बातचीत - multiple responses</li>
        <li>🇮🇳 देसी स्टाइल बातचीत (Desi style conversation)</li>
        <li>⏰ समय और तारीख बताता है (Tells time and date)</li>
        <li>🚫 NO elevenlabs import needed - Pure REST API!</li>
    </ul>

    <h3 style="margin: 15px 0 10px 0;">🎯 उदाहरण वाक्य (Example Phrases):</h3>
    <ul style="margin: 10px 0; padding-left: 20px; font-size: 14px;">
        <li>"नमस्ते" / "राम राम" (Hello)</li>
        <li>"कैसे हो?" / "क्या हाल चाल?" (How are you?)</li>
        <li>"तुम्हारा नाम क्या है?" (What is your name?)</li>
        <li>"अभी समय क्या है?" (What time is it?)</li>
        <li>"आज की तारीख क्या है?" (What's today's date?)</li>
        <li>"तुम क्या कर सकते हो?" (What can you do?)</li>
        <li>"मदद करो" (Help me)</li>
        <li>"धन्यवाद" (Thank you)</li>
        <li>"अलविदा" / "बाय" (Goodbye)</li>
    </ul>

    <h3 style="margin: 15px 0 10px 0;">🌟 NEW: Randomized Responses!</h3>
    <p style="margin: 10px 0; font-size: 14px;">
        Agent now gives different responses each time for natural conversation!
    </p>
</div>
"""))

print("\n" + "="*70)
print("✅ हिंदी वॉइस एजेंट तैयार है! (Hindi Voice Agent Ready!)")
print("="*70)
print("\n📝 त्वरित शुरुआत (Quick Start):")
print("   agent = HindiVoiceAgent(")
print("       elevenlabs_api_key='your_api_key',")
print("       voice_id='XrExE9yKIg1WjnnlVkGX'")
print("   )")
print("   agent.start()")
print("\n💬 हिंदी/हरियाणवी में बात करने के लिए तैयार!")
print("   (Ready to chat in Hindi/Haryanvi!)")
print("\n🚫 NO ELEVENLABS IMPORT - Uses direct REST API!")
print("="*70)


# In[17]:


agent = HindiVoiceAgent(
    elevenlabs_api_key='sk_829c0f6dec8ad207a4d2f9d4607395e877e4a4d1bbcee640',
    voice_id='XrExE9yKIg1WjnnlVkGX'
)

agent.start()


# In[ ]:




