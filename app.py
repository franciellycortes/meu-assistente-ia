import streamlit as st
import google.generativeai as genai

# Configuração da página com cores claras
st.set_page_config(
    page_title="Meu Chat Colorido", 
    page_icon="🌸", 
    layout="centered"
)

# Estilos personalizados (CSS) com tons claros de Azul, Rosa, Roxo e Verde
st.markdown("""
    <style>
    /* Fundo da página com degradê suave */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%);
    }
    
    /* Cor do Título */
    h1 {
        color: #6a1b9a !important; /* Roxo suave */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Estilizando a barra lateral */
    [data-testid="stSidebar"] {
        background-color: #f1f8e9 !important; /* Verde bem clarinho */
    }

    /* Botão de limpar */
    .stButton>button {
        background-color: #bbdefb; /* Azul claro */
        color: #0d47a1;
        border-radius: 20px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Barra Lateral (Verde Claro)
with st.sidebar:
    st.title("🎨 Visual Personalizado")
    st.write("Cores: Azul, Rosa, Roxo e Verde (Tons Claros)")
    if st.button("Limpar Conversa"):
        st.session_state.chat = []
        st.rerun()

# Título Principal
st.title("✨ Assistente Francielly")
st.subheader("Sua IA personalizada em tons pastéis")

# Conexão segura com a chave (Secrets)
CHAVE_API = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=CHAVE_API)
model = genai.GenerativeModel('models/gemini-3-flash-preview')

if "chat" not in st.session_state:
    st.session_state.chat = []

# Exibição das mensagens
for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Diga olá para sua nova IA..."):
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.chat.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

