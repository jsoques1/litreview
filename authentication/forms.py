from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)

    username = forms.CharField(label="",
                               widget=forms.TextInput(attrs={"class": "field", "placeholder": "Nom d’utilisateur"}))

    password1 = forms.CharField(label="",
                                widget=forms.PasswordInput(attrs={"class": "field", "placeholder": "Mot de Passe"}))
    password2 = forms.CharField(label="",
                                widget=forms.PasswordInput(
                                    attrs={"class": "field", "placeholder": "Confirmer Mot de Passe"}))
# class SignupForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = ('username', 'email', 'first_name', 'last_name',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="",
                               widget=forms.TextInput(attrs={"class": "validate", "placeholder": "Nom d’utilisateur"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Mot de Passe"}))
