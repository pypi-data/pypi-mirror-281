import smtplib
def send(sender_email, sender_password, receiver_email, message):
    try :
        #create smpt server
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(sender_email,sender_password)
        # sending the mail
        s.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully")
        # terminating the session
        s.quit()
    except:
        print("something went wrong please try again")