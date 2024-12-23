from to_do_list.serializer import TodoListSerializer
from to_do_list.models import ToDoList
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class TodoListListCreateAPIView(generics.ListCreateAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = TodoListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority']


class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = TodoListSerializer
