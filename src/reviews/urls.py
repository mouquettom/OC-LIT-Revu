from django.urls import path

from . import views


urlpatterns = [
    path('create/', views.review_create_with_ticket, name='review_create_with_ticket'),
    path('reply/', views.review_pick_ticket, name='review_pick_ticket'),
    path('reply/<int:ticket_id>/', views.review_create_for_ticket, name='review_create_for_ticket'),
    path('<int:review_id>/edit/', views.review_edit, name='review_edit'),
    path('<int:review_id>/delete/', views.review_delete, name='review_delete'),
]