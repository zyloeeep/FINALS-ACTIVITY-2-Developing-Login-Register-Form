from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

User = get_user_model()


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        error_messages={"required": "Please enter your full name."},
    )
    email = forms.EmailField(
        error_messages={
            "required": "Please enter your email address.",
            "invalid": "Enter a valid email address.",
        },
    )
    contact_number = forms.CharField(
        max_length=20,
        error_messages={"required": "Please enter your contact number."},
    )
    password1 = forms.CharField(
        error_messages={"required": "Please enter a password."},
    )
    password2 = forms.CharField(
        error_messages={"required": "Please confirm your password."},
    )
    terms = forms.BooleanField(
        error_messages={
            "required": "You must accept the Terms and Conditions to create an account."
        },
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_contact_number(self):
        number = self.cleaned_data["contact_number"].strip()
        digits = number.replace(" ", "").replace("-", "").replace("+", "")
        if not digits.isdigit() or not 7 <= len(digits) <= 15:
            raise ValidationError("Enter a valid contact number.")
        return number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")

        if password1:
            try:
                validate_password(password1)
            except ValidationError as error:
                self.add_error("password1", error)

        return cleaned_data

    def save(self):
        return User.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            full_name=self.cleaned_data["full_name"],
            contact_number=self.cleaned_data["contact_number"],
        )
class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            "required": "Please enter your email address.",
            "invalid": "Enter a valid email address.",
        },
    )
    password = forms.CharField(
        error_messages={"required": "Please enter your password."},
    )
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(username=email.lower(), password=password)
            if self.user is None:
                raise ValidationError("Invalid email or password.")

        return cleaned_data