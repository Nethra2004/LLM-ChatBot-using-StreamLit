import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Loading environment variables
load_dotenv()

# Configuring Streamlit page settings
st.set_page_config(
    page_title="AI - ChatBot!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Injecting Custom CSS for styling
st.markdown("""
<style>
/* Background Animation */
@keyframes gradientBG {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}

/* Animated Gradient Background */
.stApp {
  background: linear-gradient(-45deg, #dbeafe, #f0f4f8, #c7d2fe, #e0f2fe);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  font-family: 'Segoe UI', sans-serif;
  min-height: 100vh;
  padding: 2rem;
}

/* Chat Title */
h1 {
    text-align: center;
    color: #2c3e50;
    font-size: 3rem;
    margin-bottom: 20px;
}

/* Chat message container */
.stChatMessage {
    padding: 1rem;
    border-radius: 15px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}

.stChatMessage:hover {
    transform: scale(1.02);
}

/* User message style */
.stChatMessage.user {
    background-color: #d1e7dd;
    color: #000;
    text-align: right;
}

/* Assistant message style */
.stChatMessage.assistant {
    background-color: #cfe2ff;
    color: #000;
    text-align: left;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f1f1; 
}
::-webkit-scrollbar-thumb {
  background: #888; 
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}
</style>
""", unsafe_allow_html=True)

# API KEY
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Setting up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('models/gemini-1.5-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initializing chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Displaying the chatbot's title on the page
st.title("🤖 Your AI - Friend !")

# Displaying chatbot description below title
st.markdown("""
<div style='text-align: center; font-size: 1.2rem; color: #555; margin-bottom: 30px;'>
    An intelligent conversational assistant powered by Google Gemini-Pro AI.<br>
    Ask me anything, and let's chat smartly!
</div>
""", unsafe_allow_html=True)

# Displaying the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask me anything...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Displaying Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
