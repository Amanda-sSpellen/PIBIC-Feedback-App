import os
import json
import smtplib
import datetime
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente


def save_evaluation_data(evaluation_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(evaluation_data, json_file, ensure_ascii=False, indent=4)


def send_email_with_attachment(file_path, id):
    # Pegando informações
    sender_email = os.getenv("sender_email")
    recipient_email = os.getenv("recipient_email")
    sender_password = os.getenv("sender_password")

    # Compondo o e-mail
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Avaliação ({id})"

    # Corpo do e-mail
    msg.attach(MIMEText(f"Enviado em {datetime.datetime.now()}", 'plain'))

    # Anexando o arquivo JSON
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {file_path}")
        msg.attach(part)

    # Enviando o e-mail
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def send_evaluation_as_file(evaluation_data, delete_tmp_file=True):
    file_path = Path(os.getcwd()) / "tmp_file.json"
    save_evaluation_data(evaluation_data, file_path)
    send_email_with_attachment(file_path, evaluation_data[id])
    
    if delete_tmp_file:
        os.remove(file_path)


# # Exemplo de uso
# evaluation_data = {
#     "rating": 5,
#     "justification": "Muito bom.",
#     "response": {
#         "nota": "A",
#         "explicacao": "Excelente desempenho."
#     }
# }

# file_path = 'evaluation_data.json'
# save_evaluation_data(evaluation_data, file_path)

# # Configuração do e-mail
# sender_email = "pibic.llmlattes2024@gmail.com"
# sender_password = "wodu funh omtw hrhh"
# recipient_email = "pibic.llmlattes2024@gmail.com"
# subject = "Avaliação JSON"
# body = "Segue em anexo o arquivo JSON com a avaliação."

#send_email_with_attachment(sender_email, sender_password, recipient_email, subject, body, file_path)
