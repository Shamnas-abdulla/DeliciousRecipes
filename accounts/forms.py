from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Enter the password"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Confirm password"
    }))
    gender = forms.ChoiceField(choices=[
         ('M', 'Male'),
         ('F', 'Female'),
         ('O', 'Other'),
    ], widget=forms.RadioSelect)

    
    photo = forms.ImageField(required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password', 'gender', 'photo']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone_number = cleaned_data.get('phone_number')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
            
        return cleaned_data


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'photo']
        widgets = {
            'gender': forms.Select(choices=Account.GENDER_CHOICES),
        }

    # Optionally, add some custom validation or modify the field attributes
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True  # Prevent email from being changed

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import gettext_lazy as _

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure that the email exists in the database
        if not Account.objects.filter(email=email).exists():
            raise forms.ValidationError(_("No account with this email address exists."))
        return email

