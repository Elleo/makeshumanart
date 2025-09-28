from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os, os.path

from .models import *
from .generate import generate

def owns_site(view_func):
    def wrapper(request, site_id, *args, **kwargs):
        site = Site.objects.get(pk=site_id)
        if site.owner != request.user:
            template = loader.get_template('forbidden.html')
            context = {'logged_in': True}
            return HttpResponse(template.render(context, request))
        return view_func(request, site_id, *args, **kwargs)
    return wrapper

@login_required
def index(request):
    template = loader.get_template('editor.html')
    sites = Site.objects.filter(owner=request.user)
    if len(sites) == 1:
        return redirect(f"/editor/site/{sites[0].pk}/")
    elif len(sites) == 0:
        return redirect(f"/editor/create_site/")
    context = {'logged_in': True, 'sites': sites}
    return HttpResponse(template.render(context, request))

@login_required
@owns_site
def edit_site(request, site_id):
    template = loader.get_template('edit_site.html')
    site = Site.objects.get(pk=site_id)
    pages = Page.objects.filter(site=site)
    context = {
        'site': site,
        'pages': pages,
        'logged_in': True
    }
    return HttpResponse(template.render(context, request))

@login_required
@owns_site
def new_page(request, site_id):
    template = loader.get_template('add_page.html')
    site = Site.objects.get(pk=site_id)
    if 'page_title' in request.POST:
        position = len(Page.objects.filter(site=site))
        page = Page.objects.create(title=request.POST['page_title'], site=site, menu_position=position)
        TextSection.objects.create(page=page, text='')
        return redirect(f"/editor/site/{site.pk}/page/{page.pk}/")
    context = {
        'site': site,
        'logged_in': True
    }
    return HttpResponse(template.render(context, request))

@login_required
@owns_site
def edit_page(request, site_id, page_id):
    template = loader.get_template('edit_page.html')
    page = Page.objects.get(pk=page_id)
    section = TextSection.objects.filter(page=page_id)[0]
    if 'section_text' in request.POST:
        section.text = request.POST['section_text']
        section.save()
        generate(page.site)
    context = {'page': page, 'section': section, 'logged_in': True}
    return HttpResponse(template.render(context, request))

@login_required
@owns_site
def theme_picker(request, site_id):
    template = loader.get_template('theme_picker.html')
    site = Site.objects.get(pk=site_id)
    available_themes = []
    theme_path = os.path.join(os.path.dirname(__file__), 'themes')
    for item in os.listdir(theme_path):
        if os.path.isdir(os.path.join(theme_path, item)):
            available_themes.append(item)
    context = {
        'site': site,
        'available_themes': available_themes,
        'logged_in': True
    }
    if 'theme' in request.POST:
        theme = request.POST['theme']
        if theme in available_themes:
            site.theme = theme
            site.save()
            generate(site)
    return HttpResponse(template.render(context, request))
