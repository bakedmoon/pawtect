from django.core.mail import send_mail, BadHeaderError

def sendMailToUser(toEmail,name):
    subject = "Thanks for contact us!"
    message = "We will contact you in few moments"
    toEmail = toEmail
    send_mail(subject, message,'',[toEmail])