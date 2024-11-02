import os
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("SMTP_USER")
PASSWORD = os.getenv("SMTP_PASSWORD")
SERVER = os.getenv("SMTP_SERVER")
assert USER and PASSWORD and SERVER, "SMTP credentials not set"

def send_password_reset_email(email: str, reset_token: str):
    """ Sends a password reset email to the user."""
    smtp_port:int = 465
    smtp_user: str = USER #type: ignore
    smtp_password: str = PASSWORD #type: ignore
    smtp_server: str = SERVER #type: ignore

    reset_link = f"https://yourapp.com/reset-password?token={reset_token}"
    em = EmailMessage()
    em["From"] = smtp_user #type: ignore
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
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, em.as_string())
        print("Password reset email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
