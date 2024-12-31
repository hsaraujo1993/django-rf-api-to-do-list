from django import forms
from django.contrib import admin
from .models import ToDoList


#  formulário baseado no model ToDoList
class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = '__all__'


#  configuração personalizada do painel de administração do Django para o model ToDoList
@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "priority",
        "due_date"
    )  # campos que serão exibidos na lista de objetos no Admin django
    form = ToDoListForm  # especificando o formulário que será utilizado para criar ou editar as instâncias do model

    # modificando o formulario gerado pelo django admin antes que ele seja exibido
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)  # obter o formulario gerado automaticamente pelo django
        if obj is None:  # se objeto for None, indica que o formulario usado é para criar um novo registro, não um update ou delete
            form.fields[
                'status'].widget = forms.HiddenInput()  # como é um formulario de criação, devemos remover o campo status desse formulario, já que a tarefa é criada com status pendente
        return form
