import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def attach_and_send(date):
    smtp_server = 'smtp.office365.com'  
    smtp_port = 587 
    smtp_username = '@'
    smtp_password = ''

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = '@'
    msg['Subject'] = 'Localização dos barcos'

    body = f"Seguem em anexo o HTML com os dados de localização dos barcos do dia {date}"
    msg.attach(MIMEText(body, 'plain'))

    with open(f'templates/mapa_com_pontos_{date}.html', 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=f'mapa_com_pontos_{date}.html')

    part['Content-Disposition'] = f'attachment; filename="mapa_com_pontos_{date}.html"'
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)

        server.sendmail(smtp_username, '@', msg.as_string()) 
        print('Email enviado com sucesso')
    except Exception as e:
        print(f'Erro ao enviar email: {str(e)}')
    finally:
        server.quit()
