import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente

def send_query_to_openai(context, query, response_format):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system = f"Aja como um avaliador de currículos acadêmicos que está procurando profissionais especializados em uma área específica, e decide avaliar de forma qualitativa se o profissional se enquadra no perfil procurado pelo seu instituto. Responda à consulta do usuário com base no conteúdo do currículo abaixo.\n"
    system += f"### DADOS ### {context} ### FIM DOS DADOS ###"
    
    # print(f"SYSTEM: {system}\n\n\n")
    # print(f"USER: {query}\n\n\n")
    # print(f"RESPONSE_FORMAT: {response_format}")
    
    if response_format != None:
        completion = client.beta.chat.completions.parse(
            model = "gpt-4o-mini-2024-07-18",
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": query}
            ],
            response_format = response_format
        )
        return completion.choices[0].message.parsed

    else:
        completion = client.beta.chat.completions.parse(
            model = "gpt-4o-mini-2024-07-18",
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": query}
            ]
        )
        return completion.choices[0].message.content

        # {
        #     "type": "json_schema",
	    #         "json_schema": {
        #             {
        #             "name": "get_feedback",
        #             "description": "Provides a structured feedback response",
        #             "strict": True,
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {
        #                     "nota": {
        #                         "type": "string",
        #                         "description": "A rating or note as a text string"
        #                     },
        #                     "explicacao": {
        #                         "type": "string",
        #                         "description": "An explanation providing additional details about the rating or note"
        #                     }
        #                 },
        #                 "additionalProperties": False,
        #                 "required": ["nota", "explicacao"]
        #             }
        #         }

        #         }
        # }

    
    
