from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from links.forms import CreateLinkForm
from links.models import Link


class CreateLinkView(CreateView):
    form_class = CreateLinkForm
    model = Link
    success_url = 'index'
    template_name = 'links/create_link.html'

    def fill_form(self, form):
        form.instance.sender_ip = self.request.META.get('REMOTE_ADDR')
        form.instance.sender_system_info = self.request.META.get(
            'HTTP_USER_AGENT'
        )
        form.instance.sender_referer = self.request.META.get('HTTP_REFERER')
        form.instance.generate_shortcut(settings.SHORTCUT_LENGTH)
        return super().form_valid(form)

    def form_valid(self, form):
        url = form.cleaned_data['url']
        try:
            link = Link.objects.get(url=url)
        except Link.DoesNotExist:
            return self.fill_form(form)
        else:
            return redirect('links:get_link', shortcut=link.shortcut)

    def get_success_url(self, **kwargs):
        self.object.shortcut
        return reverse(
            'links:get_link',
            kwargs={'shortcut': self.object.shortcut},
        )


class GetLinkView(TemplateView):
    shortcut = ''
    template_name = 'links/get_link.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['shortcut'] = '{}/{}'.format(
            self.request.get_host(), self.shortcut
        )
        return context

    def dispatch(self, request, **kwargs):
        try:
            link = Link.objects.get(shortcut=kwargs['shortcut'])
        except Link.DoesNotExist:
            return redirect('links:create_link')
        else:
            self.shortcut = link.shortcut
            return super().dispatch(request, kwargs)


class RedirectLinkView(View):
    def get(self, *args, **kwargs):
        try:
            link = Link.objects.get(shortcut=kwargs.get('shortcut', ''))
        except Link.DoesNotExist:
            return redirect('links:create_link')
        else:
            link.visits
            return redirect(link.get_url())


class LinkDetailView(DetailView):
    model = Link


class SetShortcutLengthView(TemplateView):
    template_name = 'links/shortcut_length.html'

    def post(self, request, **kwargs):
        settings.SHORTCUT_LENGTH = int(
            self.request.POST.get('shortcut_length', '5')
        )
        return redirect('links:create_link')
