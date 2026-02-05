import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = (
    "Você é um Mentor Sênior em Psicopedagogia Clínica (Epistemologia Convergente). "
    "Sempre responda estruturando em 4 eixos: 1. Eixo Cognitivo (Piaget/Neuro), "
    "2. Eixo Socioafetivo (Vygotsky/Wallon/Fernández), 3. Eixo Instrumental (Sampaio/Visca), "
    "4. Eixo Terapêutico (Hipóteses e Intervenção). Trate dados de forma anônima."
)

# 3. CONEXÃO COM A API
try:
    CHAVE_API = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    
    # Modelo atualizado para a versão estável (sem prefixo v1beta)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instrucao_sistema
    )
except Exception as e:
    st.error(f"Erro na API: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL (Painel Clínico)
with st.sidebar:
    st.title("📂 Painel Clínico")
    arquivo_upload = st.file_uploader("Subir PDF ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Limpar Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")
st.subheader("Consultoria Clínica Especializada")

# 6. EXIBIÇÃO DO HISTÓRICO
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 7. INTERAÇÃO
if prompt := st.chat_input("Descreva o caso do paciente..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_envio = [prompt]
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                conteudo_envio.append({"mime_type": "application/pdf", "data": arquivo_upload.read()})
            else:
                conteudo_envio.append(Image.open(arquivo_upload))

        response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "429" in str(e):
            st.warning("Muitas tentativas seguidas. Aguarde 60 segundos para o Google liberar seu acesso gratuito.")
        else:
            st.error(f"Ocorreu um erro: {e}")
