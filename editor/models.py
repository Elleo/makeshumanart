from django.db import models
import os, os.path
import shutil
import pathlib
import subprocess


class Site(models.Model):
    title = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)
    domain = models.CharField(default='makeshuman.art', max_length=255, choices=[
                ('makeshuman.art', 'makeshuman.art'),
                ('writingstudio.org', 'writingstudio.org')
            ])
    theme = models.CharField(default='hugo-paper', max_length=255, choices=[
        ('hugo-paper', 'Paper')
        ])

    def __str__(self):
        return self.title

    def generate(self):
        moduledir = pathlib.Path(__file__).parent.resolve()
        themedir = os.path.join(moduledir, 'themes')
        wd = os.getcwd()
        os.chdir('sites')
        hugodir = '%s.%s' % (self.subdomain, self.domain)
        if os.path.exists(hugodir):
            shutil.rmtree(hugodir)
        subprocess.run(['hugo', 'new', 'site', hugodir])
        toml = """
baseURL = 'https://%s.%s/'
languageCode = 'en-us'
title = "%s"
theme = '%s'""" % (self.subdomain, self.domain, self.title, self.theme)
        with open(os.path.join(hugodir, "hugo.toml"), 'w') as f:
            f.write(toml)
        for page in Page.objects.filter(site=self):
            output = """+++
title = "%s"
draft = false
+++\n""" % page.title
            sections = list(TextSection.objects.filter(page=page)) + list(ImageSection.objects.filter(page=page))
            for section in sorted(sections, key=lambda section: section.position):
                output += section.text

            with open(os.path.join(hugodir, "content", "_index.md"), 'w') as f:
                f.write(output.replace("\r\n", "\n"))
        shutil.copytree(os.path.join(themedir, self.theme), os.path.join(hugodir, 'themes', self.theme))
        os.chdir(hugodir)
        subprocess.run(['hugo'])
        os.chdir(wd)


class Page(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_date = models.DateTimeField("Date created", auto_now_add=True, editable=False)
    modified_date = models.DateTimeField("Date modified", auto_now=True)
    index = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TextSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.text


class ImageSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    caption = models.TextField(null=True, blank=True)
    alt_text = models.TextField(null=True, blank=True)
    image = models.ImageField()

    def __str__(self):
        if self.caption:
            return self.caption
        elif self.alt_text:
            return self.alt_text
        else:
            return "Image"
