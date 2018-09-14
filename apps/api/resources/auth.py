from django import forms
from apps.social.models import Apikey
from restless.preparers import Preparer
from restless.dj import DjangoResource
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()


class AuthenticationForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class LoginPreparer(Preparer):
    def prepare(self, data):
        if data:
            return {
                "login": data.key,
                "user": data.user.id
            }
        return {
            "login": data,
            "user": None
        }


class LogoutPreparer(Preparer):
    def prepare(self, data):
        return {
            "logout": data
        }


class AuthenticationResource(DjangoResource):

    def prepare(self, data):
        if self.request.method == 'POST':
            Prep = LoginPreparer
        elif self.request.method == 'DELETE':
            Prep = LogoutPreparer

        return Prep().prepare(data)

    def is_authenticated(self):
        return True

    # POST /api/auth/
    def create(self):
        creds = AuthenticationForm(self.data)

        if creds.is_valid():
            username = creds.cleaned_data['username']
            password = creds.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                try:
                    new_key = Apikey.objects.get(user=user, key=True)
                except ObjectDoesNotExist:
                    new_key = Apikey.objects.create(user=user, key=True)
                return new_key
            else:
                return False
        else:
            return False

    # DELETE /api/auth/<username>
    def delete(self, pk):
        try:
            apikey = Apikey.objects.get(user__username=pk)
        except ObjectDoesNotExist:
            return False

        apikey.delete()
        return True
