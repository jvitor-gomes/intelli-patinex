from django.db import models
from django.contrib.auth.models import User

class Spreadsheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spreadsheets')
    name = models.CharField(max_length=255, default='Planilha sem nome')
    original_filename = models.CharField(max_length=255, default='arquivo.xlsx')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        if not self.name or self.name == 'Planilha sem nome':
            return self.original_filename
        return self.name

    class Meta:
        ordering = ['-uploaded_at']

class Sheet(models.Model):
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, related_name='sheets')
    name = models.CharField(max_length=255)
    data = models.JSONField()
    
    def __str__(self):
        return f"{self.spreadsheet.original_filename} - {self.name}"

    class Meta:
        ordering = ['name']
