from rest_framework import serializers
from to_do_list.models import ToDoList


class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = '__all__'

    def validate_status(self, value):
        request_method = self.context['request'].method
        if request_method in ['PUT', 'PATCH']:
            allowed_statuses = ['em_andamento', 'concluida', 'cancelada']
            if value not in allowed_statuses:
                raise serializers.ValidationError(f'O status "{value}" não é permitido.')
        return value
