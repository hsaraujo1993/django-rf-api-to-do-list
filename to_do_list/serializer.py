from rest_framework import serializers
from to_do_list.models import ToDoList


class TodoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDoList
        fields = '__all__'