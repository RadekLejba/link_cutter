from django import forms

from links.models import Link


class CreateLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url']

    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
