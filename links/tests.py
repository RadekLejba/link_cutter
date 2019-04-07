from http import HTTPStatus
import string

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from links.models import Link


class LinkModelTestCase(TestCase):
    def setUp(self):
        self.link = Link.objects.create(
            url='http://www.test.pl',
            shortcut='test',
        )
        self.link2 = Link.objects.create(
            url='http://www.test2.pl',
            shortcut='test2',
        )

    def test_generate_shortcut(self):
        signs = string.ascii_uppercase + string.digits + string.ascii_lowercase

        self.link.generate_shortcut(6)
        self.link2.generate_shortcut(14)

        self.assertEqual(len(self.link.shortcut), 6)
        self.assertEqual(len(self.link2.shortcut), 14)
        for sign in self.link.shortcut:
            self.assertIn(sign, signs)
        for sign in self.link2.shortcut:
            self.assertIn(sign, signs)

    def test_visits(self):
        for i in range(10):
            self.link2.get_url()

        self.assertEqual(self.link.visits, 0)
        self.assertEqual(self.link2.visits, 10)


class CreateLinkViewViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('links:create_link')
        self.link = Link.objects.create(
            url='http://www.test.pl',
            shortcut='test',
        )

    def test_correct_success_link(self):
        url = 'http://www.test2.pl/'

        response = self.client.post(self.url, {'url': url})

        link = Link.objects.get(url=url)
        self.assertEqual(
            response.url,
            reverse('links:get_link', kwargs={'shortcut': link.shortcut}),
        )

    def test_create_new_link(self):
        url = 'http://www.test2.pl/'

        self.client.post(self.url, {'url': url})

        links = Link.objects.all()
        newlink = Link.objects.get(url=url)

        self.assertEqual(len(links), 2)
        self.assertEqual(newlink.url, url)

    def test_create_existing_link(self):
        url = 'http://www.test.pl'

        self.client.post(self.url, {'url': url})

        links = Link.objects.all()
        newlink = Link.objects.get(url=url)

        self.assertEqual(len(links), 1)
        self.assertEqual(newlink.url, url)


class GetLinkViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = 'links:get_link'
        self.link = Link.objects.create(
            url='http://www.test.pl',
            shortcut='test',
        )

    def test_context_for_existing_link(self):
        response = self.client.get(
            reverse(self.url, kwargs={'shortcut': self.link.shortcut})
        )

        self.assertEqual(
            response.context['shortcut'],
            'testserver/{}'.format(self.link.shortcut)
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_existing_link(self):
        response = self.client.get(
            reverse(self.url, kwargs={'shortcut': 'randomshortcut'})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse('links:create_link'))


class RedirectLinkViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = 'redirect'
        self.link = Link.objects.create(
            url='http://www.test.pl',
            shortcut='test',
        )

    def test_redirect(self):
        response = self.client.get(
            reverse(self.url, kwargs={'shortcut': self.link.shortcut})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, self.link.url)

    def test_redirect_with_no_args(self):
        response = self.client.get(reverse(self.url))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse('links:create_link'))


class LinkDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = 'links:link_details'
        self.link = Link.objects.create(
            url='http://www.test.pl',
            shortcut='test',
        )

    def test_context(self):
        response = self.client.get(
            reverse(self.url, kwargs={'pk': self.link.shortcut})
        )
        link = response.context.get('link')

        self.assertEqual(link.shortcut, self.link.shortcut)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class SetShortcutLengthViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = 'links:shortcut_length'
        self.link = Link.objects.create(
            url='http://www.test.pl',
            shortcut='test',
        )

    def change_shortcut_length(self):
        response = self.client.post(self.url, {'shortcut_length': 11})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(settings.SHORTCUT_LENGTH, 11)
