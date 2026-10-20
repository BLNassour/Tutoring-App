from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.ta_dashboard, name='ta_dashboard'),
    path('ta/<int:pk>/', views.ta_detail, name='ta_detail'),
    path('edit-schedule/', views.edit_availability, name='edit_availability'),
    path('delete-slot/<int:pk>/', views.delete_availability, name='delete_availability'),
    path('delete-ta/<int:pk>/', views.delete_ta, name='delete_ta'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
