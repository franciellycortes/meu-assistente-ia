import streamlit as st
import google.generativeai as genai

# O Streamlit vai ler automaticamente o arquivo secrets.toml que você acabou de criar
CHAVE_API = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=CHAVE_API)
model = genai.GenerativeModel('models/gemini-3-flash-preview')

st.set_page_config(page_title="Meu Assistente Seguro", page_icon="🛡️")
st.title("🤖 Assistente Gemini 3")

if "chat" not in st.session_state:
    st.session_state.chat = []

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Como posso ajudar hoje?"):
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.chat.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erro: {e}")