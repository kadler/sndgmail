import sys
import os.path
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#--------------------------------------------------------------------------
# send_mail: Enva un email usando SMTP, usando los siguientes paetros:
#
#            -toaddr   Direccin a la que debe enviarse el correo
#            -fromaddr Desde que direccin debe enviarse
#            -password Contrasa de la diren desde
#            -subject  Tema del correo
#            -body     Cuerpo del correo
#            -attachfp Path del archivo attachado
#--------------------------------------------------------------------------
def send_email(toaddr,
               fromaddr,
               password,
               subject,
               body='',
               attachfp=None,
               ):
  try:
     msg = MIMEMultipart()
     msg['From'] = fromaddr
     msg['To'] = toaddr
     msg['Subject'] = subject
     msg.attach(MIMEText(body, 'plain'))
     if attachfp:
       with open(attachfp, "rb") as fp:
         part = MIMEApplication(fp.read())
         part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(attachfp))
         msg.attach(part)

     server = smtplib.SMTP('smtp.gmail.com', 587)
     server.starttls()
     server.login(fromaddr, password)
     text = msg.as_string()
     server.sendmail(fromaddr, toaddr, text)
     server.quit()
  except:
     pass
#--------------------------------------------------------------------------
# Punto de Entrada del Programa
#--------------------------------------------------------------------------
if __name__ == "__main__":
 toaddr = sys.argv[1]
 fromaddr = sys.argv[2]
 password = sys.argv[3]
 subject = sys.argv[4]
 body = sys.argv[5] if len(sys.argv) >= 6 else ''
 attach_full_path = sys.argv[6] if len(sys.argv) >= 7 else ''

 send_email(toaddr,         \
            fromaddr,       \
            password,       \
            subject,        \
            body,           \
            attach_full_path)
