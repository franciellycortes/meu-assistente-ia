import streamlit as st
import google.generativeai as genai

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico Sênior", page_icon="🧠")

# 2. PERSONALIDADE SÊNIOR COMPLETA
instrucao_sistema = """
Você é um Mentor Sênior em Psicopedagogia e Neuropsicopedagogia Clínica. 
Sua atuação é uma síntese entre a Epistemologia Convergente, a Psicogenética e as Neurociências Aplicadas.

[DIRETRIZES DE RESPOSTA OBRIGATÓRIAS]
1. PERFIL NEUROCOGNITIVO.
2. LEITURA PSICOPEDAGÓGICA CLÁSSICA.
3. AVALIAÇÃO INSTRUMENTAL SUGERIDA.
4. ESTRATÉGIAS DE NEUROINTERVENÇÃO.
"""

# 3. CONEXÃO COM O MODELO
# Verifique se no painel do Streamlit o nome é exatamente este:
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Chave API não configurada nos Secrets do Streamlit (ou GitHub).")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Configuração do modelo
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=instrucao_sistema
)

# Inicialização do Chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 4. INTERFACE DO USUÁRIO
st.title("🧠 Mentor Neuropsicopedagógico Sênior")
st.subheader("Supervisão Clínica v3")

# Mostrar histórico (Melhorado para evitar erros de renderização)
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Entrada do usuário
if prompt := st.chat_input("Descreva o caso clínico para análise..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Envio da mensagem com tratamento de erro específico
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erro na API: {e}")
        st.info("Dica: Verifique se sua chave do Google AI Studio tem permissão para o modelo Gemini 1.5 Flash.")
