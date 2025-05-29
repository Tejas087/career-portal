from django import forms
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileForm(forms.ModelForm):
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
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = UserProfile
        fields = ['gender', 'education', 'work_experience', 'skill_input', 'photo', 'resume', 'dob']
        widgets = {
            'work_experience': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = None

        if user:
            self.fields['name'].initial = user.name
            self.fields['email'].initial = user.email
            self.fields['mobile_no'].initial = user.mobile_no

        if self.instance and self.instance.skills:
            self.fields['skill_input'].initial = ', '.join(self.instance.skills)
