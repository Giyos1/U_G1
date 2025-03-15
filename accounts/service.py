from django.utils import timezone

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

from accounts.models import Code
from accounts.utils import code_generate
from threading import Thread


def send_email_letter(to):
    send_mail(
        subject='Test subject',
        message='test messege',
        from_email='giyosoripov4@gmail.com',
        recipient_list=[to],
        html_message="""
            <main>
                <h1>Xush kelibsiz!</h1>
                <p>bizlar xursandmiz.</p>
            </main>
        """
    )


def send_email_file_and_txt():
    path = 'file.pdf'

    email = EmailMessage(
        subject='Test',
        body='test messege',
        from_email='giyosoripov4@gmail.com',
        to=['giyosoripov4@gmail.com']
    )

    with open(path, "rb") as f:
        email.attach("file.pdf", f.read(), "application/pdf")
        email.send()


def send_email_alternative(to, user):
    reset_link = 'http://127.0.0.1:8000/accounts/restore_password/'
    subject = 'Forget password'
    from_email = 'giyosoripov4@gmail.com'
    to = [to]
    text_content = 'test'
    code = code_generate()
    time = timezone.now()
    Code.objects.create(code_number=code, user=user)
    html_c = f"""
    <main>
        <h1>Salom, {user.username}!</h1>
        <h2> code {code} </h2>
        <p>Sizning hisobingiz uchun parolni tiklash so‘rovi qabul qilindi.</p>
        <p>Agar bu so‘rovni siz bajargan bo‘lsangiz, davom etish uchun quyidagi tugmani bosing.</p>
        <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; margin-top: 10px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Parolni Tiklash</a>
        <p>Agar bu so‘rov sizga tegishli bo‘lmasa, hech qanday harakat qilishingiz shart emas.</p>
        
        <h1>{time}<h1>
    </main> 
    """

    email = EmailMultiAlternatives(
        subject, text_content, from_email, to
    )

    email.attach_alternative(html_c, 'text/html')
    email.send()


def send_email_async(to, user):
    thread1 = Thread(target=send_email_alternative, args=(to, user,))
    thread1.start()


def send_email_async_welcome(to):
    thread1 = Thread(target=send_email_letter, args=(to,))
    thread1.start()
