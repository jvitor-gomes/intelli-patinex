from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_spreadsheet, name='upload_spreadsheet'),
    path('spreadsheet/<int:spreadsheet_id>/', views.sheet_list, name='sheet_list'),
    path('spreadsheet/<int:spreadsheet_id>/sheet/<str:sheet_name>/', views.view_sheet, name='view_sheet'),
    path('spreadsheet/<int:spreadsheet_id>/sheet/<str:sheet_name>/save/', views.save_sheet, name='save_sheet'),
    path('spreadsheet/<int:spreadsheet_id>/sheet/<str:sheet_name>/export/', views.export_csv, name='export_csv'),
    path('spreadsheet/<int:spreadsheet_id>/delete/', views.delete_spreadsheet, name='delete_spreadsheet'),
] 