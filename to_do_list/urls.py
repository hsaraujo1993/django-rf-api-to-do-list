from django.urls import path
from . import views

# urls da aplicação
urlpatterns = [
    path('to_do_list/', views.TodoListListCreateAPIView.as_view(), name='to-do-list-list-create'),
    path('to_do_list/ativos/', views.TodoDoListActiveAPIView.as_view(), name='to-do-list-list-active'),
    path('to_do_list/concluidas_canceladas/', views.ToDoListStatusCompletedCancelled.as_view(), name='to-do-list-list-completed-cancelled'),
    path('to_do_list/<int:pk>', views.TodoRetrieveUpdateDestroyAPIView.as_view(), name='to-do-list-retrieve-update-destroy')
]
