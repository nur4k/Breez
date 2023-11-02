from django.contrib import admin

from mainapp.models import Client, CSVFile

admin.site.register((Client, CSVFile))
