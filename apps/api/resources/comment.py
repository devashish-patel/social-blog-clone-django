from django.core.exceptions import ObjectDoesNotExist
from restless.exceptions import NotFound, BadRequest
from restless.preparers import Preparer
from django import forms
from apps.blog.models import Comment
from .base import Resource


class CommentPreparer(Preparer):
    def prepare(self, comment):
        return {
            'comment_id': comment.id,
            'comment': comment.message,
            'username': comment.user.username,
            'post_id': comment.post.id,
            'posted_on': comment.posted_on
        }


class CommentDeletePreparer(Preparer):
    def prepare(self, data):
        return {
            "message": data['message']
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'post', 'message']


class CommentResource(Resource):
    def prepare(self, data):
        if self.request.method == 'DELETE':
            Prep = CommentDeletePreparer
        else:
            Prep = CommentPreparer

        return Prep().prepare(data)

    # POST /api/comment/
    def create(self):
        form = CommentForm(self.data)

        if not form.is_valid():
            raise BadRequest({
                'errMsg': 'Invalid Input Data!'
            })

        new_comment = form.save()
        return new_comment

    # GET /api/comment?post=<post_id>
    def list(self):
        post_id = self.request.GET.get('post', None)

        if not post_id:
            raise BadRequest({
                'errMsg': 'Valid Post Id is required!'
            })

        comments = Comment.objects.filter(post__id=int(post_id))
        return comments

    # DELETE /api/comment/<pk>
    def delete(self, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound({
                "errMsg": 'No Comment Found!'
            })

        comment.delete()
        return {'message': 'Comment Deleted Successfully'}

