import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTILO E CONFIGURAÇÃO
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE (DENTRO DE ASPAS TRIPLAS PARA EVITAR ERRO DE SINTAXE)
instrucao = """Você é um Mentor Sênior em Psicopedagogia Clínica (Epistemologia Convergente). 
Sempre responda usando estes 4 eixos: 
1. Eixo Cognitivo (Piaget/Neuro)
2. Eixo Socioafetivo (Vygotsky/Wallon/Fernández)
3. Eixo Instrumental (Sampaio/Visca)
4. Eixo Terapêutico (Hipóteses e Intervenção).
Trate dados de forma anônima."""

# 3. CONFIGURAÇÃO DA API (MODELO CORRIGIDO)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Usamos apenas 'gemini-1.5-flash' sem o prefixo 'models/' para evitar o Erro 404
    model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instrucao)
except Exception as e:
    st.error(f"Erro de configuração: {e}")

# 4. CHAT E MEMÓRIA
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🧠 Mentor Neuropsicopedagógico")

# Exibir histórico
for msg in st.session_state.chat.history:
    with st.chat_message("user" if msg.role == "user" else "assistant"):
        st.markdown(msg.parts[0].text)

# 5. ENTRADA DO USUÁRIO
if prompt := st.chat_input("Descreva o caso..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        if "429" in str(e):
            st.warning("O Google está lotado (Erro 429). Aguarde 1 minuto sem clicar em nada e tente de novo.")
        else:
            st.error(f"Ocorreu um erro: {e}")
