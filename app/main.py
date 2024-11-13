import os
import sys
import streamlit as st
import datetime

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.business_logic.resume_processor import process_resume
from app.business_logic.query_handler import handle_query, extract_attributes
from app.data_access.file_manager import list_curriculos, load_curriculo, carregar_consultas
from app.services.email_service import send_evaluation_as_file
from app.components.custom_css import inject_custom_css

# Diretório onde os currículos armazenados ficam
CURRICULO_DIR = "curriculos/"

# Caminho para o arquivo JSON
CONSULTAS_DIR = "consultas/"

def main():
    st.set_page_config(
            page_title="LattesLLM Feedback",
            layout="wide"
    ) 

    # Injetar CSS personalizado
    inject_custom_css()

    st.title("LattesLLM Feedback")

    # Dividindo em 3 colunas
    col1, col2, col3 = st.columns([1, 3, 1.5])
    cont_height = 500

    resume_name = None

    # ----------- Seção 1: Envio e Seleção de Currículo -----------
    with col1:
        st.header("Escolher Currículo")
        cont1 = st.container(height=cont_height)

        # Exibe currículos existentes no diretório
        stored_resumes = list_curriculos(CURRICULO_DIR)
        selected_resume = cont1.selectbox("Escolha um currículo existente", stored_resumes)

        # Upload de novo currículo
        uploaded_file = cont1.file_uploader("Ou faça o upload do currículo (XML)", type="xml")

        # Escolha final do currículo: preferindo o upload se houver
        if uploaded_file:
            # curriculo_data = load_curriculo(os.path.join(CURRICULO_DIR, selected_resume))
            curriculo_data = process_resume(load_curriculo(uploaded_file))
            cont1.write(f"Currículo escolhido: {uploaded_file.name}")
            resume_name = f"{uploaded_file.name}"
        else:
            curriculo_data = process_resume(os.path.join(CURRICULO_DIR, selected_resume))
            cont1.write(f"Currículo escolhido: {selected_resume}")
            resume_name = f"{selected_resume}"

    # ----------- Seção 2: Seleção de Consulta e Resposta do LLM -----------
    with col2:
        st.header("Consulta ao LLM")
        cont2 = st.container(height=cont_height)

        # Carregando as consultas
        prompts = carregar_consultas(CONSULTAS_DIR)
        consultas = list(prompts.keys())
        selected_query = cont2.selectbox("Selecione uma consulta:", consultas)

        # Exibindo conteúdo da consulta
        query_description = cont2.expander("Descrição da consulta")
        if selected_query:
            query_description.write(prompts[selected_query]['descricao'])

        # Submit button to process the selected query
        if cont2.button("Enviar para o modelo"):
            st.session_state['resume'] = resume_name
            st.session_state['query'] = prompts[selected_query]
            
            # Processando os dados de acordo com a consulta escolhida
            processed_data = extract_attributes(prompts[selected_query], curriculo_data)
            st.session_state['processed_data'] = processed_data

            # Envio da consulta e obtenção da resposta do LLM
            response, intermediary_data = handle_query(processed_data, prompts[selected_query])
            st.session_state['response'] = response
            st.session_state['intermediary_data'] = intermediary_data

        # Display the saved response and data if they exist
        if 'response' in st.session_state and 'processed_data' in st.session_state:
            cont2.write("#### Nota")
            cont2.write(f"{st.session_state['response'].nota}")

            # Show data used in the query
            data_description = cont2.expander("Dados usados")
            data_container = data_description.container(height=200)
            data_container.write(st.session_state['processed_data'])

            # Show explanation from the response
            explanation_description = cont2.expander("Explicação")
            explanation_container = explanation_description.container(height=200)
            explanation_container.write(f"{st.session_state['response'].explicacao}")

            # Show intermediary data
            intermediary_description = cont2.expander("Análises intermediárias")
            intermediary_container = intermediary_description.container(height=200)
            intermediary_container.write(st.session_state['intermediary_data'])


    # ----------- Seção 3: Avaliação da Resposta -----------
    with col3:
        st.header("Avaliar Resposta")
        cont3 = col3.container(height=cont_height)

        escala = "(1) Muito fraco   (2) Fraco   (3) Médio   (4) Bom   (5) Muito bom"

        # Avaliação usando a escala Likert
        likert_rating = cont3.slider(f"Qual seria a sua resposta para a consulta?\n\n{escala}", 1, 5, 3)
        justification = cont3.text_area("Opcional: explique o motivo da sua resposta:")

        if cont3.button("Enviar avaliação") and ('response' in st.session_state):

            # Enviar avaliação e resposta por e-mail
            evaluation_data = {
                "id": f"{datetime.datetime.now()}",
                "resume": st.session_state['resume'],
                "rating": likert_rating,
                "justification": justification,
                "query": st.session_state['query'],
                "response": {
                    "score": st.session_state['response'].nota,
                    "explanation": st.session_state['response'].explicacao
                },
                "intermediary": st.session_state['intermediary_data'],
                #"curriculo": curriculo_data
            }

            # Envia por e-mail
            send_evaluation_as_file(evaluation_data, delete_tmp_file=False)
            
            cont3.success(f"Feedback enviado. Agradecemos por sua colaboração!!")

if __name__ == "__main__":
    main()
