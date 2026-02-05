import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

# 2. PERSONALIDADE TÉCNICA (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica, fundamentado na Epistemologia Convergente (Jorge Visca).
Integre: Piaget (Cognição), Vygotsky (ZDP), Wallon (Afetividade), Alicia Fernández (Desejo de Aprender) e Neurociências (DSM-5-TR).

ESTRUTURA DE RESPOSTA OBRIGATÓRIA:
1. Eixo Cognitivo: Estágio e funções executivas.
2. Eixo Socioafetivo: Mediação e vínculo com o saber.
3. Eixo Instrumental: Sugestão de testes (EOCA, Provas Operatórias).
4. Eixo Terapêutico: Hipóteses e estratégias práticas.
"""

# 3. CONFIGURAÇÃO DO MODELO (VERSÃO ESTÁVEL)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Removida a ferramenta de Search para eliminar o erro 404
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=instrucao_sistema
    )
except Exception as e:
    st.error(f"Erro na configuração: {e}")

# 4. GESTÃO DE MEMÓRIA (CONTEXTO)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL COMPLETA
with st.sidebar:
    st.title("📂 Painel Clínico")
    st.info("Modelo: Gemini 2.0 Flash (Geração 3)")
    
    arquivo_upload = st.file_uploader("Subir Relatório ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    
    st.divider()
    if st.button("🗑️ Limpar Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")

# 6. EXIBIÇÃO DO HISTÓRICO
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 7. INTERAÇÃO E PROCESSAMENTO
if prompt := st.chat_input("Descreva o caso do paciente..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo = [prompt]
        if arquivo_upload:
            if arquivo_upload.type == "application/pdf":
                # Nota: Para PDFs complexos, pode ser necessário tratamento adicional,
                # mas o Gemini 1.5/2.0 costuma aceitar o envio direto.
                conteudo.append({"mime_type": "application/pdf", "data": arquivo_upload.read()})
            else:
                conteudo.append(Image.open(arquivo_upload))

        response = st.session_state.chat_session.send_message(conteudo)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "429" in str(e):
            st.warning("Aguarde 60 segundos. O limite de uso gratuito foi atingido.")
        else:
            st.error(f"Erro de conexão: {e}")
