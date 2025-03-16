from django.db import models
from django.urls import reverse

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('team-detail', args=[str(self.id)])

class SkillProfile(models.Model):
    # personal data
    firstname = models.CharField(max_length=40, default="", blank=True)
    lastname = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    profile_image = models.CharField(max_length=255, blank=True, help_text="URL to profile image")
    
    # relationship data
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    start_date = models.DateField("Start Date")
    current_title = models.IntegerField(default=1, choices=[
        (1, 'Associate Engineer'),
        (2, 'Engineer'),
        (3, 'Senior Engineer'),
        (4, 'Lead Engineer'),
        (5, 'Staff Engineer'),
        (6, 'Principal Engineer'),
    ])

    # Core Programming Skills
    algorithms = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'),
        (3, 'Competent'),
        (4, 'Proficient'),
        (5, 'Expert')
    ])
    data_structures = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'), 
        (3, 'Competent'),
        (4, 'Proficient'),
        (5, 'Expert')
    ])
    system_design = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'),
        (3, 'Competent'), 
        (4, 'Proficient'),
        (5, 'Expert')
    ])

    # Software Engineering Practices
    testing = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'),
        (3, 'Competent'),
        (4, 'Proficient'), 
        (5, 'Expert')
    ])
    debugging = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'),
        (3, 'Competent'),
        (4, 'Proficient'),
        (5, 'Expert')
    ])
    version_control = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'),
        (3, 'Competent'),
        (4, 'Proficient'),
        (5, 'Expert')
    ])

    # Soft Skills
    communication = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'),
        (3, 'Competent'),
        (4, 'Proficient'),
        (5, 'Expert')
    ])
    teamwork = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'),
        (3, 'Competent'),
        (4, 'Proficient'),
        (5, 'Expert')
    ])
    problem_solving = models.IntegerField(default=1, choices=[
        (1, 'Novice'),
        (2, 'Advanced Beginner'),
        (3, 'Competent'),
        (4, 'Proficient'),
        (5, 'Expert')
    ])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Skill Profile (ID: {self.id})"
