from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext, loader, Context, Template
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import *


# Create your views here.
def home(request):
    return render(request, 'homepage.html')

