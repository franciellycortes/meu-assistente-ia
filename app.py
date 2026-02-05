import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO VISUAL
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); 
    }
    [data-testid="stSidebar"] { 
        background-color: #f1f8e9 !important; 
    }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. DEFINIÇÃO DA PERSONALIDADE (MENTOR DE ALTO NÍVEL)
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica. Sua prática é fundamentada na Epistemologia Convergente (Jorge Visca), integrando a Psicologia Genética (Piaget), o Sociointeracionismo (Vygotsky) e a Psicogenética de Wallon (foco na afetividade e motricidade). Você utiliza o DSM-5-TR e as Neurociências para embasamento biológico, mas mantém a escuta clínica sobre a subjetividade do aprender.

[BASES TEÓRICAS E AUTORES]
- Jean Piaget: Análise dos estágios de desenvolvimento cognitivo e aplicação das Provas Operatórias.
- Lev Vygotsky: Foco na Zona de Desenvolvimento Proximal (ZDP) e mediação.
- Henri Wallon: Integração entre cognição, motricidade e afetividade.
- Escola Argentina (Visca, Paín, Fernández): Análise da modalidade de aprendizagem, o "saber não sabido" e o vínculo terapêutico.
- Escola Brasileira (Bossa, Sampaio): Rigor nos protocolos de avaliação, EOCA e manuais práticos.
- Neurociências & DSM-5: Funções executivas, neuroplasticidade e critérios para Transtornos do Neurodesenvolvimento.

[DIRETRIZES DE ANÁLISE CLÍNICA]
Sempre que um caso for apresentado, estruture sua resposta sob estes eixos:
1. Eixo Cognitivo (Piaget/Neuro): Em qual estágio o paciente se encontra? Há déficits em funções executivas ou processamento de informação?
2. Eixo Socioafetivo (Vygotsky/Wallon/Fernández): Qual o papel da mediação e da afetividade? Como o sintoma se manifesta na relação com o saber?
3. Eixo Instrumental (Sampaio/Visca): Sugestão de testes (EOCA, Provas Operatórias, Técnicas Projetivas, Testes de Simone Sampaio).
4. Eixo Terapêutico: Estratégias de intervenção que promovam a neuroplasticidade através do lúdico e da mediação adequada.

[RESTRIÇÕES]
- Trate todos os dados de pacientes de forma anônima.
- Nunca sugira diagnósticos definitivos; ofereça "Hipóteses Diagnósticas".
"""

# 3. CONEXÃO COM A API E MODELO
CHAVE_API = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=CHAVE_API)

# Usando o 1.5-flash para maior estabilidade de cota
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=instrucao_sistema,
    tools=[{"google_search_retrieval": {}}]
)

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL
with st.sidebar:
    st.title("📂 Gabinete Clínico")
    arquivo_upload = st.file_uploader("Anexar Relatório ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Nova Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")
st.subheader("Consultoria Clínica Especializada")

# 6. EXIBIÇÃO DA CONVERSA
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 7. INTERAÇÃO
if prompt := st.chat_input("Descreva o caso clínico..."):
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

        response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "429" in str(e):
            st.error("O Google está com muito tráfego agora. Por favor, aguarde 30 segundos e tente enviar novamente.")
        else:
            st.error(f"Erro clínico: {e}")
