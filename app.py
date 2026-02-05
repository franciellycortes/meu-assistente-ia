import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

# 2. PERSONALIDADE DO MENTOR (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica, fundamentado na Epistemologia Convergente (Jorge Visca).
Analise os casos integrando: Piaget, Vygotsky, Wallon e Alicia Fernández.

ESTRUTURA DE RESPOSTA OBRIGATÓRIA:
1. Eixo Cognitivo: Estágio e funções executivas.
2. Eixo Socioafetivo: Mediação e vínculo com o saber.
3. Eixo Instrumental: Sugestão de testes (EOCA, Provas Operatórias).
4. Eixo Terapêutico: Hipóteses e estratégias práticas.
"""

# 3. CONEXÃO COM A API (CORREÇÃO DO ERRO 404)
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Chave API não configurada no Streamlit Secrets!")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Criamos o modelo de forma estável
        # Removendo qualquer configuração que force a versão 'beta'
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instrucao_sistema
        )
except Exception as e:
    st.error(f"Erro de conexão: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. INTERFACE (BARRA LATERAL)
with st.sidebar:
    st.title("📂 Painel Clínico")
    st.info("Modo Estável: Gemini 1.5 Flash")
    arquivo_upload = st.file_uploader("Subir PDF ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    
    if st.button("🗑️ Nova Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")

# 6. HISTÓRICO DE MENSAGENS
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
                # Leitura correta para PDFs
                conteudo_envio.append({
                    "mime_type": "application/pdf",
                    "data": arquivo_upload.getvalue()
                })
            else:
                # Leitura para imagens
                img = Image.open(arquivo_upload)
                conteudo_envio.append(img)

        with st.spinner("Analisando eixos clínicos..."):
            response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "404" in str(e):
            st.error("Erro 404: O modelo não foi reconhecido. Por favor, reinicie o app no painel do Streamlit (Reboot).")
        elif "429" in str(e):
            st.warning("Limite de cota atingido. Aguarde 60 segundos.")
        else:
            st.error(f"Ocorreu um erro: {e}")

