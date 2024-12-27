from django import forms
from django.contrib import admin
from .models import ToDoList


# Formulário personalizado
class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = '__all__'

    def clean_status(self):
        status = self.cleaned_data.get('status', '').lower()
        if not self.instance.pk and status != 'pendente':
            raise forms.ValidationError("O status deve iniciar como 'pendente'.")
        return status


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "priority",
        "due_date"
    )
    form = ToDoListForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['status'].widget = forms.HiddenInput()
        return form
