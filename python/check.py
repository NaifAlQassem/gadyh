import streamlit as st
from openai import OpenAI

with st.sidebar:
    openai_api_key = st.text_input("Add your OpenAI API key", key="chatbot_api_key", type="password")
    
st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "كيف أستطيع مساعدتك؟"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Modify prompt to instruct the assistant to respond in Arabic
    arabic_prompt = f"أجب باللغة العربية: {prompt}"
    
    client = OpenAI(api_key=openai_api_key)
    
    # Append user's input (modified to request Arabic response) to session state messages
    st.session_state.messages.append({"role": "user", "content": arabic_prompt})
    st.chat_message("user").write(prompt)  # Display original prompt in the chat

    # Send the prompt to the model
    response = client.chat_completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    # Extract the assistant's response and add it to the session state
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
