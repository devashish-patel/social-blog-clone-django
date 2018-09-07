from django.conf.urls import url, include

from .resources import PostResource, CommentResource

apipatterns = [
    # Application APIs
    url(r'^post/', include(PostResource.urls())),
    url(r'^comment/', include(CommentResource.urls()))
    ]

urlpatterns = [
    url(r'^', include(apipatterns)),
]