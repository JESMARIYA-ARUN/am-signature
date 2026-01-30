from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StyledFormMixin:
    """
    Automatically adds Bootstrap form-control class
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control auth-input",
            "placeholder": " "   # ✅ required for Bootstrap floating labels
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control auth-input",
            "placeholder": " "   # ✅ required
        })
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": "Username",
            "email": "Email Address"
        }
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control auth-input",
                "placeholder": " "   # ✅ required
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control auth-input",
                "placeholder": " "   # ✅ required
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class LoginForm(StyledFormMixin, forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
