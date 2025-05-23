from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'mobile_no', 'email', 'work_status', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['work_status'].required = True
        self.fields['work_status'].widget = forms.RadioSelect()
        self.fields['work_status'].choices = [
            ('experienced', 'Experienced'),
            ('fresher', 'Fresher'),
        ]

        for field_name in self.fields:
            self.fields[field_name].help_text = None

        self.fields['name'].widget.attrs.update({'placeholder': 'Enter full name'})
        self.fields['mobile_no'].widget.attrs.update({'placeholder': 'Enter mobile number'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter email address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

    def clean_mobile_no(self):
        mobile = self.cleaned_data.get('mobile_no')
        if not re.fullmatch(r'\d{10}', mobile):
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return mobile

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
