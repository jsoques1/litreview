from django import forms
# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model
from django.template.defaultfilters import mark_safe
from . import models

# User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]

    title = forms.CharField(label=mark_safe('<strong>Titre</strong>'),
                            widget=forms.TextInput(attrs={"class": "field", "placeholder": "Titre"}))
    description = forms.CharField(label=mark_safe('<strong>Description</strong>'), max_length=2048,
                                  widget=forms.TextInput(attrs={"class": "field", "placeholder": "Description"}))
    image = forms.ImageField(label=mark_safe('<strong>Image</strong>'), required=False)


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ["followed_user"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]

    headline = forms.CharField(label=mark_safe('<strong>Titre</strong>'),
                               widget=forms.TextInput(attrs={"class": "field", "placeholder": "Titre"}))
    body = forms.CharField(label=mark_safe('<strong>Commentaire</strong>'), max_length=2048,
                           widget=forms.TextInput(attrs={"class": "field", "placeholder": "Commentaire"}))
    rating = forms.ChoiceField(label="Note", widget=forms.RadioSelect,
                               choices=[(0, "- 0"), (1, "- 1"), (2, "- 2"), (3, "- 3"), (4, "- 4"), (5, "- 5")])
