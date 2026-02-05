import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP INICIAL
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠")

# 2. PERSONALIDADE
instrucao = (
    "Você é um Mentor em Psicopedagogia Clínica (Epistemologia Convergente). "
    "Analise sob 4 eixos: Cognitivo, Socioafetivo, Instrumental e Terapêutico."
)

# 3. CONEXÃO DIRETA (SEM PREFIXOS)
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Chave API não encontrada no Streamlit Secrets!")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Aqui está o segredo: chamamos o modelo de forma simplificada
        model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 4. MEMÓRIA
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 5. BARRA LATERAL
with st.sidebar:
    st.title("📂 Painel")
    arquivo = st.file_uploader("Subir arquivo", type=["png", "jpg", "jpeg", "pdf"])

st.title("🧠 Mentor Neuropsicopedagógico")

# 6. EXIBIÇÃO
for msg in st.session_state.chat.history:
    with st.chat_message("user" if msg.role == "user" else "assistant"):
        st.markdown(msg.parts[0].text)

# 7. INTERAÇÃO
if prompt := st.chat_input("Descreva o caso..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Enviamos a instrução de personalidade junto com cada prompt para segurança
        full_query = f"Instrução: {instrucao}\n\nCaso: {prompt}"
        
        conteudo = [full_query]
        if arquivo:
            if arquivo.type == "application/pdf":
                conteudo.append({"mime_type": "application/pdf", "data": arquivo.read()})
            else:
                conteudo.append(Image.open(arquivo))

        response = st.session_state.chat.send_message(conteudo)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erro detalhado: {e}")

