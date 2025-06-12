from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile
from django.db.models import Q
from django.http import HttpResponse
from django.utils.timezone import localtime
from openpyxl import Workbook


@staff_member_required
def export_filter_page(request):
    """
    Admin-only view to filter UserProfiles by various criteria
    and optionally download the filtered data as an Excel file.
    """

    queryset = UserProfile.objects.select_related('user').all()

    # Get filter parameters from the query string
    gender = request.GET.get('gender')
    education = request.GET.get('education')
    work_experience = request.GET.get('work_experience')
    created_date = request.GET.get('created_date')
    skills_input = request.GET.get('skills')
    download = request.GET.get('download')

    # Apply filters if the parameters are provided
    if gender:
        queryset = queryset.filter(gender__iexact=gender)
    if education:
        queryset = queryset.filter(education__icontains=education)
    if work_experience:
        queryset = queryset.filter(work_experience__icontains=work_experience)
    if created_date:
        queryset = queryset.filter(created_at__date__gte=created_date)

    # Convert queryset to list for easier Python filtering below
    queryset = list(queryset)

    # Filter profiles by skills if skills input is provided
    if skills_input:
        input_skills = [s.strip().lower() for s in skills_input.split(',') if s.strip()]

        # Keep only profiles where all input skills exist in profile.skills
        queryset = [
            profile for profile in queryset
            if profile.skills and all(skill in [s.lower() for s in profile.skills] for skill in input_skills)
        ]

    # If 'download=1' in GET params, generate and return an Excel file
    if download == "1":
        wb = Workbook()
        ws = wb.active
        ws.title = "Profiles"

        # Write header row
        ws.append(['Name', 'Email', 'Mobile', 'Gender', 'Education', 'Work Experience', 'Skills', 'Created At'])

        # Write data rows for each filtered profile
        for profile in queryset:
            ws.append([
                profile.user.name,
                profile.user.email,
                profile.user.mobile_no,
                profile.gender or '',
                profile.education or '',
                profile.work_experience or '',
                ', '.join(profile.skills) if profile.skills else '',
                localtime(profile.created_at).strftime('%Y-%m-%d'),
            ])

        # Prepare HTTP response with Excel content type and attachment headers
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="filtered_profiles.xlsx"'

        # Save workbook to response and return it
        wb.save(response)
        return response

    # Render template with filtered profiles and current filter selections for form pre-fill
    return render(request, 'profiles/export_filter_page.html', {
        'profiles': queryset,
        'selected_filters': {
            'gender': gender,
            'education': education,
            'work_experience': work_experience,
            'created_date': created_date,
            'skills': skills_input,
        }
    })


@login_required
def profile_view(request):
    """
    View to display and edit the logged-in user's profile.
    GET shows the profile form,
    POST updates the profile with submitted data.
    """

    # Get or create the profile for the current user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Example list of all skills (could be dynamic or from DB)
    all_skills = ['java', 'python', 'javascript']

    if request.method == 'POST':
        # Bind form with POST data, files, and instance to update
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)

        # Skills submitted as list from JS frontend (skills[] inputs)
        skills = request.POST.getlist('skills[]')

        if form.is_valid():
            profile = form.save(commit=False)

            # Validate gender against allowed choices for extra safety
            valid_genders = [choice[0] for choice in UserProfile.GENDER_CHOICES]
            gender = form.cleaned_data.get('gender')
            profile.gender = gender if gender in valid_genders else None

            # Update photo and resume files if new ones uploaded
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            if 'resume' in request.FILES:
                profile.resume = request.FILES['resume']

            # Assign skills list from submitted data
            profile.skills = skills

            # Save profile to DB
            profile.save()

            # Also update the linked User fields from form data
            user = request.user
            user.name = form.cleaned_data.get('name')
            user.email = form.cleaned_data.get('email')
            user.mobile_no = form.cleaned_data.get('mobile_no')
            user.save()

            # Redirect to profile page (GET) after successful update
            return redirect('profile')

    else:
        # On GET, instantiate form with existing profile and user data
        form = UserProfileForm(instance=profile, user=request.user)

    # Check if editing mode requested via query string ?edit=1
    is_editing = request.GET.get('edit') == '1'

    # Prepare current skills for display in template
    skills = [skill.strip() for skill in profile.skills] if profile.skills else []

    # Render profile page template with form and context data
    return render(request, 'profiles/profile.html', {
        'form': form,
        'skills': skills,
        'all_skills': all_skills,
        'is_editing': is_editing,
        'profile': profile,
        'request': request
    })
