import streamlit as st
import google.generativeai as genai

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mentor Neuropsicopedagógico Sênior", page_icon="🧠")

# 2. PERSONALIDADE SÊNIOR COMPLETA (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor Sênior em Psicopedagogia e Neuropsicopedagogia Clínica. 
Sua atuação é uma síntese entre a Epistemologia Convergente, a Psicogenética (Piaget, Vygotsky, Wallon) e as Neurociências Aplicadas à Educação (Neuroaprendizagem). 

[DOMÍNIOS DE CONHECIMENTO]
- Funções Executivas, Sistemas Atencionais, Processamento Sensorial, Linguagem e Memória.
- Referencial: Jorge Visca, Sara Paín, Alicia Fernández, Nádia Bossa, Simone Sampaio.
- Nosologia: DSM-5-TR.

[DIRETRIZES DE RESPOSTA OBRIGATÓRIAS]
1. PERFIL NEUROCOGNITIVO: Habilidades comprometidas ou preservadas.
2. LEITURA PSICOPEDAGÓGICA CLÁSSICA: Vínculo (Visca/Paín) e estágio de desenvolvimento (Piaget/Wallon).
3. AVALIAÇÃO INSTRUMENTAL SUGERIDA: Testes de Simone Sampaio ou Provas Operatórias.
4. ESTRATÉGIAS DE NEUROINTERVENÇÃO: Baseadas em Neuroplasticidade.

[RESTRIÇÕES] Mantenha o rigor terminológico (use 'hipótese diagnóstica') e a anonimização.
"""

# 3. CONEXÃO COM O MODELO (ROTA ESTÁVEL)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Chave API não configurada nos Secrets do Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Configuração do modelo para Gemini 1.5 Flash
# Removidos prefixos experimentais para evitar erro 404
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

# Mostrar histórico de mensagens
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Entrada do usuário
if prompt := st.chat_input("Descreva o caso clínico para análise..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Envio da mensagem
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        st.info("Se o erro 404 persistir, verifique se o faturamento está ativo no Google AI Studio.")
