from django.urls import path
from .views import UserRegisterView, UserLoginView

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('signup/', UserRegisterView.as_view())
]