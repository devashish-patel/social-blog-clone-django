from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey('blog.Post', related_name='comments')
    message = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        ordering = ['-posted_on']

    def __unicode__(self):
        return self.message
