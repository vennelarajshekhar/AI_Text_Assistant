import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# Check whether API key exists
if not api_key:
    st.error("GROQ_API_KEY is not configured. Please check your .env file.")
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)


# ============================================================
# 2. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# 3. APPLICATION TITLE
# ============================================================

st.title("🤖 AI Study Assistant")

st.write(
    "Ask me any study-related question. "
    "I will explain it in simple words with examples."
)


# ============================================================
# 4. CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# 5. DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# 6. CLEAR CHAT BUTTON
# ============================================================

if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# ============================================================
# 7. USER INPUT
# ============================================================

question = st.text_input(...)


# ============================================================
# 8. PROCESS USER QUESTION
# ============================================================

if question:

    # Add user's message to chat history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Display user's message
    with st.chat_message("user"):
        st.markdown(question)


    # ========================================================
    # 9. SEND QUESTION TO GROQ
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a friendly AI Study Assistant. "
                                "Explain technical concepts in simple and "
                                "easy-to-understand words. "
                                "Assume the user is a beginner. "
                                "Use real-world examples when helpful. "
                                "Avoid unnecessary complexity. "
                                "Give clear and structured answers."
                            )
                        }
                    ] + st.session_state.messages
                )

                # Get AI response
                answer = response.choices[0].message.content

                # Display AI response
                st.markdown(answer)

                # Save AI response to chat history
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    "Sorry, something went wrong while connecting "
                    "to the AI. Please try again."
                )

                # Remove the user's message if the AI request failed
                st.session_state.messages.pop()