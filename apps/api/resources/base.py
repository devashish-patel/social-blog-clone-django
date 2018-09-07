from restless.dj import DjangoResource
from restless.exceptions import HttpError



class Resource(DjangoResource):
    """
    This class designed to be the base class of all the api classes.
    """

    def is_authenticated(self):
        """
        By overriding this method we just simply disabling authentication for
        our API
        :return: Always `True`
        """
        return True

    def build_error(self, err):
        """
        Return JSON error response if an HttpError exception otherwise raise
        """

        if isinstance(err, HttpError):
            body = self.serializer.serialize(err.message)
            return self.build_response(body, status=err.status)
        else:
            raise HttpError
