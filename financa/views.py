from django.shortcuts import render, redirect, get_object_or_404
from .models import Transacao
from .forms import TransacaoForm
from django.db.models import Sum

# Create your views here.

def financas(request):
    descricao_filtro = request.GET.get('descricao', '')
    tipo_filtro = request.GET.get('tipo', '')
    transacoes = Transacao.objects.all()

    if descricao_filtro:
        transacoes = transacoes.filter(descricao__icontains=descricao_filtro)
    if tipo_filtro:
        transacoes = transacoes.filter(tipo=tipo_filtro)
    
    receitas = Transacao.objects.filter(tipo='R').aggregate(Sum('valor'))['valor__sum'] or 0
    despesas = Transacao.objects.filter(tipo='D').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = receitas - despesas
    return render(request, 'financas.html', {'transacoes': transacoes, 'saldo': saldo})

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
    
