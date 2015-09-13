from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext, loader, Context, Template
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse 
from django.contrib.auth import authenticate, login, logout
from django.http import *

# Create your views here.
def home(request):
	return render(request,'homepage.html')


def register_user(request):
	username = password = email =''
	if request.POST:
		user_form = UserCreateForm(request.POST)
		if user_form.is_valid():
			usuario = User(username=request.POST['username'], email=request.POST['email'])
			usuario.set_password(request.POST['password1'])
			usuario.save()
			return HttpResponseRedirect(reverse('register_user'))
	else:
		user_form = UserCreateForm()

	dictionary = {
		'user_form': user_form,
		'page_title': 'Aplicacion - Register',
		'body_class': 'register',
	}
	return render(request,"register.html", dictionary)