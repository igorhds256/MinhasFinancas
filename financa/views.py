from django.shortcuts import render, redirect, get_object_or_404
from .models import Transacao
from .forms import TransacaoForm
from django.db.models import Sum, FloatField, Case, When, F
from django.db.models.functions import TruncMonth
from datetime import datetime


# Create your views here.

def financas(request):
    ano_atual = datetime.now().year
    anos = range(ano_atual - 5, ano_atual + 5)

    descricao_filtro = request.GET.get('descricao', '')
    tipo_filtro = request.GET.get('tipo', '')
    mes_filtro = request.GET.get('mes', '')
    ano_filtro = request.GET.get('ano', '')
    transacoes = Transacao.objects.all()

    if descricao_filtro:
        transacoes = transacoes.filter(descricao__icontains=descricao_filtro)
    if tipo_filtro:
        transacoes = transacoes.filter(tipo=tipo_filtro)
    if mes_filtro:
        transacoes = transacoes.filter(data__month=mes_filtro)
    if ano_filtro:
        transacoes = transacoes.filter(data__year=ano_filtro)
    
    receitas = transacoes.filter(tipo='R').aggregate(Sum('valor'))['valor__sum'] or 0
    despesas = transacoes.filter(tipo='D').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = receitas - despesas
    return render(request, 'financas.html', {'transacoes': transacoes, 'saldo': saldo, 'anos': anos})

def adicionar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('financas')
    else:
        form = TransacaoForm()
    return render(request, 'adicionar_transacao.html', {'form': form})

def detalhes_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, id=transacao_id)
    return render(request, 'detalhes_transacao.html', {'transacao': transacao})

def editar_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, id=transacao_id)
    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao)
        if form.is_valid():
            form.save()
            return redirect('financas')
    else:
        form = TransacaoForm(instance=transacao)
    return render(request, 'editar_transacao.html', {'form': form})

def deletar_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, id=transacao_id)
    if request.method == 'POST':
        transacao.delete()
        return redirect('financas')
    return render(request, 'deletar_transacao.html', {'transacao': transacao})  
    
def dashboard(request):
    # Cálculos para os cards de resumo
    total_receitas = Transacao.objects.filter(tipo='R').aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = Transacao.objects.filter(tipo='D').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_receitas - total_despesas

    # Dados para o gráfico (Agrupado por mês)
    evolucao_saldo = (
        Transacao.objects.annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(
            saldo_mes=Sum(
                Case(
                    When(tipo='R', then=F('valor')),
                    When(tipo='D', then=-F('valor')),
                    default=0,
                    output_field=FloatField(),
                )
            )
        )
        .order_by('mes')
    )

    dados_por_mes = ( 
        Transacao.objects.annotate(mes=TruncMonth('data')) 
        .values('mes', 'tipo') 
        .annotate(total=Sum('valor')) 
        .order_by('mes') )

    context = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'transacoes': Transacao.objects.all()[:10], # Últimas 10
    }
    return render(request, 'dashboard.html', {**context, 'evolucao_saldo': evolucao_saldo, 'dados_por_mes': dados_por_mes})