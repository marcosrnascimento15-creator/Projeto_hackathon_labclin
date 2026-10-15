from django.db import models


class Paciente(models.Model):
    SEXO_CHOICES = [('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outro')]

    id_paciente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Exame(models.Model):
    MATERIAL_CHOICES = [
        ('SANGUE', 'Sangue'),
        ('URINA', 'Urina'),
        ('FEZES', 'Fezes'),
        ('SALIVA', 'Saliva'),
        ('OUTRO', 'Outro'),
    ]

    id_exame = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=120)
    material = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    prazo_dias = models.PositiveIntegerField(default=1, help_text='Prazo de entrega do resultado (dias)')
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Solicitacao(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ANALISE', 'Em análise'),
        ('CONCLUIDO', 'Concluído'),
    ]

    id_solicitacao = models.AutoField(primary_key=True)
    # PROTECT: impede apagar paciente/exame que já tenham solicitações
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='solicitacoes')
    exame = models.ForeignKey(Exame, on_delete=models.PROTECT, related_name='solicitacoes')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    resultado = models.TextField(blank=True)
    observacao = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-data_solicitacao']
        verbose_name = 'solicitação'
        verbose_name_plural = 'solicitações'

    def __str__(self):
        return f'#{self.id_solicitacao} - {self.paciente} / {self.exame.nome}'
