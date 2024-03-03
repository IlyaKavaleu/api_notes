from django.urls import path
from .views import NoteListView, NoteDetailView, UserViewList, UserViewDetail
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('notes', NoteViewSet, basename='notes_detail')
# urlpatterns = router.urls
#
# user_list = UserViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# note_detail = NoteViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

urlpatterns = [
    path('notes/', NoteListView.as_view(), name='notes_list'),
    path('note_detail/<int:pk>', NoteDetailView.as_view(), name='note_detail'),
    path('users/', UserViewList.as_view(), name='users'),
    path('user_detail/<int:pk>', UserViewDetail.as_view(), name='user_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
