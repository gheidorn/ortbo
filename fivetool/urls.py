from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("engineers/", views.EngineerListView.as_view(), name="engineer-list"),
    path("engineers/<int:pk>/", views.EngineerDetailView.as_view(), name="engineer-detail"),
    path("teams/", views.TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", views.TeamDetailView.as_view(), name="team-detail"),
    path("teams/create/", views.create_team, name="team-create"),
    path("teams/<int:pk>/update/", views.update_team, name="team-update"),
    path("teams/<int:pk>/delete/", views.delete_team, name="team-delete"),
    path("organizer/", views.TeamOrganizerView.as_view(), name="team-organizer"),
    path("api/update-engineer-team/", views.update_engineer_team, name="update-engineer-team"),
]