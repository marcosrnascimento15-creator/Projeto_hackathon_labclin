from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Pacientes
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('pacientes/novo/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('pacientes/alterar/<int:id_paciente>/', views.alterar_paciente, name='alterar_paciente'),
    path('pacientes/deletar/<int:id_paciente>/', views.deletar_paciente, name='deletar_paciente'),

    # Exames
    path('exames/', views.listar_exames, name='listar_exames'),
    path('exames/novo/', views.cadastrar_exame, name='cadastrar_exame'),
    path('exames/alterar/<int:id_exame>/', views.alterar_exame, name='alterar_exame'),
    path('exames/deletar/<int:id_exame>/', views.deletar_exame, name='deletar_exame'),

    # Solicitações
    path('solicitacoes/', views.listar_solicitacoes, name='listar_solicitacoes'),
    path('solicitacoes/novo/', views.cadastrar_solicitacao, name='cadastrar_solicitacao'),
    path('solicitacoes/alterar/<int:id_solicitacao>/', views.alterar_solicitacao, name='alterar_solicitacao'),
    path('solicitacoes/deletar/<int:id_solicitacao>/', views.deletar_solicitacao, name='deletar_solicitacao'),
]
