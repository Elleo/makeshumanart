from django.db import models
import os, os.path
import shutil
import pathlib
import subprocess

from .models import *
from .file_templates import *

def generate(self):
    moduledir = pathlib.Path(__file__).parent.resolve()
    themedir = os.path.join(moduledir, 'themes')
    wd = os.getcwd()
    os.chdir('/var/www/sites')
    hugodir = '%s.%s' % (self.subdomain, self.domain)
    if os.path.exists(hugodir):
        shutil.rmtree(hugodir)
    subprocess.run(['hugo', 'new', 'site', hugodir])
    toml = toml_template % (self.subdomain, self.domain, self.title, self.theme)
    with open(os.path.join(hugodir, "hugo.toml"), 'w') as f:
        f.write(toml)
    for page in Page.objects.filter(site=self):
        output = page_template % page.title
        sections = list(TextSection.objects.filter(page=page)) + list(ImageSection.objects.filter(page=page))
        for section in sorted(sections, key=lambda section: section.position):
            output += section.text + "\n\n"
        print(page.index)
        if page.index:
            filename = "_index.md"
        else:
            filename = page.title + ".md"
        filename = filename.replace(" ", "_")
        with open(os.path.join(hugodir, "content", filename), 'w') as f:
            f.write(output.replace("\r\n", "\n"))
    shutil.copytree(os.path.join(themedir, self.theme), os.path.join(hugodir, 'themes', self.theme))
    default_dir = os.path.join(hugodir, 'themes', self.theme, 'layouts', '_default')
    shutil.copy(os.path.join(default_dir, "single.html"), os.path.join(default_dir, "index.html"))
    os.chdir(hugodir)
    subprocess.run(['hugo'])
    os.chdir(wd)
