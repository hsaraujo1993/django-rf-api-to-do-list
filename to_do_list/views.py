from datetime import date

import django_filters
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from to_do_list.serializer import ToDoListSerializer
from to_do_list.models import ToDoList


# Create your views here.

class ToDoListFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')

    class Meta:
        model = ToDoList
        fields = ['status', 'priority', 'due_date', 'start_date', 'end_date']


class TodoListListCreateAPIView(generics.ListCreateAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ToDoListFilter
    ordering_fields = ['due_date', 'status', 'priority', 'created_at']
    ordering = ['created_at']


class TodoDoListActiveAPIView(generics.ListAPIView):
    serializer_class = ToDoListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ToDoListFilter
    ordering_fields = ['due_date', 'status', 'priority', 'created_at']
    ordering = ['created_at']

    def get_queryset(self):
        ToDoList.objects.filter(
            Q(due_date__lt=date.today()) &
            Q(status__in=['pendente', 'em_andamento'])
        ).update(status='atrasada')

        return ToDoList.objects.filter(status__in=['em_andamento', 'pendente', 'atrasada'])


class ToDoListStatusCompletedCancelled(generics.ListAPIView):
    serializer_class = ToDoListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ToDoListFilter
    ordering_fields = ['due_date', 'status', 'priority', 'created_at']
    ordering = ['created_at']

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
