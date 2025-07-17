from django.contrib.auth.models import User
from django.db import models
import os, os.path
import subprocess
import pathlib
import shutil


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Page(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_date = models.DateTimeField("Date created", auto_now_add=True, editable=False)
    modified_date = models.DateTimeField("Date modified", auto_now=True)
    index = models.BooleanField(default=False)
    include_in_menu = models.BooleanField(default=True)
    menu_position = models.IntegerField(default=0)

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
