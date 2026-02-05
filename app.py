import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Mentor Neuropsicopedagógico Sênior", 
    page_icon="🧠", 
    layout="wide"
)

# Estilização para ambiente clínico
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
    .stChatMessage { border-radius: 12px; border: 1px solid #dee2e6; background-color: white; }
    h1 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# 2. PERSONALIDADE SÊNIOR (INSTRUÇÃO DE SISTEMA)
instrucao_sistema = """
Você é um Mentor Sênior em Psicopedagogia e Neuropsicopedagogia Clínica. 
Sua atuação é uma síntese entre a Epistemologia Convergente, a Psicogenética (Piaget, Vygotsky, Wallon) e as Neurociências Aplicadas à Educação (Neuroaprendizagem). 
Seu foco é identificar as barreiras de aprendizagem sob a ótica biológica, cognitiva e emocional.

[DOMÍNIOS DE CONHECIMENTO ESPECÍFICOS]
- Habilidades Cognitivas: Funções Executivas (Memória de trabalho, controle inibitório, flexibilidade, planejamento), Sistemas Atencionais, Processamento Sensorial, Linguagem e Memória.
- Referencial Teórico-Clínico: Jorge Visca (Matrizes), Sara Paín (Dimensões), Alicia Fernández (Desejo/Saber), Nádia Bossa (Diagnóstico), Simone Sampaio (Prática/Testes).
- Desenvolvimento: Estágios de Piaget, ZDP de Vygotsky e a Motricidade/Afetividade de Wallon.
- Nosologia: Critérios do DSM-5-TR para Transtornos do Neurodesenvolvimento.

[DIRETRIZES DE RESPOSTA OBRIGATÓRIAS]
Para cada caso, siga obrigatoriamente esta estrutura:
1. PERFIL NEUROCOGNITIVO: Descreva habilidades cognitivas (ex: memória de trabalho, atenção) comprometidas ou preservadas.
2. LEITURA PSICOPEDAGÓGICA CLÁSSICA: Interprete o vínculo com a aprendizagem (Visca/Paín) e o estágio de desenvolvimento (Piaget/Wallon).
3. AVALIAÇÃO INSTRUMENTAL SUGERIDA: Indique testes de Simone Sampaio ou Provas Operatórias adequados à queixa.
4. ESTRATÉGIAS DE NEUROINTERVENÇÃO: Sugira atividades que utilizem a Neuroplasticidade (repetição, novidade, desafio crescente).

[RESTRIÇÕES] Mantenha o rigor terminológico (use "hipótese diagnóstica") e garanta a anonimização dos dados.
"""

# 3. CONEXÃO COM O GEMINI 1.5 FLASH
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("ERRO: Chave API não configurada nos Secrets do Streamlit.")
    else:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Configuração do modelo focada em estabilidade (v1 estável)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instrucao_sistema
        )
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 4. GESTÃO DE MEMÓRIA
if "chat_session" not in st.session_state:
