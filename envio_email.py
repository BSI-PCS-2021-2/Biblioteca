# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def enviar_email(email, resposta):

    message = Mail(
        from_email='ppnery@edu.unirio.br',
        to_emails=email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>{}</strong>'.format(resposta))

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)

    except Exception as e:
        print(e)


#enviar_email('ppnery95@gmail.com', 'teste')