import streamlit as st
import requests  # Import requests to communicate with backend

# Backend API URL (Make sure Flask is running on this URL)
BACKEND_URL = "http://127.0.0.1:5000/"

st.title("Game Plan Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything about Game Plan System..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send user input to backend API
    try:
        response = requests.post(BACKEND_URL, json={"message": prompt})
        if response.status_code == 200:
            chatbot_response = response.json().get("response", "Sorry, I didn't understand that.")
        else:
            chatbot_response = "Error: Backend did not respond correctly."
    except requests.exceptions.RequestException:
        chatbot_response = "Error: Could not connect to backend."

    # Display chatbot response
    with st.chat_message("assistant"):
        st.markdown(chatbot_response)

    # Save response to chat history
    st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
