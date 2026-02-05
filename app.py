import streamlit as st
import google.generativeai as genai

# Configuração da página (Isso muda o título na aba do navegador e o ícone)
st.set_page_config(
    page_title="Gemini PRO 2026", 
    page_icon="🔥", 
    layout="centered"
)

# Estilo CSS para mudar a cor do cabeçalho (Opcional)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    h1 {
        color: #4facfe;
    }
    </style>
    """, unsafe_allow_html=True)

# Barra Lateral
with st.sidebar:
    st.title("⚙️ Configurações")
    st.info("Este assistente utiliza o modelo Gemini 3 Flash da Google.")
    if st.button("Limpar Histórico"):
        st.session_state.chat = []
        st.rerun()

# Título Principal
st.title("🚀 Meu Super Assistente")
st.subheader("IA de Última Geração")

# --- O restante do código de conexão e chat continua igual ---
CHAVE_API = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=CHAVE_API)
model = genai.GenerativeModel('models/gemini-3-flash-preview')

if "chat" not in st.session_state:
    st.session_state.chat = []

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Pergunte qualquer coisa..."):
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.chat.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erro: {e}")
