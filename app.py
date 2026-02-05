import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA E VISUAL
st.set_page_config(page_title="Central IA Francielly", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO E FERRAMENTAS (Google Search)
CHAVE_API = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=CHAVE_API)

# Aqui ativamos a "Personalidade" e a "Pesquisa Google"
instrucao_sistema = "Você é o Assistente da Francielly. Você é inteligente, gentil e sempre busca informações atualizadas. Se não souber algo, use a pesquisa do Google."

model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=instrucao_sistema,
    tools=[{"google_search_retrieval": {}}] # Ativa a pesquisa em tempo real
)

# 3. MEMÓRIA (Estado da Sessão)
if "chat_session" not in st.session_state:
    # Inicia a sessão de chat com memória nativa do Google
    st.session_state.chat_session = model.start_chat(history=[])

# 4. BARRA LATERAL
with st.sidebar:
    st.title("🛠️ Painel de Funções")
    arquivo_upload = st.file_uploader("Analisar Imagem ou PDF", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Limpar Memória"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    # Função de Download do Histórico
    if len(st.session_state.chat_session.history) > 0:
        texto_chat = ""
        for msg in st.session_state.chat_session.history:
            texto_chat += f"{msg.role}: {msg.parts[0].text}\n"
        st.download_button("📥 Baixar Conversa", texto_chat, file_name="conversa_ia.txt")

st.title("✨ Minha IA Completa")

# 5. EXIBIR HISTÓRICO (Memória de Contexto)
for mensagem in st.session_state.chat_session.history:
    with st.chat_message("user" if mensagem.role == "user" else "assistant"):
        st.markdown(mensagem.parts[0].text)

# 6. LÓGICA DE INTERAÇÃO
if prompt := st.chat_input("Como posso ajudar hoje?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_envio = [prompt]
        
        # Processamento de Arquivos
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                conteudo_envio.append({"mime_type": "application/pdf", "data": arquivo_upload.read()})
            else:
                img = Image.open(arquivo_upload)
                conteudo_envio.append(img)

        # Resposta com Memória e Pesquisa
        response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erro: {e}")
