import smtplib

def sendEmail(eServer,ePort,eUsername,ePassword,emailFrom,emailTo,message):
    smtpObj = smtplib.SMTP(eServer, ePort)
    smtpObj.ehlo()
    smtpObj.starttls()
#    pw=input()
#    lg=input()
#    emailFrom=input()
#    emailTo=input()
    smtpObj.login(eUsername,ePassword)
    smtpObj.sendmail(emailFrom,emailTo,message)
    smtpObj.quit()
