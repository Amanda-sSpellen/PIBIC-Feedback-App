import streamlit as st
import os
import json

from pathlib import Path
from datetime import datetime
from pydantic import BaseModel

from compression_utils import generate_compressed_dict, write_compressed_data_to_file, read_json
from openai_access import execute_prompt

class ResumeChoosingSection:
    def __init__(self, col1, section_height=530):
        self.col1 = col1
        self.section_height = section_height

    def draw(self):
        tab1 = self.col1.container(height=self.section_height)
        tab1.write('#### Currículo')

        uploaded_file = tab1.file_uploader("Faça o upload de um novo currículo", help="")

        tab1.write("#### Currículos disponíveis")
        select_file_container = tab1.container(height=200)

        files = os.listdir("raw_data")
        files = sorted([f for f in files if os.path.isfile(os.path.join("raw_data", f))])

        #file_list =  select_file_container.expander("Currículos disponíveis")
        choosen_file = select_file_container.radio("Currículos disponíveis", files, index=None, label_visibility="collapsed")
        choosen_file_name = choosen_file
        parsed_data = None

        if uploaded_file is not None:
            choosen_file = uploaded_file
            choosen_file_name = choosen_file.name
            save_path = Path("raw_data", choosen_file_name)
            with open(save_path, mode='wb') as w:
                w.write(uploaded_file.getvalue())

        if choosen_file is not None:
            processed_files = [str(f).replace("processed_", "").replace(".json", "") for f in os.listdir("processed_data/json")]
            if choosen_file_name.replace(".xml", "") not in processed_files:
                
                save_path = Path("raw_data", choosen_file_name)
                
                # Parse the uploaded file
                parsed_data = {"data": generate_compressed_dict(save_path),
                               "filename": choosen_file_name}
                
                with open(f"processed_data/json/processed_{choosen_file_name.replace(".xml", ".json")}", "w") as f:
                    f.write(json.dumps(parsed_data))

                # Save the parsed data in a folder
                save_path = "processed_data/txt/" #os.path.join("processed_data", uploaded_file.name)
                write_compressed_data_to_file(parsed_data["data"], str(save_path))
                
                select_file_container.write(f"Arquivo salvo em: {save_path}")
            else:
                parsed_data = read_json(f"processed_data/json/processed_{choosen_file_name.replace(".xml", ".json")}")
                parsed_data = {"data": parsed_data,
                               "filename": choosen_file_name}
                select_file_container.write(f"Arquivo carregado de: {f"processed_data/json/processed_{choosen_file_name.replace(".xml", ".json")}"}")
            return parsed_data, True
        return None, False


class saida_1(BaseModel):
    nota : str
    explicacao : str
    
class saida_2(BaseModel):
    key_points : list[str]
    explicacao : str
    
format_outs = {"Avaliar nível de pós-graduação em CC": saida_1,
                "Key-points do Resumo" : saida_2,
}


class PromptGenerationSection:
    def __init__(self, col2, section_height=530):
        self.col2 = col2
        self.section_height = section_height

    def draw(self, is_data_selected, parsed_data):
        tab2 = col2.container(height=section_height)
        tab2.write(f'#### Consulta')

        prompt_container = tab2.container(height=150)

        prompts = {"Avaliar nível de pós-graduação em CC": "Avalie a formação em nível de pós-graduação na área de ciência da computação do pesquisador deste currículo, considerando os seguintes critérios: a participação do pesquisador como orientador nas produções acadêmicas de seus alunos; prêmios recebidos relacionados a teses e dissertações. Seja preciso e objetivo em sua resposta. Sua resposta deve se limitar ao conteúdo do currículo, aos aspectos dos critérios de avaliação e aos dados qualitativos que podem ser inferidos.\n\n### start of output format ###\n Conclua sua análise com apenas um dos seguintes valores: \n1-Muito fraco; 2-Fraco; 3-Médio; 4-Bom; 5-Muito bom.\nVamos pensar por passo a passo..\n### end of output format ###",
                "Key-points do Resumo": "Quais são os key-points principais do pesquisador desse currículo?"}


        opt_prompts = list(prompts.keys())
        disable_run = True
        selected_prompt = None
        # print(parsed_data)
        if parsed_data != None:
            selected_prompt = prompt_container.radio(f"Escolha uma consulta aos dados de {str(parsed_data['filename']).replace('.xml', '')}:", opt_prompts)

        if is_data_selected and selected_prompt != None:
            print("Pode ativar:", parsed_data['filename'])
            disable_run = False
            
        run_prompt = tab2.button("Consultar", disabled=disable_run)

        saved_results = None

        description = tab2.expander("Descrição da consulta")
        if selected_prompt:
            description.write(prompts[selected_prompt].replace("###", "\\#\\#\\#"))

        result = None

        if run_prompt:
            #description.write(prompts[selected_prompt].replace("###", "\#\#\#"))

            # Process the parsed data with the selected prompt

            dados = tab2.expander("Dados disponíveis")

            tab2.write('#### Resultado')
            #result_container.write(prompts[selected_prompt])

            # dados.write(parsed_data["data"]['RESUME']['CV']['DG']['RC'])
            result_container = tab2.container(height=300)

            result, chat_info = execute_prompt(parsed_data["data"]["data"], prompts[selected_prompt], format_outs[selected_prompt], smaller=True)

            if(selected_prompt == "Avaliar nível de pós-graduação em CC"):
                result_container.write(f'#### Nota: {result.nota}\n###### Explicação: {result.explicacao}')

            # metadata = {"date": str(datetime.now()), 
            #             "created": chat_info.created, 
            #             "model": chat_info.model, 
            #             "usage": {"completion_tokens": chat_info.usage.completion_tokens,
            #                                     "prompt_tokens": chat_info.usage.prompt_tokens,
            #                                     "total_tokens": chat_info.usage.total_tokens}}
            # saved_results = {"metadata": metadata,
            #                 "input": {"filename": parsed_data['filename'],
            #                             "prompt": prompts[selected_prompt]},
            #                 "llm_response": result}

            # # metadata = {"date": str(datetime.now()), 
            # #             "created": chat_info, 
            # #             "model": chat_info, 
            # #             "usage": {"completion_tokens": chat_info,
            # #                                      "prompt_tokens": chat_info,
            # #                                      "total_tokens": chat_info}}
            # # saved_results = {"metadata": metadata,
            # #                  "input": {"filename": choosen_file_name,
            # #                             "prompt": prompts[selected_prompt]},
            # #                  "llm_response": result}
            
            
            # result_path = f'llm_response/{saved_results["input"]["filename"]}_{saved_results["metadata"]["date"]}.json'
            # with open(result_path, "w") as f:
            #     f.write(json.dumps(saved_results))
            metadata = {"metadata": "sup"}
            return metadata, True
        return None, False
        


