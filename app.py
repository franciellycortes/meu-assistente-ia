import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico", page_icon="🧠", layout="wide")

# 2. PERSONALIDADE COMPLETA (MENTOR DE ALTO NÍVEL)
instrucao_sistema = """
Você é um Mentor de Alto Nível em Psicopedagogia Clínica. Sua prática é fundamentada na Epistemologia Convergente (Jorge Visca), integrando a Psicologia Genética (Piaget), o Sociointeracionismo (Vygotsky) e a Psicogenética de Wallon.

[BASES TEÓRICAS]
- Jean Piaget: Estágios cognitivos e Provas Operatórias.
- Lev Vygotsky: ZDP e mediação.
- Henri Wallon: Afetividade e motricidade.
- Escola Argentina (Visca, Paín, Fernández): Modalidade de aprendizagem e vínculo.
- Escola Brasileira (Bossa, Sampaio): Protocolos EOCA e manuais práticos.

[DIRETRIZES DE ANÁLISE]
Estruture sempre a resposta nestes eixos:
1. Eixo Cognitivo (Piaget/Neuro): Estágio atual e funções executivas.
2. Eixo Socioafetivo (Vygotsky/Wallon/Fernández): Mediação e relação com o saber.
3. Eixo Instrumental (Sampaio/Visca): Sugestão de testes específicos.
4. Eixo Terapêutico: Hipóteses diagnósticas e intervenções lúdicas.

[RESTRIÇÕES]
Dados anônimos e apenas Hipóteses Diagnósticas.
"""

# 3. CONEXÃO COM A API (GEMINI 2.0 FLASH)
try:
    CHAVE_API = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    
    # Configuração para o Gemini 2.0 Flash
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=instrucao_sistema
    )
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL
with st.sidebar:
    st.title("📂 Painel Clínico")
    arquivo_upload = st.file_uploader("Subir PDF ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    if st.button("🗑️ Limpar Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico")

# 6. EXIBIÇÃO E INTERAÇÃO
for mensagem in st.session_state.chat_session.history:
    with st.chat_message("user" if mensagem.role == "user" else "assistant"):
        st.markdown(mensagem.parts[0].text)

if prompt := st.chat_input("Descreva o caso clínico..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        conteudo = [prompt]
        if arquivo_upload:
            # Lógica para processar imagem ou PDF
            if arquivo_upload.type == "application/pdf":
                conteudo.append({"mime_type": "application/pdf", "data": arquivo_upload.read()})
            else:
                conteudo.append(Image.open(arquivo_upload))

        response = st.session_state.chat_session.send_message(conteudo)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        if "429" in str(e):
            st.warning("A cota do Gemini 2.0 está zerada ou excedida para sua conta. Se este erro persistir após 5 minutos, mude o nome do modelo no código para 'gemini-1.5-flash'.")
        else:
            st.error(f"Erro clínico: {e}")

