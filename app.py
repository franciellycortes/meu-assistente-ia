import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico v3", page_icon="🧠", layout="wide")

# Estilo visual para ambiente clínico
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stChatMessage { border-radius: 15px; border: 1px solid #d1d9e6; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE COMPLETA (EPISTEMOLOGIA CONVERGENTE)
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica, com expertise profunda na Epistemologia Convergente de Jorge Visca. 
Sua função é supervisionar casos clínicos integrando as três linhas de convergência:

1. ESCOLA GENÉTICA (Piaget): Análise dos estágios do desenvolvimento cognitivo e das Provas Operatórias.
2. ESCOLA PSICANALÍTICA (Freud/Alicia Fernández): Análise da modalidade de aprendizagem, o desejo de saber e o vínculo com o objeto de conhecimento.
3. PSICOLOGIA SOCIAL (Vygotsky/Pichon-Rivière): Análise da mediação, ZDP e o contexto socio-histórico.

DIRETRIZES DE RESPOSTA (OBRIGATÓRIO SEGUIR ESTA ESTRUTURA):

## 1. Eixo Cognitivo (O 'Poder')
- Analisar estágio de pensamento (Pré-operatório, Operatório Concreto, Formal).
- Avaliar funções executivas (Memória de trabalho, controle inibitório, flexibilidade).

## 2. Eixo Socioafetivo (O 'Querer')
- Avaliar o vínculo com o terapeuta e com a escola.
- Analisar a afetividade conforme Wallon e o 'Desejo de Aprender' de Fernández.

## 3. Eixo Instrumental (O 'Fazer')
- Sugerir testes específicos: EOCA (Entrevista Operativa Centrada na Aprendizagem), Provas de Diagnóstico Operatório, Testes Projetivos Psicopedagógicos.
- Interpretação de protocolos de Sampaio e Bossa.

## 4. Eixo Terapêutico (Hipóteses e Intervenção)
- Formular hipóteses diagnósticas (Dificuldade vs. Transtorno).
- Propor estratégias de intervenção lúdica e mediação.

NOTAS ÉTICAS: Mantenha sigilo absoluto. Não use nomes reais. Use terminologia do DSM-5-TR para neurodivergências quando aplicável.
"""

# 3. CONEXÃO COM O GEMINI 2.0 FLASH (VERSÃO PROFISSIONAL)
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Chave API ausente!")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Chamada para o Gemini 2.0 Flash (Geração 3)
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            system_instruction=instrucao_sistema
        )
except Exception as e:
    st.error(f"Erro na inicialização: {e}")

# 4. GESTÃO DE MEMÓRIA (CONTEXTO CLÍNICO)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL (CENTRAL DE INTELIGÊNCIA)
with st.sidebar:
    st.title("📂 Central de Supervisão v3")
    st.write("**Modelo:** Gemini 2.0 Flash")
    
    arquivo_upload = st.file_uploader("Anexar Relatórios ou Exames", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Nova Supervisão (Limpar Memória)"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")
st.caption("Supervisão Clínica baseada em Epistemologia Convergente")

# 6. EXIBIÇÃO DO HISTÓRICO
for msg in st.session_state.chat_session.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# 7. INTERAÇÃO
if prompt := st.chat_input("Descreva o caso do paciente aqui..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo = [prompt]
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                conteudo.append({"mime_type": "application/pdf", "data": arquivo_upload.read()})
            else:
                conteudo.append(Image.open(arquivo_upload))

        with st.spinner("Analisando eixos clínicos..."):
            response = st.session_state.chat_session.send_message(conteudo)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "404" in str(e):
            st.error("Erro 404: O modelo Gemini 2.0 ainda não está disponível na sua rota. Mude para 'gemini-1.5-flash' no código se persistir.")
        else:
            st.error(f"Erro no processamento: {e}")
