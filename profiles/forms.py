from django import forms
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    # Fields from CustomUser
    name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    mobile_no = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Skills input as a single comma-separated field
    skill_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type skill and press Enter',
            'id': 'skillInput',
            'class': 'form-control'
        })
    )

    education = forms.ChoiceField(
        choices=UserProfile.EDUCATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    resume = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'})
    )

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    dob = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = [
            'name', 'email', 'mobile_no', 'dob', 'gender',
            'education', 'work_experience', 
            'skill_input', 'photo', 'resume'
        ]

        widgets = {
            'work_experience': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['gender'].empty_label = None

        # Set initial values from related User model
        if user:
            self.fields['name'].initial = user.name
            self.fields['email'].initial = user.email
            self.fields['mobile_no'].initial = user.mobile_no

        # Convert skills list to comma-separated string for skill_input
        if self.instance and self.instance.skills:
            self.fields['skill_input'].initial = ', '.join(self.instance.skills)

    def save(self, commit=True):
        # Save updated fields to User model
        user_profile = super().save(commit=False)

        # Parse skills input into a list
        skill_input = self.cleaned_data.get('skill_input', '')
        skills_list = [s.strip() for s in skill_input.split(',') if s.strip()]
        user_profile.skills = skills_list

        # Save CustomUser fields if needed
        user = self.instance.user
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.mobile_no = self.cleaned_data.get('mobile_no')
        if commit:
            user.save()
            user_profile.save()
        return user_profile
