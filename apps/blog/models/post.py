from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=128)
    content = models.TextField(default='', blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True)
    published = models.BooleanField(default=False)

    class Meta(object):
        ordering = ['-posted_on', 'title']

    def update_post(self):
        from datetime import datetime
        self.updated_on = datetime.now()
        self.save()

    def publish_post(self):
        self.published = True
        self.save()

    def __unicode__(self):
        return self.title
