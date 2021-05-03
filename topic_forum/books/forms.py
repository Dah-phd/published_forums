from .models import contact
from django.forms import ModelForm


class contact_form(ModelForm):
    class Meta:
        model = contact
        fields = ['message']
