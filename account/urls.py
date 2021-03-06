from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import HomeView, LoginPage, RegisterPage, activate

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]
