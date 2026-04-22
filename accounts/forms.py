from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate

from accounts.models import User, UserProfile


class CustomSignupForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICE,
        required=False,
        label="Select Role",
        widget=forms.Select(
            attrs={
                "class": "input",
                "id": "role",
            }
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "id": "password1",
                "placeholder": "••••••••",
                "required": "required",
                "minlength": "6",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "id": "password2",
                "placeholder": "Confirm Password",
                "required": "required",
                "minlength": "6",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "role")
        exclude = ('role',)

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "input",
                    "id": "first_name",
                    "placeholder": "First Name",
                    "required": "required",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "input",
                    "id": "last_name",
                    "placeholder": "Last Name",
                    "required": "required",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "input",
                    "id": "username",
                    "placeholder": "Username",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "input",
                    "id": "email",
                    "placeholder": "you@company.com",
                    "required": "required",
                }
            ),
        }


class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "id": "email",
                "placeholder": "you@company.com",
                "required": "required",
            }
        ),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "id": "password",
                "placeholder": "••••••••",
                "required": "required",
                "minlength": "6",
            }
        ),
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'address_line_1', 'address_line_2', 'address_line_3',
            'district', 'state', 'country', 'zip_code',
            'is_organization', 'organization_name',
            'profile_image', 'cover_image'
        ]