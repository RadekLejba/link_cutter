from django.contrib import admin
from django.urls import include, path

from links.views import RedirectLinkView

app_name = 'app'
urlpatterns = [
    path('', RedirectLinkView.as_view(), name='redirect'),
    path('<str:shortcut>', RedirectLinkView.as_view(), name='redirect'),
    path('link/', include('links.urls', namespace='links')),
    path('admin/', admin.site.urls),
]
