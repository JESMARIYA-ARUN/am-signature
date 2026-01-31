from django import forms
from django.contrib.auth.models import User


class StyledFormMixin:
    """
    Adds common Bootstrap styling to all form fields.
    Used to avoid repeating the same widget attributes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "autocomplete": "off",
            })


class RegisterForm(forms.ModelForm):
    """
    Custom registration form with password confirmation.
    """

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control auth-input",
            "placeholder": " ",
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control auth-input",
            "placeholder": " ",
        })
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": "Username",
            "email": "Email Address",
        }
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control auth-input",
                "placeholder": " ",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control auth-input",
                "placeholder": " ",
            }),
        }

    def clean(self):
        """
        Ensures both passwords match before saving the user.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        """
        Saves the user with a hashed password.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(StyledFormMixin, forms.Form):
    """
    Simple login form with shared styling.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
