.
└── lattes_llm_v3
    ├── app
    │   ├── __pycache__
    │   │   └── __init__.cpython-312.pyc
    │   ├── api
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-312.pyc
    │   │   │   └── openai_api.cpython-312.pyc
    │   │   ├── __init__.py
    │   │   └── openai_api.py
    │   ├── business_logic
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-312.pyc
    │   │   │   ├── compression_utils.cpython-312.pyc
    │   │   │   ├── query_handler.cpython-312.pyc
    │   │   │   └── resume_processor.cpython-312.pyc
    │   │   ├── __init__.py
    │   │   ├── compression_utils.py
    │   │   ├── query_handler.py
    │   │   └── resume_processor.py
    │   ├── components
    │   │   ├── __pycache__
    │   │   │   └── custom_css.cpython-312.pyc
    │   │   └── custom_css.py
    │   ├── data_access
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-312.pyc
    │   │   │   └── file_manager.cpython-312.pyc
    │   │   ├── __init__.py
    │   │   └── file_manager.py
    │   ├── services
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-312.pyc
    │   │   │   └── email_service.cpython-312.pyc
    │   │   ├── __init__.py
    │   │   └── email_service.py
    │   ├── __init__.py
    │   ├── config.py
    │   └── main.py
    ├── assets
    │   └── styles
    │       └── custom.css
    ├── consultas
    │   ├── regularidade_publicacoes.json
    │   └── zregularidade_publicacoes.json
    ├── curriculos
    │   ├── Alba Cristina Magalhães Alves de Melo.xml
    │   ├── Alfredo Goldman.xml
    │   ├── Alírio Santos de Sá.xml
    │   ├── Altigran Soares da Silva.xml
    │   ├── André Carlos Ponce de Leon Ferreira de Carvalho.xml
    │   ├── Avelino Francisco Zorzo.xml
    │   ├── Carla Maria dal Sasso Freitas.xml
    │   ├── Carlos André Guimarães Ferraz.xml
    │   ├── Eunice Pereira dos Santos Nunes.xml
    │   ├── Fabio Kon.xml
    │   ├── Itana Maria De Souza Gimenes.xml
    │   ├── José Viterbo Filho.xml
    │   └── Lisandro Zambenedetti Granville.xml
    ├── .env
    ├── README.md
    └── requirements.txt


.
├── app
│   ├── __pycache__
│   │   └── __init__.cpython-312.pyc
│   ├── api
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── openai_api.cpython-312.pyc
│   │   ├── __init__.py
│   │   └── openai_api.py
│   ├── business_logic
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── compression_utils.cpython-312.pyc
│   │   │   ├── query_handler.cpython-312.pyc
│   │   │   └── resume_processor.cpython-312.pyc
│   │   ├── __init__.py
│   │   ├── compression_utils.py
│   │   ├── query_handler.py
│   │   └── resume_processor.py
│   ├── components
│   │   ├── __pycache__
│   │   │   └── custom_css.cpython-312.pyc
│   │   └── custom_css.py
│   ├── data_access
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── file_manager.cpython-312.pyc
│   │   ├── __init__.py
│   │   └── file_manager.py
│   ├── services
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── email_service.cpython-312.pyc
│   │   ├── __init__.py
│   │   └── email_service.py
│   ├── __init__.py
│   ├── config.py
│   └── main.py
├── assets
│   └── styles
│       └── custom.css
├── consultas
├── curriculos
│   ├── Alba Cristina Magalhães Alves de Melo.xml
│   ├── Alfredo Goldman.xml
│   ├── Alírio Santos de Sá.xml
│   ├── Altigran Soares da Silva.xml
│   ├── André Carlos Ponce de Leon Ferreira de Carvalho.xml
│   ├── Avelino Francisco Zorzo.xml
│   ├── Eunice Pereira dos Santos Nunes.xml
│   ├── Fabio Kon.xml
│   ├── Itana Maria De Souza Gimenes.xml
│   ├── José Viterbo Filho.xml
│   └── Lisandro Zambenedetti Granville.xml
├── .env
├── README.md
└── requirements.txt



lattes_llm/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # Arquivo principal (UI com Streamlit)
│   ├── config.py                # Configurações gerais
│   ├── business_logic/
│   │   ├── __init__.py
│   │   ├── resume_processor.py  # Processamento de currículos XML
│   │   └── query_handler.py     # Manipulação das consultas
│   ├── api/
│   │   ├── __init__.py
│   │   └── openai_api.py        # Integração com a API OpenAI
│   ├── data_access/
│   │   ├── __init__.py
│   │   └── file_manager.py      # Gerenciamento de currículos e respostas
│   └── services/
│       ├── __init__.py
│       └── email_service.py     # Envio de e-mails
│
├── curriculos/                  # Diretório de currículos armazenados
├── .env                         # Variáveis de ambiente (API token)
├── requirements.txt             # Dependências
└── README.md                    # Documentação
