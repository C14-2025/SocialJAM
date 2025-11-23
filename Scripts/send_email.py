import os
from email.mime.text import MIMEText
import smtplib

dest = os.getenv("EMAIL_TO")
user = os.getenv("SMTP_USER")
password = os.getenv("SMTP_PASSWORD")

msg = MIMEText("Pipeline executado!")
msg["Subject"] = "Status do Pipeline"
msg["From"] = user
msg["To"] = dest

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(user, password)
    server.sendmail(user, [dest], msg.as_string())

print("Enviado para:", dest)
