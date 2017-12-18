from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import User
import re
import bcrypt
from django.contrib import messages

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    if "errors" not in request.session:
        request.session['errors'] = []
    context = {
        "errors": request.session['errors']
    }
    return render(request, "logreg_app/index.html", context)

def register(request):
    errors = User.objects.validate_registration(request.POST)
    if type(errors) == list:
        request.session['errors'] = errors
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    user = User.objects.get(email=request.POST["email"])
    request.session['id'] = user.id
    return redirect('/success')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if type(errors) == list:
        request.session['errors'] = errors
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    user = User.objects.get(email=request.POST["login_email"])
    request.session['id'] = user.id
    return redirect('/success')

def success(request):
    request.session['errors'] = []
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'logreg_app/success.html', context)