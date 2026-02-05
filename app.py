import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico Sênior", page_icon="🧠", layout="wide")

# 2. PERSONALIDADE COMPLETA (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor Sênior em Psicopedagogia e Neuropsicopedagogia Clínica. 
Sua atuação é uma síntese entre a Epistemologia Convergente, a Psicogenética (Piaget, Vygotsky, Wallon) e as Neurociências Aplicadas à Educação.

[DOMÍNIOS DE CONHECIMENTO]
- Funções Executivas, Sistemas Atencionais, Processamento Sensorial, Linguagem e Memória.
- Referencial: Jorge Visca, Sara Paín, Alicia Fernández, Nádia Bossa, Simone Sampaio.
- Nosologia: DSM-5-TR.

[DIRETRIZES DE RESPOSTA OBRIGATÓRIAS]
1. PERFIL NEUROCOGNITIVO: Habilidades comprometidas ou preservadas.
2. LEITURA PSICOPEDAGÓGICA CLÁSSICA: Vínculo (Visca/Paín) e estágio de desenvolvimento (Piaget/Wallon).
3. AVALIAÇÃO INSTRUMENTAL SUGERIDA: Testes de Simone Sampaio ou Provas Operatórias.
4. ESTRATÉGIAS DE NEUROINTERVENÇÃO: Baseadas em Neuroplasticidade.

[RESTRIÇÕES] Mantenha o rigor terminológico e a anonimização dos dados.
"""

# 3. CONEXÃO ESTÁVEL (CORREÇÃO DO ERRO 404)
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Chave API não encontrada nos Secrets!")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # AJUSTE CRUCIAL: Chamando apenas o nome do modelo sem prefixos extras
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instrucao_sistema
        )
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. INTERFACE (BARRA LATERAL)
with st.sidebar:
    st.title("📂 Central de Supervisão")
    st.info("Modelo Ativo: Gemini 1.5 Flash (Estável)")
    arquivo_upload = st.file_uploader("Subir PDF ou Imagem", type=["png", "jpg", "jpeg", "pdf"])
    
    if st.button("🗑️ Nova Supervisão"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

st.title("🧠 Mentor Neuropsicopedagógico Sênior")

# 6. EXIBIÇÃO DO HISTÓRICO
for mensagem in st.session_state.chat_session.history:
    role = "user" if mensagem.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

# 7. INTERAÇÃO E PROCESSAMENTO
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

        with st.spinner("Analisando caso clínico..."):
            response = st.session_state.chat_session.send_message(conteudo_envio)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erro detalhado: {e}")
