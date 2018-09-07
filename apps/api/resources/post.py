from django import forms
from django.core.exceptions import ObjectDoesNotExist
from restless.exceptions import NotFound, BadRequest
from restless.preparers import Preparer

from apps.blog.models import Post
from .base import Resource
from .comment import CommentPreparer


class PostCreatePreparer(Preparer):
    def prepare(self, post):
        """
        Overriding the default preparer, so we can manipulate and change the
            returned data as we need.
        :param post: post object
        :return: JSON response in our desired format.
        """
        comment_preparer = CommentPreparer()
        return {
            'id': post.id,
            'title': post.title,
            'author': post.author.username,
            'content': post.content,
            'posted_on': post.posted_on,
            'comments': [comment_preparer.prepare(comment)
                         for comment in post.comments.all()],
            'published': post.published
        }


class PostUpdatePreparer(PostCreatePreparer):
    def prepare(self, post):
        prepared = super(PostUpdatePreparer, self).prepare(post)
        prepared['updated_on'] = post.updated_on
        return prepared


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'content']


class PostResource(Resource):
    def prepare(self, data):
        if self.request.method == 'PUT':
            Prep = PostUpdatePreparer
        else:
            Prep = PostCreatePreparer

        return Prep().prepare(data)

    # POST /api/post/
    def create(self):
        form = PostForm(self.data)

        if not form.is_valid():
            raise BadRequest

        new_post = form.save()
        return new_post

    # GET /api/post/
    def list(self):
        return Post.objects.all()

    # GET /api/post/<pk>/
    def detail(self, pk):
        try:
            post = Post.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise NotFound({
                "errMsg": 'No Post Found!'
            })
        return post

    # PUT /api/post/<pk>/ --OR-- PUT /api/post/<pk>/?publish=true/false
    def update(self, pk):
        publish = self.request.GET.get('publish', None)
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound({
                "errMsg": 'No Post Found!'
            })

        if publish and publish == 'true':
            post.publish_post()
            return post

        form = PostForm(self.data)

        if not form.is_valid():
            raise BadRequest({
                "errMsg": "Invalid Data!"
            })

        post.title = form.cleaned_data['title']
        post.author = form.cleaned_data['author']
        post.content = form.cleaned_data['content']
        post.save()
        post.update_post()
        return post

    # DELETE /api/post/<pk>/
    def delete(self, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound({
                "errMsg": 'No Post Found!'
            })

        post.delete()

