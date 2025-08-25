from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),




    path('api/tasks/<str:req_task_id>/', views.todo_api, name='task-detail'),
    path('api/tasks/', views.todo_api, name='task-list'),
    path('api/tasks/clear_completed/', views.todo_api, name='clear-completed'),




















]