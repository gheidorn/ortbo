import os
import sys
import random
import datetime
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ortbo.settings')
import django
django.setup()

from fivetool.models import Team, SkillProfile

# Sample data
FIRST_NAMES = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth',
             'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen',
             'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra',
             'Donald', 'Ashley', 'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
             'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa', 'Edward', 'Deborah',
             'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon', 'Jeffrey', 'Laura', 'Ryan', 'Cynthia',
             'Jacob', 'Kathleen', 'Gary', 'Amy', 'Nicholas', 'Shirley', 'Eric', 'Angela', 'Jonathan', 'Helen',
             'Stephen', 'Anna', 'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Emma',
             'Benjamin', 'Samantha', 'Samuel', 'Katherine', 'Gregory', 'Christine', 'Frank', 'Debra', 'Alexander', 'Rachel']

LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
            'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
            'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
            'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
            'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
            'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes',
            'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper',
            'Peterson', 'Bailey', 'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson',
            'Watson', 'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz', 'Hughes',
            'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers', 'Long', 'Ross', 'Foster', 'Jimenez']

TEAM_NAMES = [
    "Frontend Wizards", 
    "Backend Brigade", 
    "DevOps Dynamos", 
    "QA Guardians"
]

TEAM_DESCRIPTIONS = [
    "Our frontend team specializes in creating intuitive, responsive user interfaces with modern frameworks and a focus on accessibility.", 
    "Database experts and API architects who build the backbone of our applications with scalability in mind.", 
    "Infrastructure specialists who ensure our deployment pipelines and production environments are reliable and efficient.", 
    "Quality assurance engineers who maintain high standards through comprehensive automated and manual testing protocols."
]

def generate_random_date(start_year=2015, end_year=2023):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)

def create_teams():
    """Create 4 teams"""
    teams = []
    for i in range(4):
        team, created = Team.objects.get_or_create(
            name=TEAM_NAMES[i],
            defaults={
                'description': TEAM_DESCRIPTIONS[i]
            }
        )
        teams.append(team)
        print(f"{'Created' if created else 'Found'} team: {team.name}")
    return teams

def create_engineers(num_engineers, teams):
    """Create specified number of engineers with random skills"""
    for i in range(num_engineers):
        # Generate a unique combination of first and last name
        firstname = random.choice(FIRST_NAMES)
        lastname = random.choice(LAST_NAMES)
        
        # Calculate a start date between 1-8 years ago
        start_date = generate_random_date()
        
        # Assign a title based partly on start date (seniority)
        years_experience = (timezone.now().date() - start_date).days / 365
        if years_experience < 2:
            title_weight = [70, 25, 5, 0, 0, 0]  # Mostly junior
        elif years_experience < 4:
            title_weight = [20, 50, 25, 5, 0, 0]  # Mostly mid-level
        elif years_experience < 6:
            title_weight = [5, 20, 50, 20, 5, 0]  # Mostly senior
        else:
            title_weight = [0, 5, 30, 40, 20, 5]  # Mostly lead/staff
            
        title = random.choices([1, 2, 3, 4, 5, 6], weights=title_weight)[0]
        
        # Assign to a random team (20% chance of being unassigned)
        team = random.choice([None] + teams) if random.random() < 0.8 else None
        
        # Generate skill ratings based on experience and some randomness
        base_skill = min(5, max(1, int(years_experience * 0.6) + 1))
        
        # Create the engineer
        engineer = SkillProfile(
            firstname=firstname,
            lastname=lastname,
            email=f"{firstname.lower()}.{lastname.lower()}@example.com",
            start_date=start_date,
            current_title=title,
            team=team,
            
            # Core programming skills - based on experience with some randomness
            algorithms=min(5, max(1, base_skill + random.randint(-1, 1))),
            data_structures=min(5, max(1, base_skill + random.randint(-1, 1))),
            system_design=min(5, max(1, base_skill + random.randint(-1, 1))),
            
            # Engineering practices - more random
            testing=random.randint(1, 5),
            debugging=random.randint(1, 5),
            version_control=random.randint(1, 5),
            
            # Soft skills - independent of experience
            communication=random.randint(1, 5),
            teamwork=random.randint(1, 5),
            problem_solving=random.randint(1, 5)
        )
        engineer.save()
        print(f"Created engineer: {engineer.firstname} {engineer.lastname} ({engineer.get_current_title_display()})")

def main():
    print("Adding example data to Ortbo...")
    
    # Check if data already exists
    existing_teams = Team.objects.count()
    existing_engineers = SkillProfile.objects.count()
    
    if existing_teams >= 4 and existing_engineers >= 100:
        print(f"Database already has {existing_teams} teams and {existing_engineers} engineers. No data added.")
        return
    
    # Create teams and engineers
    teams = create_teams()
    
    # Calculate how many more engineers to create
    engineers_to_create = max(0, 100 - existing_engineers)
    if engineers_to_create > 0:
        create_engineers(engineers_to_create, teams)
        print(f"Added {engineers_to_create} engineers to reach a total of {existing_engineers + engineers_to_create}")
    
    print("Example data creation complete!")

if __name__ == "__main__":
    main()