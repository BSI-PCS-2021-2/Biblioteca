# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def enviar_email_reclamacao(email, resposta):

    message = Mail(
        from_email='ppnery@edu.unirio.br',
        to_emails=email,
        subject='Resposta da reclamação feita',
        html_content='<h3>Em resposta à sua reclamação</h3>: <strong>{}</strong>'.format(resposta))

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)

    except Exception as e:
        print(e)

def enviar_email_cobranca(email, titulo):

    message = Mail(
        from_email='ppnery@edu.unirio.br',
        to_emails=email,
        subject='Cobrança de empréstimo em atraso',
        html_content='Prezado cliente, a obra de nome {} se encontra em atraso. Favor, devolver o mais rápido possível'.format(titulo))

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)

    except Exception as e:
        print(e)



#enviar_email('ppnery95@gmail.com', 'teste')