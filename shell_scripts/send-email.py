import smtplib, ssl

# ==== SHOCKMEDIA SLAGERIJ ====
# port = 465
# smtp_server = "shockmedia.email"
# sender_email = "info@slagerijoosterhof.nl"
# receiver_email = "info@slagerijoosterhof.nl"
# password = "uUX4XdL3u63V9wLcm9eK"
# ==== GAMIL CEESVW ====
# port = 587  # For starttls
# smtp_server = "smtp.gmail.com"
# sender_email = "ceesvw@gmail.com"
# receiver_email = "ceesvw@gmail.com"
# password = "Y6^c7$j0#w0%"
# ==== GAMIL SLAGERIJ ====
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "slagerij.oosterhof@gmail.com"
receiver_email = "slagerij.oosterhof@gmail.com"
password = "D=Ydonm8pth$$"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)