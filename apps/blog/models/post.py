from django.contrib.auth import get_user_model
from django.db import models
from apps.group.models import SocialGroup

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=128)
    content = models.TextField(default='', blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True)
    published = models.BooleanField(default=False)
    group = models.ForeignKey(SocialGroup, related_name='post', null=True, blank=True)

    class Meta(object):
        ordering = ['-posted_on', 'title']
        unique_together = ('title', 'author')

    def update_post(self):
        from datetime import datetime
        self.updated_on = datetime.now()
        self.save()

    def publish_post(self):
        self.published = True
        self.save()

    def __unicode__(self):
        return self.title
