from django.contrib import admin
from to_do_list.models import ToDoList

# Register your models here.


@admin.register(ToDoList)
class ToDoList(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "priority",
        "due_date"
    )
