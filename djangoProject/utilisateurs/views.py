import logging

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User
from profiles.models import Profile

logger = logging.getLogger(__name__)

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'utilisateurs/register.html'
    
    def form_valid(self, form):
        user = form.save()
        # Create a profile for the user
        Profile.objects.create(user=user)
        login(self.request, user)
        messages.success(self.request, 'Inscription réussie. Bienvenue!')
        return redirect('accueil')

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'utilisateurs/login.html'
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        logger.debug(f"Tentative de connexion pour l'utilisateur : {username}")
        
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            logger.info(f"Connexion réussie pour l'utilisateur : {username}")
            messages.success(self.request, 'Connexion réussie.')
            return redirect(self.get_success_url())
        else:
            logger.warning(f"Échec de connexion pour l'utilisateur : {username}")
            messages.error(self.request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """If the form is invalid, add an error message and render the form."""
        messages.error(self.request, 'Connexion échouée. Veuillez vérifier votre nom d\'utilisateur et votre mot de passe.')
        return super().form_invalid(form)

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Vous êtes maintenant déconnecté.')
    return redirect('login')

class AccueilView(TemplateView):
    template_name = 'utilisateurs/accueil.html'
