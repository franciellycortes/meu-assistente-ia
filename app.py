import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Mentor Neuropsicopedagógico Sênior", 
    page_icon="🧠", 
    layout="wide"
)

# Estilização para ambiente clínico
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
    .stChatMessage { border-radius: 12px; border: 1px solid #dee2e6; background-color: white; }
    h1 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE SÊNIOR (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor Sênior em Psicopedagogia e Neuropsicopedagogia Clínica. 
Sua atuação é uma síntese entre a Epistemologia Convergente, a Psicogenética (Piaget, Vygotsky, Wallon) e as Neurociências Aplicadas à Educação (Neuroaprendizagem). 
Seu foco é identificar as barreiras de aprendizagem sob a ótica biológica, cognitiva e emocional.

[DOMÍNIOS DE CONHECIMENTO ESPECÍFICOS]
- Habilidades Cognitivas: Funções Executivas (Memória de trabalho, controle inibitório, flexibilidade, planejamento), Sistemas Atencionais, Processamento Sensorial, Linguagem e Memória.
- Referencial Teórico-Clínico: Jorge Visca (Matrizes), Sara Paín (Dimensões), Alicia Fernández (Desejo/Saber), Nádia Bossa (Diagnóstico), Simone Sampaio (Prática/Testes).
- Desenvolvimento: Estágios de Piaget, ZDP de Vygotsky e a Motricidade/Afetividade de Wallon.
- Nosologia: Critérios do DSM-5-TR para Transtornos do Neurodesenvolvimento.

[DIRETRIZES DE RESPOSTA OBRIGATÓRIAS]
Para cada caso, siga obrigatoriamente esta estrutura:
1. PERFIL NEUROCOGNITIVO: Descreva habilidades cognitivas comprometidas ou preservadas.
2. LEITURA PSICOPEDAGÓGICA CLÁSSICA: Interprete o vínculo com a aprendizagem e o estágio de desenvolvimento.
3. AVALIAÇÃO INSTRUMENTAL SUGERIDA: Indique testes de Simone Sampaio ou Provas Operatórias.
4. ESTRATÉGIAS DE NEUROINTERVENÇÃO: Sugira atividades baseadas em Neuroplasticidade.

[RESTRIÇÕES] Mantenha o rigor terminológico e garanta a anonimização dos dados.
"""

# 3. CONEXÃO COM O GEMINI 1.5 FLASH
# Inicializamos a variável model como None para evitar erros de referência
model = None

try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("ERRO: Chave API não configurada nos Secrets do Streamlit.")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Configuração do modelo 1.5 Flash
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instrucao_sistema
        )
except Exception as e:
    st.error(f"Erro na conexão inicial: {e}")

# 4. GESTÃO DE MEMÓRIA (INDENTAÇÃO CORRIGIDA)
if model:
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
else:
    st.stop() # Interrompe o app se o modelo não carregar

# 5. BARRA LATERAL
with st.sidebar:
    st.title("📂 Central de Supervisão")
    st.info("Modelo: Gemini 1.5 Flash")
    arquivo_upload = st.file_uploader("Subir PDF ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    
    if st.button("🗑️ Nova Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico Sênior")
st.caption("Integração: Epistemologia Convergente & Neurociências")

# 6. HISTÓRICO
for msg in st.session_state.chat_session.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# 7. INTERAÇÃO
if prompt := st.chat_input("Descreva o caso clínico..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_envio = [prompt]
        
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                conteudo_envio.append({
                    "mime_type": "application/pdf",
                    "data": arquivo_upload.getvalue()
                })
            else:
                img = Image.open(arquivo_upload)
                conteudo_envio.append(img)

        with st.spinner("Analisando eixos clínicos..."):
            response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erro no processamento: {e}")
