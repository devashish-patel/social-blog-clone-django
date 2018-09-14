from django.conf.urls import url, include

from .resources import PostResource, CommentResource, UserResource, \
    NotificationResource, AuthenticationResource, GroupResource

apipatterns = [
    # Application APIs
    url(r'^auth/', include(AuthenticationResource.urls())),
    url(r'^post/', include(PostResource.urls())),
    url(r'^comment/', include(CommentResource.urls())),
    url(r'^user/', include(UserResource.urls())),
    url(r'^notification/', include(NotificationResource.urls())),
    url(r'^group/', include(GroupResource.urls()))
]

urlpatterns = [
    url(r'^', include(apipatterns)),
]
