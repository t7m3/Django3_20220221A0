from django import forms

class HelloForm(forms.Form):
    data = [
        ('one', 'item 1'),
        ('two', 'item 2'),
        ('three', 'item 3'),
        ('four', 'item 4'),
        ('five', 'item 5')
    ]
    choice = forms.ChoiceField(label='radio', \
        choices=data, widget=forms.Select(attrs={'size': 5}))
