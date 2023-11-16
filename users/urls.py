from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('registration/', views.RegisterView.as_view(), name='registration'),
]
