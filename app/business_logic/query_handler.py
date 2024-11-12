import json
from pydantic import BaseModel
from app.api.openai_api import send_query_to_openai

def get_nested_value(data, tags):
    """Percorre o JSON seguindo o caminho representado pelas tags e retorna o valor encontrado.
    Suporta dicionários aninhados e listas."""
    
    for tag in tags:
        if isinstance(data, dict):
            data = data.get(tag, {})
            
        elif isinstance(data, list):
            # Se for uma lista, aplica a função recursivamente em cada item da lista
            data = [get_nested_value(item, [tag]) for item in data]
            
        else:
            return None
        
        if not data:
            return None
    return data

def extract_attributes(query, curriculo):
    """Extrai os atributos de json_1 percorrendo json_2 de acordo com as tags especificadas.
    Suporta dicionários e listas aninhadas."""
    
    atributos = query['atributos']
    result = {}

    for atributo_obj in atributos:
        tag = atributo_obj['tag']
        caminho = atributo_obj['caminho']
        #print(atributo, " : ", tags)
        # Usar as tags para percorrer o json_2 e pegar o valor correspondente
        valor = get_nested_value(curriculo, caminho)[tag]
        
        if tag in result:
            result[tag].append(valor)
        else:
            result[tag] = [valor]

    return result


class RespostaDaAnalise(BaseModel):
    nota: str
    explicacao: str

def handle_query(curriculo_data, query):
    # Gera o contexto para o LLM a partir do currículo processado
    evaluation_metric = "Conclua sua análise com uma das seguintes notas: \n1-Muito fraco; 2-Fraco; 3-Médio; 4-Bom; 5-Muito bom. \nApós isso, explique seu raciocínio em passo a passo." #"### start of output format ###\n Conclua sua análise com apenas um dos seguintes valores: \n1-Muito fraco; 2-Fraco; 3-Médio; 4-Bom; 5-Muito bom.\nVamos pensar por passo a passo..\n### end of output format ###"
    response_format = query['response_format']

    #context = extract_attributes(query, curriculo_data) # extração de só as tags importantes do curriculo_data

    # Send context in batches
    context = curriculo_data.__str__()
    char_per_batch = 32000
    intermediary_query = query['consulta intermediaria']

    intermediary_analyses = []
    if len(context) > char_per_batch:
        for i in range(0, len(context) - char_per_batch, char_per_batch):
            end = char_per_batch if i + char_per_batch <= len(context) else len(context)
            mini_context = context[i : i + end]
            mini_analysis = send_query_to_openai(mini_context, f"{intermediary_query}", None)

            intermediary_analyses.append(mini_analysis)
        
    else:
        intermediary_analyses = [send_query_to_openai(context, f"{intermediary_query}", None)]
    intermediary_analyses = "\n\n".join(intermediary_analyses)

    # print("\n\n\nANALYSES")
    # print(intermediary_analyses)
    # print(*[f"{analysis}\n" for analysis in intermediary_analyses])

    # Envia a consulta para o LLM (API OpenAI)
    response = send_query_to_openai(intermediary_analyses, f"{query['consulta final']} \n{evaluation_metric}", RespostaDaAnalise)
    # response = None
    return response, intermediary_analyses
