from django.urls import path

from links.views import (
    CreateLinkView, GetLinkView, LinkDetailView, SetShortcutLengthView
)

app_name = 'links'
urlpatterns = [
    path('create_link', CreateLinkView.as_view(), name='create_link'),
    path('get_link/<str:shortcut>', GetLinkView.as_view(), name='get_link'),
    path(
        'get_link/<pk>/stats',
        LinkDetailView.as_view(),
        name='link_details',
    ),
    path(
        'shortcut_length',
        SetShortcutLengthView.as_view(),
        name='shortcut_length'
    ),
]
