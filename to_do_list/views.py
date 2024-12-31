from datetime import date

import django_filters
import rest_framework.filters
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from to_do_list.serializer import ToDoListSerializer
from to_do_list.models import ToDoList


# Create your views here.

# View de configuração de filtros
class ToDoListFilter(django_filters.FilterSet):

    # Configuração de filtro range de data
    start_date = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')

    class Meta:

        # Configurando campos que podem ser filtrados
        model = ToDoList
        fields = ['status', 'priority', 'due_date', 'start_date', 'end_date']  # campos disponíveis para filtrar


# View de GET geral e POST
class TodoListListCreateAPIView(generics.ListCreateAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer  # adicionando serializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # configurações da rest_framework para filtros e ordenação
    filterset_class = ToDoListFilter  # herdando filtro da classe
    ordering_fields = ['due_date', 'status', 'priority', 'created_at']  # campos onde podemos realizar a ordenação
    ordering = ['created_at']  # campo com ordenação padrão


# View para listagem de tarefas ativas
class TodoDoListActiveAPIView(generics.ListAPIView):
    serializer_class = ToDoListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ToDoListFilter
    ordering_fields = ['due_date', 'status', 'priority', 'created_at']
    ordering = ['created_at']

    # query_set responsável por filtrar as tarefas atrasadas com status pendente e em_andamento e alterar para atrasada
    def get_queryset(self):
        ToDoList.objects.filter(
            Q(due_date__lt=date.today()) &
            Q(status__in=['pendente', 'em_andamento'])
        ).update(status='atrasada')

        # Após realizar a validaçao das tarefas atrasadas, listamos somente as tarefas com status ativo: em_andamento, pendente e atrasada
        return ToDoList.objects.filter(status__in=['em_andamento', 'pendente', 'atrasada'])


# View para listagem de tarefas com status concluida e cancelada
class ToDoListStatusCompletedCancelled(generics.ListAPIView):
    serializer_class = ToDoListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ToDoListFilter
    ordering_fields = ['due_date', 'status', 'priority', 'created_at']
    ordering = ['created_at']

    # query_set filtrando os status concluida e cancelada
    def get_queryset(self):
        return ToDoList.objects.filter(status__in=['concluida', 'cancelada'])


# View de UPDATE, PATCH E DELETE
class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer

    # Somente permitido deletar tarefas que contém status pendente e cancelada
    def perform_destroy(self, instance):
        if instance.status not in ["pendente", "cancelada"]:
            raise ValidationError({'message':
                                       f'O status {instance.status} não permite exclusão. Permitidos: pendente ou cancelada.'})
        # Caso respeitem o status, deleção é realizada
        instance.delete()
