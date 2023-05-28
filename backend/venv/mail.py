import smtplib
import key as postoffice
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(name, email, message):
    # Email Configuration
    sender_email = postoffice.webmanager_semail
    sender_password = postoffice.mail_key
    receiver_email = postoffice.webmanager_remail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    #Rate Limiting - adding a delay to mitigate spam
    time.sleep(5) # Delay in seconds

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Message from {}'.format(name)

    body = 'Hello from {},\n\n{},\n\n I should now be on the email Server {}'.format(name, message, email)
    msg.attach(MIMEText(body, 'plain'))

    # then Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))


