from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri
from django.contrib.auth import authenticate, login, logout

def index(request):
    template = loader.get_template('index.html')
    context = {'logged_in': request.user.is_authenticated}
    return HttpResponse(template.render(context, request))

def donate(request):
    template = loader.get_template('donate.html')
    context = {'logged_in': request.user.is_authenticated}
    return HttpResponse(template.render(context, request))

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    template = loader.get_template('login.html')
    context = {'logged_in': request.user.is_authenticated}
    if 'username' in request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET and url_has_allowed_host_and_scheme(request.GET['next'], None):
                return redirect(iri_to_uri(request.GET['next']))
            return redirect("/")
        else:
            context['messages']=['Invalid username or password']
    return HttpResponse(template.render(context, request))

def logout_view(request):
    logout(request)
    return redirect("/")
