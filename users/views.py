from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView


def landing_page(request):
    return render(request, 'landing.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    



