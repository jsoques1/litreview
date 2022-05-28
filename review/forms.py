from django import forms
# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model
from . import models

# User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]

    title = forms.CharField(label="Title", label_suffix="")
    description = forms.CharField(max_length=2048, label_suffix="")
    image = forms.ImageField(label_suffix="", required=False)


class FollowUsersForm(forms.ModelForm):

    class Meta:
        model = models.UserFollows
        fields = ["followed_user"]

