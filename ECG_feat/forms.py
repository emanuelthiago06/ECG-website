from django import forms
from .models import ECG_models

class ECG_form(forms.ModelForm):
    class Meta:
        model = ECG_models
        fields = [
            "amp"
        ]