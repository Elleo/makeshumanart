from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *
from .generate import generate

@login_required
def index(request):
    template = loader.get_template('editor.html')
    context = {'logged_in': True}
    return HttpResponse(template.render(context, request))

@login_required
def edit_page(request, page_id):
    template = loader.get_template('edit_page.html')
    page = Page.objects.get(pk=page_id)
    section = TextSection.objects.filter(page=page_id)[0]
    if 'section_text' in request.POST:
        section.text = request.POST['section_text']
        section.save()
        generate(page.site)
    context = {'page': page, 'section': section, 'logged_in': True}
    return HttpResponse(template.render(context, request))
