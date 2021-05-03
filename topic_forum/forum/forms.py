from django.forms import ModelForm
from forum.models import comment
from login.models import DM, friend_list


class comment_form(ModelForm):
    class Meta:
        model = comment
        fields = ['post_title', 'text']


class DMform(ModelForm):
    class Meta:
        model = DM
        fields = ['message_subject', 'message']


class adding_friend(ModelForm):
    class Meta:
        model = friend_list
        fields = ['friend']
