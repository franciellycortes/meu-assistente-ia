import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

# Estilo Visual
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; background-color: white; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE TÉCNICA
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica, fundamentado na Epistemologia Convergente (Jorge Visca).
Sua análise deve integrar Piaget, Vygotsky, Wallon e Alicia Fernández.

ESTRUTURA OBRIGATÓRIA DE RESPOSTA:
1. Eixo Cognitivo (Piaget/Neuro): Estágio e funções executivas.
2. Eixo Socioafetivo (Vygotsky/Wallon/Fernández): Mediação e vínculo.
3. Eixo Instrumental (Sampaio/Visca): Sugestão de testes (EOCA, Provas Operatórias).
4. Eixo Terapêutico: Hipóteses e estratégias práticas.
"""

# 3. CONEXÃO COM A API (ESTÁVEL)
try:
    CHAVE_API = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    
    # Mudança para evitar o erro 404: usamos o modelo sem o prefixo v1beta
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instrucao_sistema
    )
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL
with st.sidebar:
    st.title("📂 Painel Clínico")
    st.info("Modelo Estável: Gemini 1.5 Flash")
    arquivo_upload = st.file_uploader("Subir Relatório ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Nova Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")

# 6. HISTÓRICO
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 7. INTERAÇÃO E PROCESSAMENTO
if prompt := st.chat_input("Descreva o caso clínico..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_envio = [prompt]
        
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                # Tratamento específico para PDF enviado como documento
                conteudo_envio.append({
                    "mime_type": "application/pdf",
                    "data": arquivo_upload.getvalue()
                })
            else:
                img = Image.open(arquivo_upload)
                conteudo_envio.append(img)

        with st.spinner("Analisando eixos clínicos..."):
            # Envio forçando o uso do modelo configurado
            response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "404" in str(e):
            st.error("Erro 404: O sistema não encontrou o modelo. Verifique se o arquivo 'requirements.txt' está atualizado no seu GitHub.")
        elif "429" in str(e):
            st.warning("Limite de cota atingido. Aguarde 60 segundos.")
        else:
            st.error(f"Erro no processamento: {e}")
