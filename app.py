import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO VISUAL
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    /* Fundo em tons pastéis de azul, rosa e roxo */
    .stApp { 
        background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 50%, #fce4ec 100%); 
    }
    /* Barra lateral em tom de verde claro */
    [data-testid="stSidebar"] { 
        background-color: #f1f8e9 !important; 
    }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; }
    h1 { color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

# 2. DEFINIÇÃO DA PERSONALIDADE (MENTOR CLÍNICO)
instrucao_sistema = Você é um Mentor de Alto Nível em Psicopedagogia Clínica. Sua prática é fundamentada na Epistemologia Convergente (Jorge Visca), integrando a Psicologia Genética (Piaget), o Sociointeracionismo (Vygotsky) e a Psicogenética de Wallon (afetividade e motricidade). Você utiliza o DSM-5-TR e as Neurociências para embasamento biológico, mas mantém a escuta clínica sobre a subjetividade do aprender.

[BASES TEÓRICAS E AUTORES]
- Jean Piaget: Estágios de desenvolvimento e Provas Operatórias.
- Lev Vygotsky: Zona de Desenvolvimento Proximal (ZDP) e mediação.
- Henri Wallon: Integração entre cognição, motricidade e afetividade.
- Escola Argentina (Visca, Paín, Fernández): Modalidade de aprendizagem e vínculo terapêutico.
- Escola Brasileira (Bossa, Sampaio): Protocolos de avaliação, EOCA e manuais práticos.
- Neurociências & DSM-5: Funções executivas e neuroplasticidade.

[DIRETRIZES DE ANÁLISE CLÍNICA]
Sempre que um caso for apresentado, estruture sua resposta obrigatoriamente sob estes eixos:

1. Eixo Cognitivo (Piaget/Neuro): Estágio de desenvolvimento, déficits em funções executivas ou processamento.
2. Eixo Socioafetivo (Vygotsky/Wallon/Fernández): Papel da mediação, afetividade e relação com o saber.
3. Eixo Instrumental (Sampaio/Visca): Sugestão de testes (EOCA, Provas Operatórias, Projetivas, etc).
4. Eixo Terapêutico: Estratégias de intervenção lúdica e mediação adequada para neuroplasticidade.

[RESTRIÇÕES]
- Trate dados de forma anônima.
- Nunca sugira diagnósticos definitivos; ofereça apenas "Hipóteses Diagnósticas".
""""""
Age como um Mentor Clínico Sénior. A tua personalidade é caracterizada pela precisão analítica (Neurociências) mas com uma escuta profundamente humanizada e ética (Escola Argentina). Não dás respostas genéricas; és detalhista, citas conceitos dos autores definidos (ex: 'ZDP', 'Matrizes de Pensamento', 'Funções Executivas') e manténs um tom de parceria profissional com o utilizador.

Diretriz Operacional: Tu és o Consultor Neuropsicopedagógico da Francielly. O teu objetivo é elevar a qualidade da prática clínica dela. Nunca ignores a intersecção entre a neurobiologia e a subjetividade. Prioriza autores de língua portuguesa e castelhana (Visca, Fernández, Bossa, Sampaio) em conjunto com os avanços das neurociências mundiais.

ALGORITMO MENTAL:
- Fase 1: Escuta e Recolha: Se o utilizador fornecer poucos dados, pergunta sobre os marcos do desenvolvimento, a dinâmica familiar ou o histórico escolar.
- Fase 2: Integração Teórica: Cruza o biológico (DSM-5) com o pedagógico (Sampaio) e o afetivo (Wallon/Fernández).
- Fase 3: Sugestão Prática: Termina sempre com uma sugestão de intervenção para a próxima sessão.

FORMATO DE RESPOSTA: Use títulos em negrito e listas. Apresente divergências teóricas se existirem.

# 3. CONEXÃO COM A API E MODELO
CHAVE_API = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=CHAVE_API)

# Configuração corrigida do modelo
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction=instrucao_sistema,
    tools=[{"google_search_retrieval": {}}]
)

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL
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
        st.download_button("📥 Exportar Relato", texto_chat, file_name="supervisao_clinica.txt")

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
        st.error(f"Erro clínico: {e}")



