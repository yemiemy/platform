from django.shortcuts import render, get_object_or_404, redirect
from projects.models import Project, Issue, Solution, Feedback
from accounts.models import Team
from django.contrib import messages
from datetime import datetime
import pytz


# Create your views here.
def create(request):
    if request.POST:
        title = request.POST['title']
        description = request.POST['description']
        point = request.POST['point']
        startdate = request.POST['startdate']
        deadline = request.POST['deadline']

        project = Project.objects.create(title=title, description=description, point=point, startdate=startdate, deadline=deadline)

        if 'attachment' in request.FILES:
            attachment = request.FILES['attachment']
            project.attachment = attachment
            
        project.save()

        messages.success(request, 'Project successfully created!')
        return redirect ('assign_project',project.id)
        
    return render(request, 'projects/create.html')

def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context ={
        'project':project,
    }
    return render(request, 'projects/project.html', context)

def projects(request):
    all_projects = Project.objects.all().order_by('-startdate')
    all_projects_counter = len(all_projects)
    active_projects = Project.objects.all().filter(is_accepted=False)
    active_projects_counter = len(active_projects)
    accepted_projects = Project.objects.all().filter(is_accepted=True)
    accepted_projects_counter = len(accepted_projects)
    context = {
        'all_projects': all_projects,
        'active_projects': active_projects,
        'accepted_projects': accepted_projects,
        'all_projects_counter': all_projects_counter,
        'active_projects_counter': active_projects_counter,
        'accepted_projects_counter': accepted_projects_counter,
    }
    return render(request, 'projects/projects.html', context)

def team_projects(request, team_id):
    team = Team.objects.get(id=team_id)
    all_projects = Project.objects.filter(team=team).order_by('-startdate')
    all_projects_counts = len(all_projects)
    active_projects = all_projects.filter(is_accepted=False)
    active_projects_counts = len(active_projects)
    accepted_projects = all_projects.filter(is_accepted=True)
    accepted_projects_counts = len(accepted_projects)
    context = {
        'all_projects': all_projects,
        'all_projects_counts': all_projects_counts,
        'active_projects': active_projects,
        'active_projects_counts': active_projects_counts,
        'accepted_projects': accepted_projects,
        'accepted_projects_counts': accepted_projects_counts,
    }
    return render(request, 'projects/team_projects.html', context)

def assign_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.POST:
        team = request.POST['team']
        team = Team.objects.get(id=team)
        project.team = team
        project.is_assigned = True
        project.save()
        messages.success(request, 'Project successfully assigned!')
        return redirect('dashboard')


    teams = Team.objects.all()

    context={
        "project":project, 'teams':teams,
    }
    return render(request, 'projects/assign-project.html', context)


def submit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.POST:
        utc = pytz.UTC
        deadline = str(project.deadline)
        deadline = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S%z')
        deadline = deadline.replace(tzinfo=utc)
        now = datetime.now()
        now = now.replace(tzinfo=utc)

        details = request.POST['details']

        solution = Solution.objects.create(details=details)

        if 'attachment' in request.FILES:
            solution.attachment = request.FILES['attachment']

        solution.save()

        project.is_submitted =True
        project.solution = solution

        project.save()

        
        if now < deadline:
            team = project.team
            team.pendingPoints = project.point
            team.save()
            messages.success(request, 'Congratulations! Project submitted Successfully before deadline!')
            return redirect('dashboard')
        else:
            project.team.pendingPoints = 0
            project.save()
            messages.success(request, "Sorry! Project submitted successfully but you didn't meet the deadline")
            return redirect('dashboard')
    context = {
        'project':project
    }
    return render(request, 'projects/submit-project.html', context)

def solution(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project':project,
    }
    return render(request, 'projects/solution.html', context)

def confirm_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.GET:
        team = project.team
        team.totalPoints += team.pendingPoints
        team.pendingPoints = 0
        team.save()
        project.is_accepted = True
        project.is_submitted = False
        project.save()
        messages.success(request, 'Project confirmed and leaderboard updated successfully')

        return redirect('dashboard')

    context = {
        'project': project,
    }

    return render(request, 'projects/confirm-project.html', context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.POST:
        project.delete()
        messages.success(request, 'Project successfully deleted!')
        return redirect('dashboard')

    context = {
        'project':project
    }
    return render(request, 'projects/delete-project.html', context)

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    teams = Team.objects.all()

    if request.POST:
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.point = request.POST['point']
        project.startdate = request.POST['startdate']
        project.deadline = request.POST['deadline']
        team = request.POST['team']

        project.team = Team.objects.get(id=team)

        if 'attachment' in request.FILES:
            project.attachment = request.FILES['attachment']
            
        project.save()

        messages.success(request, 'Project successfully Updated!')
        return redirect ('dashboard')

    context = {
        'project':project, 'teams':teams,
    }
    return render(request, 'projects/edit-project.html', context)

def issues(request):
    issues = Issue.objects.all().order_by('-post_date')

    context = {
        "issues": issues,
    }
    
    return render(request, 'projects/issues.html', context)

def create_issue(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.POST:
        title = request.POST['title']
        message = request.POST['message']

        issue = Issue.objects.create(title=title, message=message, project=project)
        issue.save()

        messages.success(request, 'Issue successfully created!')
        return redirect("dashboard")

    context = {
        'project':project,
    }
    return render(request, 'projects/create-issue.html', context)

def create_feedback(request, team_id):
    if request.POST:
        team_id = request.POST['team']
        title = request.POST['title']
        message = request.POST['message']
        team = Team.objects.get(id=team_id)
        feedback = Feedback.objects.create(team=team, title=title, message=message)
        feedback.save()
        messages.success(request, 'Feedback successfully sent!')
        return redirect('dashboard')
    return render(request, 'projects/feedback.html')

def feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    context = {
        'feedback':feedback,
    }
    return render(request, 'projects/feedback.html', context)

def issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    context = {
        'issue':issue,
    }
    return render(request, 'projects/issue.html', context)
    
def search(request):
    query = request.GET['query']
    user = request.user
    if not user.userprofile.is_line_manager:
        team = user.userprofile.team
        team = Team.objects.filter(name__iexact=team)[0]
        project = Project.objects.filter(team=team)
        project = project.filter(title__icontains=query)|project.filter(description__icontains=query)
    else:
        project = Project.objects.filter(title__icontains=query)|Project.objects.filter(description__icontains=query)
    template = 'projects/results.html'
    context =  {'query': query, 'projects':project}
    return render(request, template, context)
