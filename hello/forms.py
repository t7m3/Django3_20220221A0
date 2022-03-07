from django import forms

class HelloForm(forms.Form):
    data = [
        ('one', 'item 1'),
        ('two', 'item 2'),
        ('three', 'item 3')
    ]
    choice = forms.ChoiceField(label='Choice', \
        choices=data)
