from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy


class SendEmail:
    def __init__(self,user:User,request):
        self.user = user
        self.current_site = get_current_site(request)
        self.token = default_token_generator.make_token(self.user)
        # будет создан экземпляр юзера по модели, 
        # извлечётся его id создастся уникальная ссылка по ней юзер подтвердит свою почту
        #переводит id пользователя в байты.
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk)) 

    def send_activate(self):
        #строит URL по имени маршрута account:user_registration, 
        # подставляя в него параметры uidb64 и token
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
        self.user.email_user(subject=subject,message=message)

def activate_email_task(user:User):
    send_email = SendEmail(user=user)
    send_email.send_activate()