from django.urls import path
from . import views



urlpatterns = [
    path('to_do_list/', views.TodoListListCreateAPIView.as_view(), name='to-do-list-lis-create'),
    path('to_do_list/<int:pk>', views.TodoRetrieveUpdateDestroyAPIView.as_view(), name='to-do-list-retrieve-update-destroy')
]