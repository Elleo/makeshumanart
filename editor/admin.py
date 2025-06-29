from django.contrib import admin


from .models import *

admin.site.register(Site)
admin.site.register(Page)
admin.site.register(TextSection)
admin.site.register(ImageSection)
