from __future__ import with_statement
from django import forms
from .models import Message, Group, Friend, Good
from django.contrib.auth.models import User

# 

# Group のチェックボックスフォーム
class GroupCheckForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupCheckForm, self).__init__(*args, **kwargs)

        print('＊＊＊＊＊通過(GroupCheckForm1)')  # デバグ用
        print('＊＊＊＊＊その時 user=',user)  # デバグ用

        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.MultipleChoiceField(
            choices=[(item.title, item.title) for item in \
                Group.objects.filter(owner__in=[user, public])
            ],
            widget=forms.CheckboxSelectMultiple(),
        )

# Group の選択メニューフォーム
class GroupSelectForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) \
                for item in Group.objects.filter(owner=user)
            ],
            widget=forms.Select(attrs={'class':'form-control'}),
        )

# Friend のチェックボックスフォーム
class FriendsForm(forms.Form):
    def __init__(self, user, friends=[], vals=[], *args, **kwargs):
        super(FriendsForm, self).__init__(*args, **kwargs)
        self.fields['friends'] = forms.MultipleChoiceField(
            choices=[(item.user, item.user) for item in friends  # ←このfriendsの中にあるもの全てが、項目として表示されるらしい。 2022-04-06
            ],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals  # これで、チェックをONにする項目が決まるらしい。valsと等しい項目だけがONになる？ 2022-04-06
        )

# Group 作成フォーム
class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=50, \
        widget=forms.TextInput(attrs={'class':'form-control'})
        )

# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=500, \
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':2})
        )

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) \
                for item in Group.objects.filter(owner__in=[user, public])
            ],
            widget=forms.Select(attrs={'class':'form-control'}),
        )
        