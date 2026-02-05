import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Assistente Multimodal", page_icon="📸", layout="centered")

# Estilos CSS (Cores pastéis)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    </style>
    """, unsafe_allow_html=True)

# Conexão com a API
CHAVE_API = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=CHAVE_API)
model = genai.GenerativeModel('models/gemini-3-flash-preview')

# Barra Lateral com Upload
with st.sidebar:
    st.title("📁 Arquivos")
    arquivo_upload = st.file_uploader("Suba uma imagem ou PDF", type=["png", "jpg", "jpeg", "pdf"])
    
    if st.button("Limpar Histórico"):
        st.session_state.chat = []
        st.rerun()

st.title("✨ Assistente Inteligente")
st.subheader("Envie fotos ou documentos para eu analisar!")

if "chat" not in st.session_state:
    st.session_state.chat = []

# Exibir histórico
for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Lógica de interação
if prompt := st.chat_input("O que deseja saber sobre o arquivo?"):
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_para_enviar = [prompt]
        
        # Se houver um arquivo, adicionamos ele à lista de envio
        if arquivo_upload is not None:
            if arquivo_upload.type == "application/pdf":
                # Para PDF, usamos os bytes diretamente
                pdf_data = arquivo_upload.read()
                conteudo_para_enviar.append({"mime_type": "application/pdf", "data": pdf_data})
            else:
                # Para imagem, usamos a biblioteca PIL
                img = Image.open(arquivo_upload)
                conteudo_para_enviar.append(img)

        response = model.generate_content(conteudo_para_enviar)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.chat.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Erro ao processar: {e}")
