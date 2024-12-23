from django.db import models

# Create your models here.

STATUS_CHOICES = [('pendente', 'Pendente'),
                  ('concluida', 'Concluída'),
                  ('em_andamento', 'Em Andamento'),
                  ('atrasado', 'Atrasado')]

STATUS_PRIORITY = [('alta', 'Alta'),
                   ('média', 'Média'),
                   ('baixa', 'Baixa')]


class ToDoList(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    status = models.CharField(choices=STATUS_CHOICES, null=False, blank=False, max_length=20)
    priority = models.CharField(choices=STATUS_PRIORITY, null=False, blank=False, max_length=15)
    due_date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
