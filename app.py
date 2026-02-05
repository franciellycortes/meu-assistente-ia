import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; background-color: white; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE (INSTRUÇÃO SIMPLIFICADA PARA EVITAR ERRO DE SINTAXE)
instrucao = (
    "Você é um Mentor Sênior em Psicopedagogia Clínica. "
    "Sempre responda estruturando em 4 eixos: 1. Eixo Cognitivo, "
    "2. Eixo Socioafetivo, 3. Eixo Instrumental, 4. Eixo Terapêutico. "
    "Baseie-se em Visca, Piaget, Vygotsky e Wallon."
)

# 3. CONEXÃO COM A API (CORREÇÃO DO ERRO 404)
try:
    CHAVE_API = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    # Chamada sem o prefixo 'models/' e sem forçar v1beta
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL (PAINEL CLÍNICO)
with st.sidebar:
    st.title("📂 Painel Clínico")
    st.write("Carregue documentos ou imagens abaixo:")
    arquivo_upload = st.file_uploader("Subir Arquivo", type=["png", "jpg", "jpeg", "pdf"])
    st.divider()
    if st.button("🗑️ Limpar Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")
st.subheader("Consultoria Clínica Especializada")

# Exibição do histórico
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 6. INTERAÇÃO E TRATAMENTO DE ERROS (ERRO 429)
if prompt := st.chat_input("Descreva o caso do paciente..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Mesclamos a instrução com o prompt para garantir a personalidade
        prompt_completo = f"{instrucao}\n\nAnalise o seguinte caso: {prompt}"
        
        response = st.session_state.chat_session.send_message(prompt_completo)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "429" in str(e):
            st.warning("O Google excedeu o limite de uso temporário. Aguarde 2 minutos e tente reenviar.")
        else:
            st.error(f"Ocorreu um problema: {e}")
