from django.urls import path

from . import views


urlpatterns = [
    path('create/', views.ticket_create, name='ticket_create'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('<int:ticket_id>/edit/', views.ticket_edit, name='ticket_edit'),
    path('<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),
]