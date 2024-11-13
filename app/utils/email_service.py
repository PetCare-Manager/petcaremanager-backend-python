import os
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")
SERVER = os.getenv("MAIL_HOST")
PORT = os.getenv("MAIL_PORT")
assert USER and PASSWORD and SERVER, "SMTP credentials not set"

def send_password_reset_email(email: str, reset_token: str):
    """ Sends a password reset email to the user."""
    MAIL_PORT = PORT
    MAIL_USERNAME: str = USER #type: ignore
    MAIL_PASSWORD: str = PASSWORD #type: ignore
    MAIL_HOST: str = SERVER #type: ignore

    reset_link = f"https://yourapp.com/reset-password?token={reset_token}"
    em = EmailMessage()
    em["From"] = MAIL_USERNAME #type: ignore
    em["To"] = email
    em["Subject"] = "Password Reset Request"

    body = f"""
        <p>Hola,</p>
        <p>Has solicitado restablecer tu contraseña. De momento la pagina web no esta disponible
        pero puedes usar directamente este token {reset_token} en el api</p>
        <p>Haz clic en el enlace de abajo para restablecerla:</p>
        <a href="{reset_link}">Restablecer Contraseña</a>
        <p>Este enlace expirará en 1 hora.</p>
        <p>Si no solicitaste esto, por favor ignora este correo.</p>
    """
    em.set_content(body, subtype="html")

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT, context=context) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, email, em.as_string())
        print("Password reset email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to authenticate with the SMTP server: {e}")
    except smtplib.SMTPConnectError as e:
        print(f"Failed to connect to the SMTP server: {e}")
    except smtplib.SMTPHeloError as e:
        print(f"SMTP server refused HELO message: {e}")
    except smtplib.SMTPSenderRefused as e:
        print(f"SMTP server refused sender address: {e}")
    except smtplib.SMTPRecipientsRefused as e:
        print(f"SMTP server refused recipient addresses: {e}")
    except smtplib.SMTPDataError as e:
        print(f"SMTP server replied with an unexpected error code: {e}")
    except smtplib.SMTPNotSupportedError as e:
        print(f"SMTP command or option not supported by the server: {e}")
    except smtplib.SMTPException as e:
        print(f"An SMTP error occurred: {e}")