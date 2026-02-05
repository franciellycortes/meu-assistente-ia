import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); }
    [data-testid="stSidebar"] { background-color: #f1f8e9 !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. DEFINIÇÃO DA PERSONALIDADE E DIRETRIZES OPERACIONAIS
instrucao_sistema = """
Age como um Mentor Clínico Sénior. A tua personalidade é caracterizada pela precisão analítica (Neurociências) mas com uma escuta profundamente humanizada e ética (Escola Argentina). Não dás respostas genéricas; és detalhista, citas conceitos dos autores definidos (ex: 'ZDP', 'Matrizes de Pensamento', 'Funções Executivas') e manténs um tom de parceria profissional com o utilizador.

Diretriz Operacional: Tu és o Consultor Neuropsicopedagógico da Francielly. O teu objetivo é elevar a qualidade da prática clínica dela. Nunca ignores a intersecção entre a neurobiologia e a subjetividade. Prioriza autores de língua portuguesa e castelhana (Visca, Fernández, Bossa, Sampaio) em conjunto com os avanços das neurociências mundiais.

ALGORITMO MENTAL (Fluxo de Trabalho):
- Fase 1: Escuta e Recolha: Se o utilizador fornecer poucos dados, pergunta sobre os marcos do desenvolvimento, a dinâmica familiar ou o histórico escolar antes de fechar uma hipótese.
- Fase 2: Integração Teórica: Cruza sempre o biológico (DSM-5) com o pedagógico (Sampaio) e o afetivo (Wallon/Fernández).
- Fase 3: Sugestão Prática: Toda a teoria deve terminar numa sugestão prática de intervenção que possa ser aplicada na próxima sessão.

FORMATO DE RESPOSTA:
- Utiliza títulos em negrito e listas de tópicos.
- Se houver divergência entre autores (ex: uma visão estritamente orgânica vs. uma visão psicodramática), apresenta ambos os pontos de vista para que o utilizador possa decidir o que melhor se aplica ao paciente.
"""

# 3. CONEXÃO COM A API
CHAVE_API = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=CHAVE_API)

model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=instrucao_sistema,
    tools=[{"google_search_retrieval": {}}]
)

# 4. GESTÃO DE MEMÓRIA (CHAT)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL (PAINEL CLÍNICO)
with st.sidebar:
    st.title("📂 Gabinete Clínico")
    arquivo_upload = st.file_uploader("Anexar Relatório, Imagem ou Atividade", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Nova Supervisão (Limpar)"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    if len(st.session_state.chat_session.history) > 0:
        texto_chat = ""
        for msg in st.session_state.chat_session.history:
            texto_chat += f"{msg.role.upper()}: {msg.parts[0].text}\n\n"
        st.download_button("📥 Exportar Relato de Supervisão", texto_chat, file_name="supervisao_clinica.txt")

st.title("🧠 Mentor Neuropsicopedagógico")
st.subheader("Consultoria Clínica Especializada")

# 6. EXIBIÇÃO DA CONVERSA
for mensagem in st.session_state.chat_session.history:
    with st.chat_message("user" if mensagem.role == "user" else "assistant"):
        st.markdown(mensagem.parts[0].text)

# 7. INTERAÇÃO E PROCESSAMENTO
if prompt := st.chat_input("Descreve o caso ou coloca a tua dúvida técnica..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_envio = [prompt]
        
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                conteudo_envio.append({"mime_type": "application/pdf", "data": arquivo_upload.read()})
            else:
                img = Image.open(arquivo_upload)
                conteudo_envio.append(img)

        # Resposta com o "Algoritmo Mental" ativado
        response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erro clínico: {e}")

