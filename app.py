import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

# 2. PERSONALIDADE (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica (Epistemologia Convergente).
Estruture suas respostas em 4 eixos: 
1. Eixo Cognitivo
2. Eixo Socioafetivo
3. Eixo Instrumental
4. Eixo Terapêutico
"""

# 3. CONEXÃO BLINDADA (AQUI ESTÁ A CORREÇÃO)
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Chave API não encontrada!")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Tentamos a chamada direta. O erro 404 ocorre quando o código 
        # tenta usar 'models/gemini-1.5-flash'. Vamos usar apenas o nome:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instrucao_sistema
        )
except Exception as e:
    st.error(f"Erro na configuração: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. INTERFACE
st.title("🧠 Mentor Neuropsicopedagógico")

with st.sidebar:
    st.title("📂 Painel Clínico")
    arquivo_upload = st.file_uploader("Subir PDF ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    if st.button("🗑️ Nova Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# Histórico
for msg in st.session_state.chat_session.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# 6. INTERAÇÃO
if prompt := st.chat_input("Descreva o caso clínico..."):
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
        # Se der erro 404 novamente, o código vai imprimir o erro técnico exato para investigarmos
        st.error(f"Erro técnico encontrado: {e}")


