from django.contrib import admin
from .models import Paciente, Exame, Solicitacao

admin.site.register(Paciente)
admin.site.register(Exame)
admin.site.register(Solicitacao)