class EvaluationSection:
    def __init__(self, col3, section_height=530):
        self.col3 = col3
        self.section_height = section_height
    
    def draw(self, is_data_selected, is_prompt_generated, metadata):
        tab3 = col3.container(height=section_height)
        tab3.subheader("(TODO)")
        # grade = tab3.radio('Em uma escala de 1 a 5, avalie a resposta do modelo.\nConsidere 1 como muito insatisfeito, e 5 como muito satisfeito.', [1, 2, 3, 4, 5], index=None, horizontal=True)

        # print(is_data_selected, is_prompt_generated, grade)
        tab3.subheader("Explicação")
        explanation = tab3.text_area("(Opcional) Descreva em uma breve explicação dos motivos que levaram você a escolher tal escala.")
        disable_eval = False # True
        run_evaluation = tab3.button("Concluir", disabled=disable_eval)
        # if (grade != None):
        #     disable_eval = False



        # if steps['prompt selection']:
        #     if result_path:
        #         saved_results = read_json(result_path)
        #     else:
        #         saved_results = None

        # if go_bitch:
        #     run_evaluation = tab3.button("Concluir", disabled=activate)
        #     if run_evaluation:
        #         with open(f'llm_response/{saved_results["input"]["filename"]}_{saved_results["metadata"]["date"]}.json', "w") as f:
        #             saved_results["user_evaluation": {"grade": grade,
        #                                             "explanation": f"{explanation}"}]
        #             f.write(json.dumps(saved_results))



def ensure_directory_exists(directory_path):
    """
    Checks if the directory exists at the specified path.
    If it does not exist, the directory is created.

    Args:
        directory_path (str): The path of the directory to check/create.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)



section_height = 530
# Streamlit app
st.set_page_config(
        page_title="LattesLLM",
        layout="wide"
)
# st.header("LattesLLM")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
            [data-testid='stFileUploader'] {
                width: max-content;
            }
            [data-testid='stFileUploader'] section {
                padding: 0;
                float: left;
            }
            [data-testid='stFileUploader'] section > input + div {
                display: none;
            }
            [data-testid='stFileUploader'] section + div {
                float: right;
                padding-top: 0;
            }
        </style>
        """, unsafe_allow_html=True)

# tab2, tab3 = 
col1, col2, col3 = st.columns([25, 40, 30]) #tabs(["Currículos", "Chat", "Avaliação"])


ensure_directory_exists("raw_data")
ensure_directory_exists("processed_data")
ensure_directory_exists("processed_data/json")
ensure_directory_exists("processed_data/txt")
ensure_directory_exists("llm_response")

section1 = ResumeChoosingSection(col1, section_height)
section2 = PromptGenerationSection(col2, section_height)
section3 = EvaluationSection(col3, section_height)

parsed_data, is_data_selected = section1.draw()
metadata, is_prompt_generated = section2.draw(is_data_selected, parsed_data)
section3.draw(is_data_selected, is_prompt_generated, metadata)
