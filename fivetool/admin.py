from django.contrib import admin
from .models import SkillProfile, Team

# Register your models here.
@admin.register(SkillProfile)
class SkillProfileAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'current_title', 'team', 'start_date')
    list_filter = ('current_title', 'team')
    search_fields = ('lastname', 'firstname', 'email')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
