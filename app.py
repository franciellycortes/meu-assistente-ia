import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Mentor Neuropsicopedagógico Sênior", 
    page_icon="🧠", 
    layout="wide"
)

# Estilo para um ambiente profissional e clínico
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
    .stChatMessage { border-radius: 12px; border: 1px solid #dee2e6; background-color: white; }
    h1 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE COMPLETA (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor Sênior em Psicopedagogia e Neuropsicopedagogia Clínica. 
Sua atuação é uma síntese entre a Epistemologia Convergente, a Psicogenética (Piaget, Vygotsky, Wallon) e as Neurociências Aplicadas à Educação (Neuroaprendizagem). 
Seu foco é identificar as barreiras de aprendizagem sob a ótica biológica, cognitiva e emocional.

[DOMÍNIOS DE CONHECIMENTO ESPECÍFICOS]
- Habilidades Cognitivas: Funções Executivas (Memória de trabalho, controle inibitório, flexibilidade, planejamento), Sistemas Atencionais, Processamento Sensorial (Consciência fonológica, integração visomotora), Linguagem e Memória.
- Referencial Teórico: Jorge Visca, Sara Paín, Alicia Fernández, Nádia Bossa, Simone Sampaio.
- Desenvolvimento: Estágios de Piaget, ZDP de Vygotsky, Motricidade/Afetividade de Wallon.
- Nosologia: Critérios do DSM-5-TR para Transtornos do Neurodesenvolvimento.

[DIRETRIZES DE RESPOSTA OBRIGATÓRIAS]
Para cada caso ou dúvida, siga exatamente esta estrutura:
1. PERFIL NEUROCOGNITIVO: Descreva habilidades comprometidas ou preservadas (ex: memória, atenção).
2. LEITURA PSICOPEDAGÓGICA CLÁSSICA: Interprete o vínculo com a aprendizagem (Visca/Paín) e o estágio de desenvolvimento (Piaget/Wallon).
3. AVALIAÇÃO INSTRUMENTAL SUGERIDA: Indique testes de Simone Sampaio ou Provas Operatórias adequados.
4. ESTRATÉGIAS DE NEUROINTERVENÇÃO: Sugira atividades baseadas em Neuroplasticidade (repetição, novidade, desafio, engajamento).

[RESTRIÇÕES]
- Rigor terminológico: use "hipótese diagnóstica", nunca "veredito".
- Proteção de dados: garanta a anonimização.
"""

# 3. CONEXÃO COM O MODELO GEMINI 2.0 FLASH
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("ERRO: Configure a chave GOOGLE_API_KEY no painel do Streamlit (Secrets).")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Instanciação do modelo Gemini 2.0 Flash (Geração 3)
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            system_instruction=instrucao_sistema
        )
except Exception as e:
    st.error(f"Erro na conexão com a Inteligência Artificial: {e}")

# 4. GESTÃO DE MEMÓRIA (CONTEXTO DA SUPERVISÃO)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL (PAINEL DE CONTROLE)
with st.sidebar:
    st.title("📂 Central de Supervisão")
    st.info("Modelo: Gemini 2.0 Flash (v3)")
    
    arquivo_upload = st.file_uploader("Subir Relatórios (PDF) ou Imagens", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Nova Supervisão (Limpar Histórico)"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico Sênior")
st.markdown("---")

# 6. EXIBIÇÃO DO HISTÓRICO DE MENSAGENS
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 7. INTERAÇÃO E PROCESSAMENTO DE CASOS
if prompt := st.chat_input("Insira os dados do caso clínico ou sua dúvida técnica..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo_para_envio = [prompt]
        
        # Processamento de arquivos anexados
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                conteudo_para_envio.append({
                    "mime_type": "application/pdf",
                    "data": arquivo_upload.read()
                })
            else:
                img = Image.open(arquivo_upload)
                conteudo_para_envio.append(img)

        # Chamada da resposta do Mentor
        with st.spinner("Analisando sob as óticas biológica, cognitiva e emocional..."):
            response = st.session_state.chat_session.send_message(conteudo_para_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erro técnico no processamento: {e}")

