from django import forms

import requests

from .models import Link


class BasicLinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ("original_url", "identifier")

    def clean_original_url(self):
        url = self.cleaned_data['original_url']
        if "//" in url[8:]:
            raise forms.ValidationError("Don't be silly.")
        try:
            r = requests.get(url)
        except requests.exceptions.MissingSchema:
            raise forms.ValidationError("Please enter a real URL.")
        if r.status_code not in (200, 301, 302):
            raise forms.ValidationError("Please enter a working or accessible URL")
        return url
