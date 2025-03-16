from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import SkillProfile, Team

def index(request):
    return render(request, 'fivetool/index.html')

class EngineerListView(ListView):
    model = SkillProfile
    template_name = 'fivetool/engineer_list.html'
    context_object_name = 'engineers'
    paginate_by = 9
    
    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            return SkillProfile.objects.filter(
                Q(firstname__icontains=search_query) | 
                Q(lastname__icontains=search_query)
            ).order_by('lastname', 'firstname')
        return SkillProfile.objects.all().order_by('lastname', 'firstname')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class EngineerDetailView(DetailView):
    model = SkillProfile
    template_name = 'fivetool/engineer_detail.html'
    context_object_name = 'engineer'

class TeamListView(ListView):
    model = Team
    template_name = 'fivetool/team_list.html'
    context_object_name = 'teams'
    paginate_by = 9
    
    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = Team.objects.all()
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        # Calculate average skills for each team
        for team in queryset:
            if team.members.exists():
                team.avg_algorithms = team.members.aggregate(Avg('algorithms'))['algorithms__avg']
                team.avg_data_structures = team.members.aggregate(Avg('data_structures'))['data_structures__avg']
                team.avg_system_design = team.members.aggregate(Avg('system_design'))['system_design__avg']
                team.avg_testing = team.members.aggregate(Avg('testing'))['testing__avg']
                team.avg_debugging = team.members.aggregate(Avg('debugging'))['debugging__avg']
                team.avg_version_control = team.members.aggregate(Avg('version_control'))['version_control__avg']
                team.avg_communication = team.members.aggregate(Avg('communication'))['communication__avg']
                team.avg_teamwork = team.members.aggregate(Avg('teamwork'))['teamwork__avg']
                team.avg_problem_solving = team.members.aggregate(Avg('problem_solving'))['problem_solving__avg']
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class TeamDetailView(DetailView):
    model = Team
    template_name = 'fivetool/team_detail.html'
    context_object_name = 'team'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        
        if team.members.exists():
            # Calculate average skills
            context['avg_algorithms'] = team.members.aggregate(Avg('algorithms'))['algorithms__avg']
            context['avg_data_structures'] = team.members.aggregate(Avg('data_structures'))['data_structures__avg']
            context['avg_system_design'] = team.members.aggregate(Avg('system_design'))['system_design__avg']
            context['avg_testing'] = team.members.aggregate(Avg('testing'))['testing__avg']
            context['avg_debugging'] = team.members.aggregate(Avg('debugging'))['debugging__avg']
            context['avg_version_control'] = team.members.aggregate(Avg('version_control'))['version_control__avg']
            context['avg_communication'] = team.members.aggregate(Avg('communication'))['communication__avg']
            context['avg_teamwork'] = team.members.aggregate(Avg('teamwork'))['teamwork__avg']
            context['avg_problem_solving'] = team.members.aggregate(Avg('problem_solving'))['problem_solving__avg']
        
        return context

class TeamOrganizerView(TemplateView):
    template_name = 'fivetool/team_organizer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        context['unassigned_engineers'] = SkillProfile.objects.filter(team__isnull=True)
        return context

def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            team = Team.objects.create(name=name, description=description)
            return redirect('team-detail', pk=team.id)
    
    return redirect('team-list')

def update_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            team.name = name
            team.description = description
            team.save()
    
    return redirect('team-detail', pk=team.id)

def delete_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    if request.method == 'POST':
        # Move all engineers to unassigned
        SkillProfile.objects.filter(team=team).update(team=None)
        team.delete()
    
    return redirect('team-list')

@csrf_exempt
def update_engineer_team(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            engineer_id = data.get('engineer_id')
            team_id = data.get('team_id')
            
            engineer = get_object_or_404(SkillProfile, id=engineer_id)
            
            if team_id:
                team = get_object_or_404(Team, id=team_id)
                engineer.team = team
            else:
                engineer.team = None
                
            engineer.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})