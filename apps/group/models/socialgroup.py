from __future__ import unicode_literals
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


class SocialGroup(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True)
    description = models.TextField(default='', blank=True)
    members = models.ManyToManyField(User, blank=True, related_name='group')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SocialGroup, self).save()

    class Meta:
        ordering = ['name']
