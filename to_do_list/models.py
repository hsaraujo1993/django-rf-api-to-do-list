from django.db import models
from rest_framework.exceptions import ValidationError

# Create your models here.

STATUS_CHOICES = [('pendente', 'Pendente'),
                  ('concluida', 'Concluída'),
                  ('em_andamento', 'Em Andamento'),
                  ('atrasada', 'Atrasada'),
                  ('cancelada', 'Cancelada')]

STATUS_PRIORITY = [('alta', 'Alta'),
                   ('media', 'Média'),
                   ('baixa', 'Baixa')]


class ToDoList(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pendente', null=False, blank=False, max_length=20)
    priority = models.CharField(choices=STATUS_PRIORITY, null=False, blank=False, max_length=15)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):

        if not self.pk and self.status != 'pendente':
            raise ValidationError({"message": "O status deve iniciar como 'pendente'."})

    def save(self, *args, **kwargs):

        self.full_clean()
        super().save(*args, **kwargs)
