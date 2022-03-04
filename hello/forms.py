from django import forms

class HelloForm(forms.Form):
    check = forms.BooleanField(label='Checkbox', required=False)
