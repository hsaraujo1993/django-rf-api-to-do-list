from rest_framework import serializers
from to_do_list.models import ToDoList


# classe serializer da aplicação ToDoList
class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = '__all__' # indica que todos os campos do Model ToDoList serão serializados

    # função para validar os status disponível para atualização
    def validate_status(self, value):
        request_method = self.context['request'].method  # acessando a instância para receber qual metodo HTTP foi realizado na requisição

        if request_method in ['PUT', 'PATCH']:  # se o metodo realizado for PUT ou PATCH, entrará no if
            allowed_statuses_update = ['em_andamento', 'concluida', 'cancelada']  # status que permitem atualização
            if value not in allowed_statuses_update:  # se o value(status) não está na lista de status permitidos
                raise serializers.ValidationError(
                    f'O status "{value}" não é permitido para atualizações. Permitidos: {", ".join(allowed_statuses_update)}.'
                )

        return value
