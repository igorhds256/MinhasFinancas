from .models import Transacao
from django import forms

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data', 'tipo']
        widgets = {
            'data': forms.DateInput(
                format='%Y-%m-%d', 
                attrs={'type': 'date'}
            ),
        }
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor (R$)',
            'data': 'Data da Transação',
            'tipo': 'Tipo de Transação',
        }


    def __init__(self, *args, **kwargs):
        super(TransacaoForm, self).__init__(*args, **kwargs)
        # Garante que o Django interprete o formato corretamente ao carregar
        self.fields['data'].format = '%Y-%m-%d'