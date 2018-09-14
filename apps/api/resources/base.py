from restless.dj import DjangoResource
from restless.exceptions import HttpError
from django.core.exceptions import ObjectDoesNotExist


class Resource(DjangoResource):
    """
    This class designed to be the base class of all the api classes.
    """
    def is_true(self, val):
        if val == 'true':
            return True
        return False

    def is_authenticated(self):
        """
        By overriding this method we just simply disabling authentication for
        our API
        :return: Always `True`
        """
        user_id = self.request.META.get('HTTP_USER', None)
        token = self.request.META.get('HTTP_AUTHORIZATION', None)
        token = self.is_true(token)

        if token:
            from apps.social.models import Apikey
            if user_id:
                try:
                    apikey = Apikey.objects.get(user__id=user_id)
                except ObjectDoesNotExist:
                    return False
                return apikey.key == token
            else:
                return False
        return token

    def build_error(self, err):
        """
        Return JSON error response if an HttpError exception otherwise raise
        """

        if isinstance(err, HttpError):
            body = self.serializer.serialize(err.message)
            return self.build_response(body, status=err.status)
        else:
            raise HttpError
