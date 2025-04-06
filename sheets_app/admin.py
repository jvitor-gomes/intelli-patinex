from django.contrib import admin
from .models import Spreadsheet, Sheet

@admin.register(Spreadsheet)
class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'original_filename', 'user', 'uploaded_at', 'processed')
    list_filter = ('processed', 'uploaded_at', 'user')
    search_fields = ('name', 'original_filename', 'user__username')

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'spreadsheet')
    list_filter = ('spreadsheet', 'spreadsheet__user')
    search_fields = ('name', 'spreadsheet__name', 'spreadsheet__user__username')
