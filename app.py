import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

# Estilo para um ambiente clínico acolhedor
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; background-color: white; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE TÉCNICA (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica, fundamentado na Epistemologia Convergente (Jorge Visca).
Integre: Piaget (Cognição), Vygotsky (ZDP), Wallon (Afetividade), Alicia Fernández (Desejo de Aprender) e Neurociências.

ESTRUTURA DE RESPOSTA OBRIGATÓRIA:
1. Eixo Cognitivo: Estágio e funções executivas.
2. Eixo Socioafetivo: Mediação e vínculo com o saber.
3. Eixo Instrumental: Sugestão de testes (EOCA, Provas Operatórias).
4. Eixo Terapêutico: Hipóteses e estratégias práticas.
"""

# 3. CONEXÃO COM A API (GEMINI 1.5 FLASH - ALTA PERFORMANCE)
try:
    CHAVE_API = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instrucao_sistema
    )
except Exception as e:
    st.error(f"Erro na configuração da API: {e}")

# 4. GESTÃO DE MEMÓRIA (CONTEXTO)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL (PAINEL CLÍNICO)
with st.sidebar:
    st.title("📂 Painel de Análise")
    st.info("Modelo: Gemini 1.5 Flash (Otimizado)")
    arquivo_upload = st.file_uploader("Subir Relatório (PDF) ou Exames (JPG/PNG)", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Nova Supervisão (Limpar)"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")
st.subheader("Consultoria Clínica Especializada")

# 6. EXIBIÇÃO DO HISTÓRICO
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 7. PROCESSAMENTO E INTERAÇÃO
if prompt := st.chat_input("Descreva o caso ou pergunte sobre o arquivo anexado..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_envio = [prompt]
        
        # Tratamento de Arquivos para evitar erro de 'mídia inválida'
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                # O Gemini 1.5 lê PDFs diretamente através de bytes
                pdf_data = arquivo_upload.read()
                conteudo_envio.append({"mime_type": "application/pdf", "data": pdf_data})
            else:
                # Tratamento de Imagens
                img = Image.open(arquivo_upload)
                conteudo_envio.append(img)

        # Resposta do Mentor
        with st.spinner("Analisando eixos clínicos..."):
            response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "429" in str(e):
            st.warning("Aguarde um instante. O sistema está processando as informações.")
        else:
            st.error(f"Erro no processamento: {e}")
