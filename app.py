import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Mentor Neuropsicopedagógico Sênior", 
    page_icon="🧠", 
    layout="wide"
)

# Estilização Clínica
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
    .stChatMessage { border-radius: 12px; border: 1px solid #dee2e6; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE SÊNIOR (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor Sênior em Psicopedagogia e Neuropsicopedagogia Clínica. 
Sua atuação é uma síntese entre a Epistemologia Convergente, a Psicogenética (Piaget, Vygotsky, Wallon) e as Neurociências Aplicadas à Educação (Neuroaprendizagem). 
Seu foco é identificar as barreiras de aprendizagem sob a ótica biológica, cognitiva e emocional.

[DIRETRIZES DE RESPOSTA OBRIGATÓRIAS]
1. PERFIL NEUROCOGNITIVO: Habilidades cognitivas comprometidas ou preservadas.
2. LEITURA PSICOPEDAGÓGICA CLÁSSICA: Vínculo com a aprendizagem e estágio de desenvolvimento.
3. AVALIAÇÃO INSTRUMENTAL SUGERIDA: Testes de Simone Sampaio ou Provas Operatórias.
4. ESTRATÉGIAS DE NEUROINTERVENÇÃO: Atividades baseadas em Neuroplasticidade.

[RESTRIÇÕES] Mantenha o rigor terminológico e garanta a anonimização.
"""

# 3. CONEXÃO COM O GEMINI 1.5 FLASH (CORREÇÃO DO ERRO 404)
model = None

try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("ERRO: Chave API não configurada nos Secrets do Streamlit.")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # O prefixo 'models/' força o uso da rota estável v1, evitando o erro 404 da v1beta
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash',
            system_instruction=instrucao_sistema
        )
except Exception as e:
    st.error(f"Erro na conexão inicial: {e}")

# 4. GESTÃO DE MEMÓRIA
if model:
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
else:
    st.warning("Aguardando configuração da API...")
    st.stop()

# 5. INTERFACE
st.title("🧠 Mentor Neuropsicopedagógico Sênior")

with st.sidebar:
    st.header("📂 Configurações")
    arquivo_upload = st.file_uploader("Subir PDF ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    if st.button("🗑️ Nova Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# Histórico
for msg in st.session_state.chat_session.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# Interação
if prompt := st.chat_input("Descreva o caso clínico..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_envio = [prompt]
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                conteudo_envio.append({"mime_type": "application/pdf", "data": arquivo_upload.getvalue()})
