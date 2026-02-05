import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica. Sua prática é fundamentada na Epistemologia Convergente (Jorge Visca), integrando Piaget, Vygotsky e Wallon. Utilize o DSM-5-TR e as Neurociências para embasamento biológico, mas mantenha a escuta clínica sobre a subjetividade do aprender.

ESTRUTURA DE RESPOSTA OBRIGATÓRIA:
1. Eixo Cognitivo (Piaget/Neuro): Estágio de desenvolvimento e funções executivas.
2. Eixo Socioafetivo (Vygotsky/Wallon/Fernández): Papel da mediação e afetividade.
3. Eixo Instrumental (Sampaio/Visca): Sugestão de testes (EOCA, Provas Operatórias, etc).
4. Eixo Terapêutico: Hipóteses Diagnósticas e sugestões de intervenção prática.

RESTRIÇÕES: Trate dados de forma anônima e nunca dê diagnósticos definitivos; ofereça apenas Hipóteses Diagnósticas.
"""

# 3. CONEXÃO COM A API
try:
    CHAVE_API = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    
    # Modelo configurado corretamente para evitar erro 404
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instrucao_sistema
    )
except Exception as e:
    st.error(f"Erro na configuração da API: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL
with st.sidebar:
    st.title("📂 Painel Clínico")
    arquivo_upload = st.file_uploader("Subir PDF ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    if st.button("🗑️ Limpar Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")
st.subheader("Consultoria Clínica Especializada")

# 6. EXIBIÇÃO DA CONVERSA
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 7. INTERAÇÃO
if prompt := st.chat_input("Descreva o caso do paciente..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo = [prompt]
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                conteudo.append({"mime_type": "application/pdf", "data": arquivo_upload.read()})
            else:
                conteudo.append(Image.open(arquivo_upload))

        response = st.session_state.chat_session.send_message(conteudo)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "429" in str(e):
            st.warning("O Google está processando muitas requisições. Aguarde 30 segundos e tente novamente.")
        else:
            st.error(f"Ocorreu um problema: {e}")
