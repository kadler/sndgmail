import sys
import os.path
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

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
               attachfp='',
               ):
  try:
     msg = MIMEMultipart()
     msg['From'] = fromaddr
     msg['To'] = toaddr
     msg['Subject'] = subject
     msg.attach(MIMEText(body, 'plain'))
     if attachfp <> '':
       part = MIMEBase('application', "octet-stream")
       part.set_payload( open(file,"rb").read() )
       Encoders.encode_base64(part)
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
 body=''
 if len(sys.argv) >= 5:
  body = sys.argv[4]
 attach_full_path=''
 if len(sys.argv) >= 6:
  attach_full_path = sys.argv[5]

 send_email(toaddr,         \
            fromaddr,       \
            password,       \
            subject,        \
            body,           \
            attach_full_path)
