import os
import sys
import streamlit as st

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.business_logic.resume_processor import process_resume
from app.business_logic.query_handler import handle_query, extract_attributes
from app.data_access.file_manager import list_curriculos, load_curriculo, carregar_consultas
from app.services.email_service import send_email
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

    # ----------- Seção 1: Envio e Seleção de Currículo -----------
    with col1:
        st.header("Escolher Currículo")
        cont1 = st.container(height=cont_height)

        # Upload de novo currículo
        uploaded_file = cont1.file_uploader("Faça upload de um currículo (XML)", type="xml")

        # Exibe currículos existentes no diretório
        stored_resumes = list_curriculos(CURRICULO_DIR)
        selected_resume = cont1.selectbox("Ou escolha um currículo existente do nosso banco de dados", stored_resumes)

        # Escolha final do currículo: preferindo o upload se houver
        if uploaded_file:
            # curriculo_data = load_curriculo(os.path.join(CURRICULO_DIR, selected_resume))
            curriculo_data = process_resume(load_curriculo(uploaded_file))
            cont1.write(f"Currículo escolhido: {uploaded_file.name}")
        else:
            curriculo_data = process_resume(os.path.join(CURRICULO_DIR, selected_resume))
            cont1.write(f"Currículo escolhido: {selected_resume}")

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

        if cont2.button("Enviar para o modelo"):
            
            # Processando os dados de acordo com a consulta escolhida
            processed_data = extract_attributes(prompts[selected_query], curriculo_data)
            st.session_state['processed_data'] = processed_data

            # Mostrando os dados que serão usados na consulta
            data_description = cont2.expander("Dados usados")
            data_container = data_description.container(height=200)
            data_container.write(processed_data)

            # Envio da consulta e obtenção da resposta do LLM
            response, intermediary_data = handle_query(processed_data, prompts[selected_query])
            st.session_state['response'] = response
            st.session_state['instermediary_data'] = intermediary_data

            cont2.write(f"#### Nota")
            cont2.write(f"{response.nota}")

            # Mostrando os dados que serão usados na consulta
            explanation_description = cont2.expander("Explicação")
            explanation_container = explanation_description.container(height=200)
            explanation_container.write(f"{response.explicacao}")

            # Mostrando os dados que serão usados na consulta
            intermediary_description = cont2.expander("Análises intermediárias")
            intermediary_container = intermediary_description.container(height=200)
            intermediary_container.write(intermediary_data)


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
                    "rating": likert_rating,
                    "justification": justification,
                    "response": response,
                    #"curriculo": curriculo_data
                }

                st.write(evaluation_data)
                # Envia por e-mail
                # email = "evaluation_receiver@example.com"
                # send_email(email, evaluation_data)
                # cont3.success(f"Evaluation and response sent to {email}!")

if __name__ == "__main__":
    main()
