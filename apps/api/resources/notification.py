from django import forms
from restless.preparers import Preparer
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from restless.exceptions import BadRequest, NotFound
from .base import Resource
from apps.blog.models import Notification


class NotificationForm(forms.Form):
    message = forms.CharField(required=False)
    model = forms.CharField(required=False)
    object_id = forms.IntegerField(required=False)

    def clean_model(self):
        model = self.cleaned_data['model']
        if not model:
            return
        try:
            content_type = ContentType.objects.get_by_natural_key(
                app_label='blog', model=model.lower())
        except ContentType.DoesNotExist:
            msg = _('Model not found')
            raise forms.ValidationError(msg)
        return content_type

    def clean(self):
        data = super(NotificationForm, self).clean()
        object_id = data.get('object_id')
        content_type = data.get('models')

        try:
            obj = content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            msg = _('Object not found')
            raise forms.ValidationError(msg)

        data['content_object'] = obj



class NotificationPreparer(Preparer):
    def prepare(self, notification):
        return {
            'message': notification.message,
            'models': notification.content_type.name,
            'object_id': notification.object_id
        }


class NotificationResource(Resource):
    preparer = NotificationPreparer()

    # POST /api/notification/
    def create(self):
        form = NotificationForm(self.data)

        if not form.is_valid():
            raise BadRequest({
                'errNo': 422,
                'errDev': 'The received data did not pass validation.',
                'errMsg': _('The received data did not pass validation.'),
                'errors': form.errors
            })

        message = form.cleaned_data['message']
        content_type = form.cleaned_data['model']
        object_id = form.cleaned_data['object_id']

        new_notification = Notification.objects.create(message=message,
                                                       content_type=content_type,
                                                       object_id=object_id)
        return new_notification

    # GET /api/notification/
    def list(self):
        form = NotificationForm(self.request.GET)

        if not form.is_valid():
            raise BadRequest({
                'errNo': 422,
                'errDev': 'The received data did not pass validation.',
                'errMsg': _('The received data did not pass validation.'),
                'errors': form.errors
            })

        content_type = form.cleaned_data['model']
        object_id = form.cleaned_data['object_id']

        notifications = Notification.objects.filter(content_type=content_type,
                                                    object_id=object_id)

        return notifications

    # GET /api/notification/<pk>/
    def detail(self, pk):
        try:
            notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFound({
                'errNo': 404,
                'errDev': 'No notification found.',
                'errMsg': _('No notification found'),
            })
        return notification

    # DELETE /api/notification/<pk>
    def delete(self, pk):
        try:
            notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFound({
                'errNo': 404,
                'errDev': 'No notification found.',
                'errMsg': _('No notification found'),
            })
        notification.delete()

