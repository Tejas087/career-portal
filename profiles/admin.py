from django.contrib import admin
from django.db.models import Q
from .models import UserProfile 

# Custom admin filter to filter users by individual skills stored in JSONField
class SkillsFilter(admin.SimpleListFilter):
    title = 'Skills'  # Display name in admin sidebar
    parameter_name = 'skill'  # URL query parameter 

    def lookups(self, request, model_admin):
        """
        Returns a list of skill choices for the filter.
        Extracts unique skills from all UserProfile entries.
        """
        all_skills = set()
        for profile in UserProfile.objects.exclude(skills__isnull=True):
            if profile.skills and isinstance(profile.skills, list):
                for skill in profile.skills:
                    all_skills.add(skill.lower())  # Normalize to lowercase for consistency
        return [(skill, skill.capitalize()) for skill in sorted(list(all_skills))]

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected skill.
        Uses multiple Q objects to handle different JSON array formats.
        """
        if self.value():
            skill_to_filter = self.value().lower()
            q_objects = (
                Q(skills__icontains=f'["{skill_to_filter}"]') |          # Single skill
                Q(skills__icontains=f'["{skill_to_filter}",') |          # Skill at start
                Q(skills__icontains=f', "{skill_to_filter}",') |         # Skill in middle
                Q(skills__icontains=f', "{skill_to_filter}"]')           # Skill at end
            )
            return queryset.filter(q_objects)
        return queryset


# Register UserProfile in admin with custom display and filtering
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'gender', 'dob', 'education', 
        'work_experience', 'display_skills', 'photo', 'resume'
    )
    search_fields = ('user__email', 'user__name', 'skills')  # Allow search by user email, name, skills
    list_filter = (
        'gender', 
        'education', 
        'work_experience',
        SkillsFilter,  # Custom skill filter
    )

    # Organize form fields into sections
    fieldsets = (
        (None, {
            'fields': (
                'user', 'gender', 'dob', 'education', 
                'work_experience', 'skills', 'photo', 'resume'
            )
        }),
    )

    def display_skills(self, obj):
        #Display skills as a comma-separated string. 
        return ", ".join(obj.skills) if obj.skills else "N/A"
    display_skills.short_description = 'Skills'  # Column title in admin list view
