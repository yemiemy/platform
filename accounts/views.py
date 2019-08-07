from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Team
from django.contrib.auth.models import User
from django.contrib import messages, auth
from projects.models import Project, Issue, Feedback

#YEMI
import re 
from django.shortcuts import render, redirect, Http404
from .forms import UserRegisterForm, UserUpdateForm #ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from accounts.models import EmailConfirmed, UserProfile
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#Create your views here.
def login(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
        
    else:
        return render(request, 'accounts/login.html')

@login_required
def dashboard(request):
    user = request.user
    try:
        if user.userprofile:
            

            user_team = user.userprofile.team
            all_teams = Team.objects.all()
            all_issues = Issue.objects.all().order_by("-post_date")
            all_projects = Project.objects.all()[:5]
            projects = Project.objects.all()

            team_feedbacks = Feedback.objects.filter(team=user_team).order_by('-post_date')


            team_projects = Project.objects.filter(team=user_team)
            # user_team = Team.objects.get(members=user)
            # print(user_team)
            completed_projects = Project.objects.filter(is_accepted=True)

            

            projects_counter = 0
            for project in projects:
                projects_counter+=1

            completed_counter = 0
            for project in completed_projects:
                completed_counter+=1

            if not projects_counter == 0:
                completed_percent = int((completed_counter/projects_counter)*100)
                ongoing_percent = int(100 - completed_percent)
            else:
                completed_percent = 0
                ongoing_percent = 0

            ongoing_counter = projects_counter - completed_counter
            
            
            team_completed_projects = team_projects.filter(is_accepted=True)

            team_projects_counter = 0
            for project in team_projects:
                team_projects_counter+=1

            team_completed_counter = 0
            for project in team_completed_projects:
                team_completed_counter+=1

            if not team_projects_counter == 0:
                team_completed_percent = int((team_completed_counter/team_projects_counter)*100)
                team_ongoing_percent = int(100 - team_completed_percent)
            else:
                team_completed_percent = 0
                team_ongoing_percent = 0

            team_ongoing_counter = team_projects_counter - team_completed_counter

            issues = Issue.objects.all().order_by('-post_date')


            context = {   
                'all_teams':all_teams, 'all_projects':all_projects,
                'all_issues': all_issues,
                'completed_percent': completed_percent,
                'ongoing_percent': ongoing_percent,
                'completed_counter': completed_counter,
                'ongoing_counter': ongoing_counter,
                'team_completed_percent': team_completed_percent,
                'team_ongoing_percent': team_ongoing_percent,
                'team_completed_counter': team_completed_counter,
                'team_ongoing_counter': team_ongoing_counter,
                'user_team': user_team,
                'team_projects': team_projects,
                'issues':issues,
                'team_feedbacks':team_feedbacks,
             }
            return render(request, 'accounts/dashboard.html', context)
        else:
            return redirect('no_team')
    except:
        return redirect('no_team')

def no_team(request):
    return render(request, 'accounts/no-team.html')

def create_team(request):
    users = User.objects.all()
    if request.POST:
        name = request.POST['name']

        if "members" in request.POST:
            members = request.POST.getlist('members')
        else:
            messages.error(request, 'Please select team members')
            return redirect('create_team')

        if "manager" in request.POST:
            program_manager = request.POST['manager']
        else:
            messages.error(request, 'Please select a team lead')
            return redirect('create_team')

        program_manager = User.objects.get(username=program_manager)

        team = Team.objects.create(name=name, program_manager=program_manager)


        for member in members:
            user = User.objects.get(username=member)
            team.members.add(user)
            profile = user.userprofile
            profile.team = team
            profile.save()


        user = User.objects.get(username=program_manager)

        if user in team.members.all():
            user.userprofile.is_program_manager = True
            user.save()
            team.save()
        else:
            messages.error(request, 'Please select a team lead from the members you selected')
            return redirect('create_team')
        
        messages.success(request, 'Team successfully created!')
        return redirect("dashboard")

    context = {'users':users,}
    return render(request, 'accounts/create-team.html', context)

def manage_teams(request):
    teams = Team.objects.all()
    context ={
        'teams':teams
    }
    return render(request, 'accounts/manage-teams.html', context)

def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.POST:
        team.delete()
        messages.success(request, 'Team successfully deleted!')
        return redirect('dashboard')

    context = {
        'team': team,
    }
    return render(request, 'accounts/delete-team.html', context)

def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    projects = Project.objects.filter(team=team)
    completed_projects = projects.filter(is_accepted=True)

    teams = Team.objects.all().order_by('-totalPoints')
    length = len(teams)
    n = range(1, length+1)

    dictionary = {}
    position = []

    for x in n:
        position.append(x)

    for key,val in zip(position,teams):
        dictionary[key] = val

    for key, val in dictionary.items():
        the_team = Team.objects.get(id=val.id)
        the_team.position = key
        the_team.save()

    projects_counter = 0
    for project in projects:
        projects_counter+=1

    completed_counter = 0
    for project in completed_projects:
        completed_counter+=1

    # projects = len(projects)
    # completed_projects = len(projects)

    if not projects_counter == 0:
        completed_percent = int((completed_counter/projects_counter)*100)
        ongoing_percent = int(100 - completed_percent)
    else:
        completed_percent = 0
        ongoing_percent = 0

    ongoing_counter = projects_counter - completed_counter

    context = {
        "team":team,
        "projects":projects,
        "completed_percent":completed_percent,
        "ongoing_percent":ongoing_percent,
        'completed_counter': completed_counter,
        'ongoing_counter': ongoing_counter,
    }
    return render(request, 'accounts/team.html', context)

def update_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    users = User.objects.all()

    if request.POST:
        for member in team.members.all():
            user = User.objects.get(username=member)
            team.members.remove(user)

        user = team.program_manager
        user.userprofile.is_program_manager = False
        user.save()
        
        team.name = request.POST['name']
        if "members" in request.POST:
            members = request.POST.getlist('members')
        else:
            messages.error(request, 'Please select team members')
            return redirect('update_team', team.id)
        
        if "manager" in request.POST:
            program_manager = request.POST['manager']
        else:
            messages.error(request, 'Please select a team lead')
            return redirect('update_team', team.id)

        team.program_manager = User.objects.get(username=program_manager)

        for member in members:
            user = User.objects.get(username=member)
            team.members.add(user)
            profile = user.userprofile
            profile.team = team
            profile.save()

        user = User.objects.get(username=program_manager)
        if user in team.members.all():
            user.userprofile.is_program_manager = True
            user.save()
            team.save()
        else:
            messages.error(request, 'Please select a team lead from the members you selected')
            return redirect('create_team')
        
        messages.success(request, 'Team successfully Updated!')
        return redirect('dashboard')

    context = {
        'team':team, 'users': users,
    }
    return render(request, 'accounts/update-team.html', context)

#YEMI
def register(request):
	if request.method=='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			print('VALID')
			username = form.cleaned_data.get('username')
			position = form.cleaned_data.get('position')
			user = User.objects.get(username=username)
			profile = UserProfile.objects.create(position=position, user=user)
			profile.save()
			messages.success(request, f'Account created for {username}! Check your email to confirm your email address.')
			return redirect('register')

	else:
		form = UserRegisterForm()
	return render(request, 'accounts/register.html', {'form':form})

SHA1_RE = re.compile('^[a-f0-9]{40}$')
def activation_view(request, activation_key):
	if SHA1_RE.search(activation_key):
		print ('activation key is valid')
		try:
			user_confirmed = EmailConfirmed.objects.get(activation_key=activation_key)
		except EmailConfirmed.DoesNotExist:
			user_confirmed = None
			messages.success(request, 'There was an error with your request')
			return redirect('register')
		if user_confirmed is not None and not user_confirmed.confirmed:
			message = 'Confirmation Successful!!'
			user_confirmed.confirmed = True
			#user_confirmed.activation_key = 'confirmed'
			user_confirmed.save()
			messages.success(request, 'Your account has been activated! You can now <a href={}>Login</a>'.format(reverse("login")), extra_tags='safe')
		
		elif user_confirmed is not None and user_confirmed.confirmed:
			message = 'Already confirmed'
			messages.success(request, 'Your account has already been activated! <a href={}>Login</a>'.format(reverse("login")), extra_tags='safe')
		
		
		else:
			message = ''
		context = {'message':message}
		return render(request, 'accounts/activation.html', context)
	else:
		raise Http404