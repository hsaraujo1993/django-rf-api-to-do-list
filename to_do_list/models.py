from django.db import models
from rest_framework.exceptions import ValidationError

# Create your models here.

# Opções de status
STATUS_CHOICES = [('pendente', 'Pendente'),
                  ('concluida', 'Concluída'),
                  ('em_andamento', 'Em Andamento'),
                  ('atrasada', 'Atrasada'),
                  ('cancelada', 'Cancelada')]

# opções de priority
PRIORITY_CHOICES = [('alta', 'Alta'),
                   ('media', 'Média'),
                   ('baixa', 'Baixa')]


# Model da aplicação
class ToDoList(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pendente', null=False, blank=False, max_length=20)
    priority = models.CharField(choices=PRIORITY_CHOICES, null=False, blank=False, max_length=15)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metodo que retorna o valor title ao executar a instancia do modelo ToDoList.
    def __str__(self):
        return self.title

    # função para validação de status em uma nova instância (cadastro de tarefa)
    def clean(self):

        # se instancia não tiver uma chave pk e status da instância for diferente de pendente, exibirá erro.
        if not self.pk and self.status != 'pendente':
            raise ValidationError({"message": "O status deve iniciar como 'pendente'."})

    # metodo save salva a instância no banco de dados
    def save(self, *args, **kwargs):

        self.full_clean()
        super().save(*args, **kwargs)
