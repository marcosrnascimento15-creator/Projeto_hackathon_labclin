from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ExameForm, PacienteForm, SolicitacaoForm
from .models import Exame, Paciente, Solicitacao


# ---------------------------------------------------------------- HOME
@login_required
def home(request):
    contexto = {
        'total_pacientes': Paciente.objects.count(),
        'total_exames': Exame.objects.count(),
        'pendentes': Solicitacao.objects.filter(status='PENDENTE').count(),
        'em_analise': Solicitacao.objects.filter(status='ANALISE').count(),
        'concluidas': Solicitacao.objects.filter(status='CONCLUIDO').count(),
        'recentes': Solicitacao.objects.select_related('paciente', 'exame')[:5],
    }
    return render(request, 'home.html', contexto)


# ------------------------------------------------------------ PACIENTES
@login_required
def listar_pacientes(request):
    query = request.GET.get('buscar', '').strip()
    pacientes = Paciente.objects.all()
    if query:
        pacientes = pacientes.filter(Q(nome__icontains=query) | Q(cpf__icontains=query))
    return render(request, 'pacientes/listar.html', {'pacientes': pacientes, 'query': query})


@login_required
def cadastrar_paciente(request):
    form = PacienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Paciente cadastrado com sucesso.')
        return redirect('listar_pacientes')
    return render(request, 'form_pagina.html', {'form': form, 'titulo': 'Novo paciente', 'voltar': 'listar_pacientes'})


@login_required
def alterar_paciente(request, id_paciente):
    paciente = get_object_or_404(Paciente, pk=id_paciente)
    form = PacienteForm(request.POST or None, instance=paciente)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Paciente atualizado com sucesso.')
        return redirect('listar_pacientes')
    return render(request, 'form_pagina.html', {'form': form, 'titulo': 'Alterar paciente', 'voltar': 'listar_pacientes'})


@login_required
@require_POST
def deletar_paciente(request, id_paciente):
    paciente = get_object_or_404(Paciente, pk=id_paciente)
    try:
        paciente.delete()
        messages.success(request, 'Paciente excluído.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o paciente possui solicitações de exames.')
    return redirect('listar_pacientes')


# --------------------------------------------------------------- EXAMES
@login_required
def listar_exames(request):
    query = request.GET.get('buscar', '').strip()
    exames = Exame.objects.all()
    if query:
        exames = exames.filter(Q(nome__icontains=query) | Q(codigo__icontains=query))
    return render(request, 'exames/listar.html', {'exames': exames, 'query': query})


@login_required
def cadastrar_exame(request):
    form = ExameForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Exame cadastrado com sucesso.')
        return redirect('listar_exames')
    return render(request, 'form_pagina.html', {'form': form, 'titulo': 'Novo exame', 'voltar': 'listar_exames'})


@login_required
def alterar_exame(request, id_exame):
    exame = get_object_or_404(Exame, pk=id_exame)
    form = ExameForm(request.POST or None, instance=exame)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Exame atualizado com sucesso.')
        return redirect('listar_exames')
    return render(request, 'form_pagina.html', {'form': form, 'titulo': 'Alterar exame', 'voltar': 'listar_exames'})


@login_required
@require_POST
def deletar_exame(request, id_exame):
    exame = get_object_or_404(Exame, pk=id_exame)
    try:
        exame.delete()
        messages.success(request, 'Exame excluído.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o exame possui solicitações.')
    return redirect('listar_exames')


# ---------------------------------------------------------- SOLICITAÇÕES
@login_required
def listar_solicitacoes(request):
    query = request.GET.get('buscar', '').strip()
    status = request.GET.get('status', '')
    solicitacoes = Solicitacao.objects.select_related('paciente', 'exame')
    if query:
        solicitacoes = solicitacoes.filter(
            Q(paciente__nome__icontains=query) | Q(exame__nome__icontains=query))
    if status:
        solicitacoes = solicitacoes.filter(status=status)
    return render(request, 'solicitacoes/listar.html', {
        'solicitacoes': solicitacoes,
        'query': query,
        'status': status,
        'status_choices': Solicitacao.STATUS_CHOICES,
    })


@login_required
def cadastrar_solicitacao(request):
    form = SolicitacaoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Solicitação registrada com sucesso.')
        return redirect('listar_solicitacoes')
    return render(request, 'form_pagina.html', {'form': form, 'titulo': 'Nova solicitação de exame', 'voltar': 'listar_solicitacoes'})


@login_required
def alterar_solicitacao(request, id_solicitacao):
    solicitacao = get_object_or_404(Solicitacao, pk=id_solicitacao)
    form = SolicitacaoForm(request.POST or None, instance=solicitacao)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Solicitação atualizada com sucesso.')
        return redirect('listar_solicitacoes')
    return render(request, 'form_pagina.html', {'form': form, 'titulo': 'Alterar solicitação', 'voltar': 'listar_solicitacoes'})


@login_required
@require_POST
def deletar_solicitacao(request, id_solicitacao):
    get_object_or_404(Solicitacao, pk=id_solicitacao).delete()
    messages.success(request, 'Solicitação excluída.')
    return redirect('listar_solicitacoes')
