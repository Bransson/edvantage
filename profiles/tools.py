from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
import threading

from .token import account_activation_token
from django.contrib.auth import get_user_model


User = get_user_model()

def get_user_with_email_or_username(request):
    username = request.session['last-username-entered']
    if '@' in username:
        try:
            user_object = User.objects.get(email=username)
        except:
            pass
    else:
        user_object = User.objects.get(username=username)
    
    return user_object



 
def send_email(mail_subject, user, domain):
            message = render_to_string('profiles/acc_active_email.html', {
                'user': user,
                'domain': domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()



class EmailThread(threading.Thread):
    def __init__(self, mail_subject, user, domain):
        self.mail_subject = mail_subject
        self.user = user
        self.domain = domain
        threading.Thread.__init__(self)

    def run(self):
            message = render_to_string('profiles/acc_active_email.html', {
                'user': self.user,
                'domain': self.domain,
                'uid':urlsafe_base64_encode(force_bytes(self.user.pk)),
                'token':account_activation_token.make_token(self.user),
            })
            to_email = self.user.email
            email = EmailMessage(
                        self.mail_subject, message, to=[to_email]
            )
            print("sending email")
            email.send()
            print("email has been sent succesfully")



def send_html_mail(mail_subject, user, domain):
    EmailThread(mail_subject, user, domain).start()