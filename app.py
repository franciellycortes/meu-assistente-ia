import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

# Estilo visual para manter o tom profissional e acolhedor
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; background-color: white; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE DO MENTOR
# Usamos uma variável simples para evitar erros de aspas
instrucao = (
    "Você é um Mentor Sênior em Psicopedagogia Clínica. "
    "Sempre responda estruturando em 4 eixos: 1. Eixo Cognitivo, "
    "2. Eixo Socioafetivo, 3. Eixo Instrumental, 4. Eixo Terapêutico. "
    "Use referências de Visca, Piaget, Vygotsky e Wallon."
)

# 3. CONEXÃO COM A API (AQUI ESTAVA O ERRO 404)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Chamada direta e simples para evitar o erro 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 4. MEMÓRIA DO CHAT
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 5. BARRA LATERAL (PAINEL CLÍNICO)
with st.sidebar:
    st.title("📂 Painel Clínico")
    arquivo = st.file_uploader("Anexar Exames ou Fotos", type=["png", "jpg", "jpeg", "pdf"])
    st.divider()
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")

# Exibir histórico
for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# 6. ENTRADA E PROCESSAMENTO
if prompt := st.chat_input("Descreva o caso do paciente aqui..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Enviamos a instrução de sistema junto com o prompt para garantir a personalidade
        full_prompt = f"Instrução: {instrucao}\n\nPaciente: {prompt}"
        
        # Envio de mensagem
        response = st.session_state.chat.send_message(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "429" in str(e):
            st.warning("O Google está ocupado. Espere 1 minuto e tente de novo.")
        else:
            st.error(f"Erro clínico: {e}")
