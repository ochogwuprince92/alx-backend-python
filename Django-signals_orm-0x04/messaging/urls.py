from django.urls import path
from .views import delete_user

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('inbox/', views.user_inbox, name='user_inbox'),
]