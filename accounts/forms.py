from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(label='', \
					widget=forms.TextInput(attrs={'placeholder': 'first name'}))
	last_name = forms.CharField(label='', \
					widget=forms.TextInput(attrs={'placeholder': 'last name'}))
	username = forms.CharField(label='', \
					widget=forms.TextInput(attrs={'placeholder': 'username'}))
	position = forms.CharField(label='', \
					widget=forms.TextInput(attrs={'placeholder': 'Role in company (e.g software dev)'}))
	email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))

	password1 = forms.CharField(label='', \
					widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(label='', \
					widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

	class Meta:
		model = User
		fields = ['first_name','last_name','username','position', 'email','password1', 'password2']


	# class Meta:
	# 	model = Role
	# 	fields = ['position']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		user_count = User.objects.filter(email=email).count()
		print(user_count)
		if user_count > 0 :
			raise forms.ValidationError('This email has already been registered')
		return email
	# def clean_role(self):
	# 	print(self.cleaned_data.get('position'))
	# 	return position


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email',]

