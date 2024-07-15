from datetime import date
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory, Feedback
from .tasks import send_message_on_email


@receiver(signal=pre_save, sender=Post)
def limits_posts(sender, instance, **kwargs):
    user = instance.user
    dtoday = date.today()
    len_sender_all_now = sender.objects.filter(add_date__date=dtoday, user_id=user).count()
    if len_sender_all_now >= 3:
        raise ValidationError('Публиковать больше 3-х статей в сутки, запрещено!')



@receiver(signal=pre_save, sender=Feedback)
def notify_about_new_post(sender, instance, **kwargs):
        if instance.accept == True:
            title = 'Ответ на отклик'
            text = f'{instance.send_user.username}, Ваш отклик принят автором поста --> "{instance.post.title}"'
            send_message_on_email(user=instance.send_user, post=instance.post,
                                  text = text, title=title)

