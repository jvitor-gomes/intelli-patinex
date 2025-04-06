from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .forms import SpreadsheetUploadForm, FileUploadForm
from .models import Spreadsheet, Sheet
import pandas as pd
import json
from datetime import datetime
import csv
import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def get_recent_spreadsheets(user):
    return Spreadsheet.objects.filter(user=user, processed=True).order_by('-uploaded_at')[:5]

@login_required
def upload_spreadsheet(request):
    recent_spreadsheets = get_recent_spreadsheets(request.user)
    if request.method == 'POST':
        form = SpreadsheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES['file']
                spreadsheet = Spreadsheet.objects.create(
                    user=request.user,
                    name=form.cleaned_data.get('name') or 'Planilha sem nome',
                    original_filename=file.name
                )
                
                process_spreadsheet(spreadsheet, file)
                messages.success(request, 'Planilha carregada com sucesso!')
                return redirect('sheet_list', spreadsheet_id=spreadsheet.id)
            except Exception as e:
                if spreadsheet:
                    spreadsheet.delete()
                messages.error(request, f'Erro ao processar a planilha: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SpreadsheetUploadForm()
    
    return render(request, 'sheets_app/upload.html', {
        'form': form,
        'recent_spreadsheets': recent_spreadsheets
    })

def process_spreadsheet(spreadsheet, file):
    file_ext = file.name.split('.')[-1].lower()
    
    if file_ext == 'csv':
        try:
            df = pd.read_csv(file, sep=';', encoding='utf-8')
            
            if len(df.columns) == 1 and all(col.startswith('Unnamed: ') for col in df.columns):
                file.seek(0)
                df = pd.read_csv(file, sep=';', encoding='utf-8', header=None)
                df.columns = [f'Coluna {i+1}' for i in range(len(df.columns))]
        except:
            file.seek(0)
            df = pd.read_csv(file, encoding='utf-8')
            
            if len(df.columns) == 1 and all(col.startswith('Unnamed: ') for col in df.columns):
                file.seek(0)
                df = pd.read_csv(file, encoding='utf-8', header=None)
                df.columns = [f'Coluna {i+1}' for i in range(len(df.columns))]
        
        sheet_data = {'Sheet1': df}
    else:
        excel_file = pd.ExcelFile(file)
        sheet_data = {name: pd.read_excel(excel_file, sheet_name=name) 
                     for name in excel_file.sheet_names}
    
    for sheet_name, df in sheet_data.items():
        for col in df.select_dtypes(include=['datetime64[ns]']).columns:
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        df = df.fillna('')
        
        data = {
            'columns': df.columns.tolist(),
            'data': df.to_dict('records')
        }
        
        Sheet.objects.create(
            spreadsheet=spreadsheet,
            name=sheet_name,
            data=data
        )
    
    spreadsheet.processed = True
    spreadsheet.save()

@login_required
def sheet_list(request, spreadsheet_id):
    spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
    
    if spreadsheet.user != request.user:
        raise PermissionDenied
    
    sheets = spreadsheet.sheets.all()
    context = {
        'spreadsheet': spreadsheet,
        'sheets': sheets,
        'recent_spreadsheets': get_recent_spreadsheets(request.user),
        'current_spreadsheet': spreadsheet
    }
    return render(request, 'sheets_app/sheet_list.html', context)

@login_required
def view_sheet(request, spreadsheet_id, sheet_name):
    spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
    
    if spreadsheet.user != request.user:
        raise PermissionDenied
    
    sheet = get_object_or_404(Sheet, spreadsheet=spreadsheet, name=sheet_name)
    context = {
        'sheet': sheet,
        'recent_spreadsheets': get_recent_spreadsheets(request.user),
        'current_spreadsheet': spreadsheet
    }
    return render(request, 'sheets_app/view_sheet.html', context)

def save_sheet(request, spreadsheet_id, sheet_name):
    if request.method == 'POST':
        spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
        sheet = get_object_or_404(Sheet, spreadsheet=spreadsheet, name=sheet_name)
        
        form_data = request.POST
        rows_data = []
        columns = sheet.data['columns']
        
        i = 0
        while f'data[{i}][{columns[0]}]' in form_data:
            row = {}
            for column in columns:
                row[column] = form_data.get(f'data[{i}][{column}]', '')
            rows_data.append(row)
            i += 1
        
        sheet.data['data'] = rows_data
        sheet.save()
        
        messages.success(request, 'Alterações salvas com sucesso!')
        return redirect('view_sheet', spreadsheet_id=spreadsheet_id, sheet_name=sheet_name)
    
    return redirect('view_sheet', spreadsheet_id=spreadsheet_id, sheet_name=sheet_name)

def export_csv(request, spreadsheet_id, sheet_name):
    spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
    sheet = get_object_or_404(Sheet, spreadsheet=spreadsheet, name=sheet_name)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{sheet_name}.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow(sheet.data['columns'])
    
    for row in sheet.data['data']:
        writer.writerow([row.get(column, '') for column in sheet.data['columns']])
    
    return response

@login_required
def delete_spreadsheet(request, spreadsheet_id):
    spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
    
    if spreadsheet.user != request.user:
        raise PermissionDenied
    
    spreadsheet.delete()
    messages.success(request, 'Planilha excluída com sucesso!')
    return redirect('upload_spreadsheet')

@login_required
def home(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            try:
                df = pd.read_excel(file)
                request.session['columns'] = df.columns.tolist()
                messages.success(request, 'Arquivo carregado com sucesso!')
                return redirect('select_columns')
            except Exception as e:
                messages.error(request, f'Erro ao processar o arquivo: {str(e)}')
        else:
            messages.error(request, 'Por favor, selecione um arquivo válido.')
    else:
        form = FileUploadForm()
    
    return render(request, 'sheets_app/home.html', {'form': form})

@login_required
def select_columns(request):
    columns = request.session.get('columns', [])
    if not columns:
        messages.error(request, 'Por favor, faça o upload de um arquivo primeiro.')
        return redirect('home')
    
    return render(request, 'sheets_app/select_columns.html', {'columns': columns})

@login_required
def view_spreadsheet(request, spreadsheet_id):
    spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
    sheets = Sheet.objects.filter(spreadsheet=spreadsheet)
    return render(request, 'sheets_app/view.html', {
        'spreadsheet': spreadsheet,
        'sheets': sheets
    })

@login_required
def download_sheet(request, sheet_id):
    sheet = get_object_or_404(Sheet, id=sheet_id)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{sheet.name}.csv"'
    
    writer = csv.writer(response)
    df = pd.read_excel(sheet.file.path)
    writer.writerow(df.columns)
    for index, row in df.iterrows():
        writer.writerow(row)
    
    return response
