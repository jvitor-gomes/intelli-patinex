from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False, label='Nome')
    last_name = forms.CharField(max_length=100, required=False, label='Sobrenome')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label='Biografia')
    telefone = forms.CharField(max_length=20, required=False, label='Telefone')
    endereco = forms.CharField(max_length=200, required=False, label='Endereço')
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='Data de Nascimento'
    )

    class Meta:
        model = Profile
        fields = ['bio', 'telefone', 'endereco', 'data_nascimento'] 