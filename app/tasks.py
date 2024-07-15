from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from MMORPG import settings

def send_message_on_email(user, post, title, text):


    html_content = render_to_string('send.html',
                                    {
        'user': user.username,
        'text': text,
        'title' : title,
        'link' : f'{settings.SITE_URL}/posts/{post.pk}'
    }
                                )

    msg = EmailMultiAlternatives(
        subject= title,
        body=post.text[0:50],
        from_email='dimonsmile98@yandex.ru',
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def weekly_send_notify(posts, emails):
    for email in emails:
        html_content = render_to_string('weeklysend.html',
                                        {
                                            'posts': posts,
                                            'link': SITE_URL,
                                            'user' : email
                                        }
                                        )

        msg = EmailMultiAlternatives(
            subject='Публикации за неделю',
            body='',
            from_email='dimonsmile98@yandex.ru',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()