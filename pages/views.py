from django.shortcuts import render, redirect
from accounts.models import Team
from projects.models import Project, Issue

# Create your views here.
def index(request):
    # return render(request, 'pages/index.html')
    return redirect('dashboard')

def leaderboard(request):
    teams = Team.objects.all().order_by('-totalPoints')
    length = len(teams)
    n = range(1, length+1)

    dictionary = {}
    position = []

    for x in n:
        position.append(x)

    for key,val in zip(position,teams):
        dictionary[key] = val

    context = {
        'teams': teams, 'dictionary':dictionary,
    }
    return render(request, 'pages/leaderboard.html', context)

def notifications(request):
    projects = Project.objects.filter(is_submitted=True)
    projects_counter = len(projects)
    issues = Issue.objects.all().order_by("-post_date")
    issues_counter = len(issues)
    
    context = {
        'projects':projects,
        'projects_counter':projects_counter,
        'issues_counter': issues_counter,
        'issues': issues
    }
    return render(request, 'pages/notifications.html', context)

def error_404(request, exception):
    return render(request, 'pages/error_404.html', status=404)

def error_500(request):
    data = {}
    return render(request, 'pages/error_500.html', data)

def error_403(request, exception):
    return render(request, 'pages/error_403.html', status=403)