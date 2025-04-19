from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Comment(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments_user')
    text = models.TextField()
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={
                                         'model__in':('video',),
                                     })
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Комментарий пользователя {self.user.username}"
    