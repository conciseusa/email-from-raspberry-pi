
##------------------------------------------
##--- Author: Pradeep Singh updated by Walter Spurgiasz
##--- Blog: https://iotbytes.wordpress.com/programmatically-send-e-mail-from-raspberry-pi-using-python-and-gmail/
##--- Date: 21st Dec 2019
##--- Version: 2.0
##--- Python Ver: 3.5
##--- Description: This python code will send Plain Text and HTML based emails using SMTP server
##------------------------------------------


import configparser, inspect, os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Form the absolute path for the settings.ini file
settings_Dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
settings_File_Path =  os.path.join(settings_Dir, 'settings.ini')


#================= GET SETTINGS FROM EMAIL SECTION IN settings.ini FILE ==============
def read_Email_Settings():

    try:
        config = configparser.ConfigParser()
        config.optionxform=str   #By default config returns keys from Settings file in lower case. This line preserves the case for keys
        config.read(settings_File_Path)

        global SMTP_SERVER
        global SMTP_PORT
        global FROM_ADD
        global USERNAME
        global PASSWORD

        SMTP_SERVER = config.get("EMAIL","SMTP_ADD")
        SMTP_PORT = config.get("EMAIL","SMTP_PORT")
        FROM_ADD = config.get("EMAIL","FROM_ADD")
        USERNAME = config.get("EMAIL","USERNAME")
        PASSWORD = config.get("EMAIL","PASSWORD")

    except Exception as error_msg:
        print ("Error while trying to read SMTP/EMAIL Settings.")
        print ({"Error" : str(error_msg)})
#=====================================================================================

read_Email_Settings()


class Class_eMail():

    def __init__(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self.session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        self.session.ehlo()
        self.session.starttls(context=context)
        self.session.ehlo()
        self.session.login(USERNAME, PASSWORD)


    def initialise_Mail_Body(self, To_Add, Subject):
        #Prepare Mail Body
        Mail_Body = MIMEMultipart()
        Mail_Body['From'] = FROM_ADD
        Mail_Body['To'] = To_Add
        Mail_Body['Subject'] = Subject
        return Mail_Body


    #Call this to send plain text emails.
    def send_Text_Mail(self, To_Add, Subject, txtMessage):
        Mail_Body = self.initialise_Mail_Body(To_Add, Subject)
        #Attach Mail Message
        Mail_Msg = MIMEText(txtMessage, 'plain')
        Mail_Body.attach(Mail_Msg)
        #Send Mail
        self.session.sendmail(FROM_ADD, [To_Add], Mail_Body.as_string())


    #Call this to send HTML emails.
    def send_HTML_Mail(self, To_Add, Subject, htmlMessage):
        Mail_Body = self.initialise_Mail_Body(To_Add, Subject)
        #Attach Mail Message
        Mail_Msg = MIMEText(htmlMessage, 'html')
        Mail_Body.attach(Mail_Msg)
        #Send Mail
        self.session.sendmail(FROM_ADD, [To_Add], Mail_Body.as_string())


    def send_HTML_Attachment_Mail(self, To_Add, Subject, htmlMessage, filename):
        Mail_Body = self.initialise_Mail_Body(To_Add, Subject)
        #Attach Mail Message
        Mail_Msg = MIMEText(htmlMessage, 'html')
        Mail_Body.attach(Mail_Msg)

        with open(filename, "rb") as attachment:
            if filename[-4:] == '.jpg':
                part = MIMEBase("image", "jpg")
            else:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
        Mail_Body.attach(part)

        #Send Mail
        self.session.sendmail(FROM_ADD, [To_Add], Mail_Body.as_string())


    def __del__(self):
        self.session.close()
        del self.session
