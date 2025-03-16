# Generated by Django 5.1.6 on 2025-02-15 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SkillProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=40)),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('current_title', models.IntegerField(choices=[(1, 'Associate Engineer'), (2, 'Engineer'), (3, 'Senior Engineer'), (4, 'Lead Engineer'), (5, 'Staff Engineer'), (6, 'Principal Engineer')], default=1)),
                ('algorithms', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('data_structures', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('system_design', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('testing', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('debugging', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('version_control', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('communication', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('teamwork', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('problem_solving', models.IntegerField(choices=[(1, 'Novice'), (2, 'Advanced Beginner'), (3, 'Competent'), (4, 'Proficient'), (5, 'Expert')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
