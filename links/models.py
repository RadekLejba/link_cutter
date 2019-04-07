import random
import string

from django.db import models


class Link(models.Model):
    url = models.URLField(max_length=10000)
    visits = models.IntegerField(default=0)
    shortcut = models.CharField(max_length=20, unique=True, primary_key=True)
    sender_ip = models.CharField(max_length=20, null=True)
    sender_system_info = models.TextField(null=True)
    sender_referer = models.TextField(null=True)

    def __str__(self):
        return self.shortcut

    def get_url(self):
        self.visits += 1
        self.save()
        return self.url

    def generate_shortcut(self, sequence_length):
        shortcut = ''
        unique = False

        while unique is False:
            signs = (
                string.ascii_uppercase + string.digits + string.ascii_lowercase
            )
            shortcut = ''.join(
                random.choices(signs, k=sequence_length)
            )

            try:
                self.__class__.objects.get(shortcut=shortcut)
            except self.__class__.DoesNotExist:
                unique = True
            else:
                pass

        self.shortcut = shortcut
