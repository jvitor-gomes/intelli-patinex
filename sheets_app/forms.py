from django import forms
from .models import Spreadsheet

class SpreadsheetUploadForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        help_text='Nome opcional para identificar a planilha. Se não fornecido, será usado o nome do arquivo.'
    )
    file = forms.FileField(
        label='Selecione um arquivo',
        help_text='Formatos suportados: .xlsx, .xls, .csv'
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['xlsx', 'xls', 'csv']:
                raise forms.ValidationError('Formato de arquivo não suportado. Use .xlsx, .xls ou .csv')
            if file.size > 5242880:  # 5MB
                raise forms.ValidationError('O arquivo é muito grande. O tamanho máximo é 5MB.')
        return file 

class FileUploadForm(forms.Form):
    file = forms.FileField(
        label='Selecione um arquivo',
        help_text='Formatos suportados: .xlsx, .xls, .csv'
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['xlsx', 'xls', 'csv']:
                raise forms.ValidationError('Formato de arquivo não suportado. Use .xlsx, .xls ou .csv')
            if file.size > 5242880:  # 5MB
                raise forms.ValidationError('O arquivo é muito grande. O tamanho máximo é 5MB.')
        return file 