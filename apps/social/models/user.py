from django.contrib.auth.models import User, PermissionsMixin


class SocialUser(User, PermissionsMixin):

    def __unicode__(self):
        return '@{0}'.format(self.username)

