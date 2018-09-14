from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ObjectDoesNotExist
from restless.exceptions import NotFound, BadRequest
from restless.preparers import Preparer
from django.utils.translation import ugettext as _

from .base import Resource
User = get_user_model()


class UserCreateFrom(forms.UserCreationForm):
    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')
        model = User


class UserCreatePreparer(Preparer):
    def prepare(self, user):
        return {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }


class UserResource(Resource):
    preparer = UserCreatePreparer()

    def is_authenticated(self):
        return True

    # POST /api/user/
    def create(self):
        form = UserCreateFrom(self.data)

        if not form.is_valid():
            raise BadRequest({
                'errNo': 422,
                'errDev': 'The received data did not pass validation.',
                'errMsg': _('The received data did not pass validation.'),
                'errors': form.errors
            })

        new_user = form.save()

        return new_user

    # GET /api/user/<pk>/
    def detail(self, pk):
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFound({
                'errNo': 404,
                'errDev': 'No user found.',
                'errMsg': _('No user found'),
            })

        return user
