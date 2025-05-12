from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy
from celery import shared_task


class SendEmail:
    def __init__(self,user:User,domain:str):
        self.user = user
        self.current_site = domain
        #Создаём уникальный токен при регистрации для юзера.Eго id получает make_token
        self.token = default_token_generator.make_token(self.user)
        # Будет создан экземпляр юзера по его модели, его id извлечётся и 
        # будет переведёт в uidb64 
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk,encoding='utf-8')) 

    def send_activate(self):
        #строит URL по имени маршрута account:user_registration, 
        # подставляя в него параметры uidb64 и token, то есть в url адресс его 
        # уникальный токен и его id, закодированный в uidb64
        reset_password_url = reverse_lazy(
            "account:signup_confirm",
            kwargs={"uidb64":self.uid,
                    "token":self.token,}
        )
        subject = f"Активация аккаунта на сайте {self.current_site}"
        message = (
            f"Благодарим за регистрацию на сайте {self.current_site}.\n"
            "Для активации учётной записи,пожалуйста перейдите по ссылке:\n"
            f"http://{self.current_site}{reset_password_url}\n"
        )
        # встроенный метод модели пользователя, 
        # который отправляет письмо на email 
        # пользователя с заданной темой и текстом.
        email = EmailMessage(subject,
                         message,
                         'kaznacheev6969@gmail.com',
                         [self.user.email])
        email.send()

@shared_task
def activate_email_task(user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    current_site = Site.objects.get_current().domain
    send_email = SendEmail(user=user, domain=current_site)
    send_email.send_activate()