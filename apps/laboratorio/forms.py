from django import forms
from .models import Paciente, Exame, Solicitacao


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'sexo', 'email', 'telefone']
        widgets = {
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'data_nascimento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(61) 90000-0000'}),
        }
        error_messages = {
            'cpf': {'unique': 'CPF já cadastrado.'},
        }


class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ['codigo', 'nome', 'material', 'preco', 'prazo_dias', 'descricao']
        widgets = {
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
        error_messages = {
            'codigo': {'unique': 'Código de exame já cadastrado.'},
        }


class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['paciente', 'exame', 'status', 'resultado', 'observacao']
        widgets = {
            'resultado': forms.Textarea(attrs={'rows': 4}),
        }
