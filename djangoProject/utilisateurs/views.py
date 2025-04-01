from django.db.models import Q, Max, Subquery, OuterRef, Value, TextField
from django.db.models.functions import Coalesce  # Ajout de cet import

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from conversations.models import Conversation
from mess.models import Mess
from .models import Utilisateur
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            return redirect('dashboard')  # Changé de 'accueil' à 'dashboard'
        else:
            messages.error(request, 'Identifiants invalides.')
    return render(request, 'utilisateurs/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'utilisateurs/dashboard.html', {
        'user': request.user
    })

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return redirect('signup')
            
        try:
            user = Utilisateur.objects.create_user(
                nom_utilisateur=username,
                email=email,
                mot_de_passe=password1
            )
            messages.success(request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('login')
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'utilisateurs/signup.html')


@login_required
def user_list_view(request):
    users = Utilisateur.objects.exclude(id=request.user.id).annotate(
        last_message=Coalesce(
            Subquery(
                Mess.objects.filter(
                    id_conversation__in=Conversation.objects.filter(
                        Q(id_participant1=OuterRef('id'), id_participant2=request.user.id) |
                        Q(id_participant1=request.user.id, id_participant2=OuterRef('id'))
                    )
                ).order_by('-horodatage').values('contenu')[:1]
            ),
            Value(''),
            output_field=TextField()
        )
    )
    return render(request, 'utilisateurs/user_list.html', {'users': users})


@login_required
def get_conversation(request, user_id):
    other_user = get_object_or_404(Utilisateur, id=user_id)

    conversation = Conversation.objects.filter(
        (Q(id_participant1=request.user) & Q(id_participant2=other_user)) |
        (Q(id_participant1=other_user) & Q(id_participant2=request.user))
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(
            id_participant1=request.user,
            id_participant2=other_user
        )

    messages = Mess.objects.filter(id_conversation=conversation).order_by('horodatage')

    return JsonResponse({
        'messages': [{
            'contenu': msg.contenu,
            'expediteur': msg.id_expediteur.nom_utilisateur,
            'horodatage': msg.horodatage.strftime("%Y-%m-%d %H:%M:%S"),
            'is_mine': msg.id_expediteur == request.user,
            'avatar_url': msg.id_expediteur.profil.url_avatar if hasattr(msg.id_expediteur,
                                                                         'profil') and msg.id_expediteur.profil.url_avatar else None
        } for msg in messages],
        'conversation_id': conversation.id,
        'other_user_avatar': other_user.profil.url_avatar if hasattr(other_user,
                                                                     'profil') and other_user.profil.url_avatar else None
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        message_content = request.POST.get('message')

        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Verify user is part of conversation
        if request.user not in [conversation.id_participant1, conversation.id_participant2]:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        message = Mess.objects.create(
            id_conversation=conversation,
            id_expediteur=request.user,
            contenu=message_content
        )

        return JsonResponse({
            'status': 'success',
            'message': {
                'contenu': message.contenu,
                'expediteur': message.id_expediteur.nom_utilisateur,
                'horodatage': message.horodatage.strftime("%Y-%m-%d %H:%M:%S"),
                'is_mine': True
            }
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def get_new_messages(request, conversation_id, last_message_time):
    from datetime import datetime
    from django.utils.dateparse import parse_datetime

    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Vérifier que l'utilisateur fait partie de la conversation
    if request.user not in [conversation.id_participant1, conversation.id_participant2]:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Convertir last_message_time en objet datetime
    last_time = parse_datetime(last_message_time)

    # Récupérer les nouveaux messages
    new_messages = Mess.objects.filter(
        id_conversation=conversation,
        horodatage__gt=last_time
    ).order_by('horodatage')

    return JsonResponse({
        'messages': [{
            'contenu': msg.contenu,
            'expediteur': msg.id_expediteur.nom_utilisateur,
            'horodatage': msg.horodatage.strftime("%Y-%m-%d %H:%M:%S"),
            'is_mine': msg.id_expediteur == request.user,
            'avatar_url': msg.id_expediteur.profil.url_avatar if hasattr(msg.id_expediteur,
                                                                         'profil') and msg.id_expediteur.profil.url_avatar else None
        } for msg in new_messages]
    })


