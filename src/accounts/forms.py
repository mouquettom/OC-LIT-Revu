from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data['username'].strip()

        if not username:
            raise forms.ValidationError(
                "Veuillez saisir un nom d'utilisateur."
            )

        if " " in username:
            raise forms.ValidationError(
                "Le nom d'utilisateur ne peut pas contenir d'espaces. Utilisez par exemple un underscore : nom_prenom."
            )

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Ce nom d'utilisateur est déjà utilisé."
            )

        return username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")