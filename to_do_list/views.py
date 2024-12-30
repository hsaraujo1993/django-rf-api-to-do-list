from datetime import date
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from to_do_list.serializer import ToDoListSerializer
from to_do_list.models import ToDoList


# Create your views here.

class TodoListListCreateAPIView(generics.ListCreateAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority']


class TodoDoListActiveAPIView(generics.ListAPIView):
    serializer_class = ToDoListSerializer

    def get_queryset(self):
        ToDoList.objects.filter(
            Q(due_date__lt=date.today()) &
            Q(status__in=['pendente', 'em_andamento'])
        ).update(status='atrasada')

        # Retorna o queryset filtrado
        return ToDoList.objects.filter(status__in=['em_andamento', 'pendente', 'atrasada'])


class ToDoListStatusCompletedCancelled(generics.ListAPIView):
    serializer_class = ToDoListSerializer

    def get_queryset(self):
        return ToDoList.objects.filter(status__in=['concluida', 'cancelada'])


class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer

    def perform_destroy(self, instance):
        if instance.status not in ["pendente", "cancelada"]:
            raise ValidationError({'message':
                                       f'O status {instance.status} não permite exclusão. Permitidos: pendente ou cancelada.'})

        instance.delete()
