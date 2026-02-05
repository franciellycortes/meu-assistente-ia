import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠")

# 2. PERSONALIDADE
instrucao = (
    "Você é um Mentor Sênior em Psicopedagogia Clínica. "
    "Estruture as respostas em 4 eixos: Cognitivo, Socioafetivo, Instrumental e Terapêutico."
)

# 3. CONEXÃO COM A API (AJUSTADO PARA GEMINI 2.0)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Mudança aqui: Nome oficial para o Gemini 2.0
    model = genai.GenerativeModel('gemini-2.0-flash') 
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 4. CHAT
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🧠 Mentor Gemini 2.0")

# 5. BARRA LATERAL
with st.sidebar:
    st.title("📂 Painel Clínico")
    arquivo = st.file_uploader("Subir arquivo", type=["png", "jpg", "jpeg", "pdf"])

# 6. PROCESSAMENTO
if prompt := st.chat_input("Descreva o caso..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # No 2.0, a instrução vai dentro do envio se não configurada no Model
        full_prompt = f"{instrucao}\n\nCaso: {prompt}"
        response = st.session_state.chat.send_message(full_prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        if "429" in str(e):
            st.warning("ERRO DE COTA: O Gemini 2.0 Gratuito tem limites baixos. Tente mudar para 'gemini-1.5-flash' no código se este erro persistir.")
        else:
            st.error(f"Erro: {e}")

