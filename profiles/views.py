from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    all_skills = ['java', 'python', 'javascript']

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        skills = request.POST.getlist('skills[]')

        if form.is_valid():
            profile = form.save(commit=False)

            valid_genders = [choice[0] for choice in UserProfile.GENDER_CHOICES]
            gender = form.cleaned_data.get('gender')
            profile.gender = gender if gender in valid_genders else None

            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']

            if 'resume' in request.FILES:
                profile.resume = request.FILES['resume']

            profile.skills = skills
            profile.save()

            user = request.user
            user.name = form.cleaned_data.get('name')
            user.email = form.cleaned_data.get('email')
            user.mobile_no = form.cleaned_data.get('mobile_no')
            user.save()

            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    is_editing = request.GET.get('edit') == '1'
    skills = [skill.strip() for skill in profile.skills] if profile.skills else []

    return render(request, 'profiles/profile.html', {
        'form': form,
        'skills': skills,
        'all_skills': all_skills,
        'is_editing': is_editing,
        'profile': profile,
        'request': request
    })
