
from .base import Resource
from restless.preparers import Preparer
from apps.group.models import SocialGroup
from django.contrib.auth import get_user_model
from django import forms
from restless.exceptions import BadRequest, NotFound
from django.utils.translation import ugettext as _
from apps.api.utils import routes
from django.core.exceptions import ObjectDoesNotExist
from restless.resources import skip_prepare
User = get_user_model()

# Preparer
class GroupPreparer(Preparer):
    def prepare(self, data):
        return {
            "group_name": data.name,
            "group_description": data.description
        }



# Forms
class GroupForm(forms.ModelForm):
    class Meta:
        model = SocialGroup
        fields = ['name', 'description']


# Resource
@routes(('PUT', r'^add_member/(?P<pk>\d+)/$', 'add_member'))
class GroupResource(Resource):

    preparer = GroupPreparer()

    # POST /api/group/
    def create(self):
        form = GroupForm(self.data)

        if not form.is_valid():
            raise BadRequest({
                'errNo': 422,
                'errDev': 'The received data did not pass validation.',
                'errMsg': _('The received data did not pass validation.'),
                'errors': form.errors
            })

        try:
            user = User.objects.get(pk=self.data['user'])
        except:
            user = None

        if user:
            new_group = form.save(commit=False)
            new_group.members.add(user)
            new_group.save()
            return form.save_m2m()
        else:
            return form.save()

    # PUT /api/group/add_member/<pk>/
    @skip_prepare
    def add_member(self, pk):
        group = SocialGroup.objects.get(pk=pk)
        print(self.data['user'])
        user = User.objects.get(pk=self.data['user'])

        if user not in group.members.all():
            group.members.add(user)

        print(group.members.all())

        return group

    # GET /api/group/
    def list(self):
        pass

    # GET /api/group/<pk>/
    def detail(self):
        pass

    # DELETE /api/group/<pk>/
    def delete(self, pk):
        pass

