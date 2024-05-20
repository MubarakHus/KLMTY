from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import DailyWords

class DailyWordsResource(resources.ModelResource):
    class Meta:
        model = DailyWords
        # Optionally, specify fields you want to include in imports/exports
        fields = ('day', 'words')

class DailyWordsAdmin(ImportExportModelAdmin):
    resource_class = DailyWordsResource

admin.site.register(DailyWords, DailyWordsAdmin)
