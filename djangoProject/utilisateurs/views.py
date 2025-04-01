from django.db.models import Q, Max, Subquery, OuterRef, Value, TextField
from django.db.models.functions import Coalesce  # Ajout de cet import

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from conversations.models import Conversation
from mess.models import Mess
from .models import Utilisateur
from django.contrib.auth.forms import UserCreationForm
from profils.models import Profil
from datetime import datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            
            # Stocker les informations importantes de l'utilisateur dans la session
            request.session['user_id'] = user.id
            request.session['username'] = user.nom_utilisateur  # Stocker le nom d'utilisateur
            request.session['email'] = user.email  # Stocker l'email si nécessaire
            
            # Si vous avez besoin de plus d'informations, vous pouvez les ajouter ici
            # Par exemple, si l'utilisateur a un profil avec une image
            if hasattr(user, 'profil') and user.profil:
                request.session['avatar'] = user.profil.url_avatar
            
            # Forcer la sauvegarde de la session
            request.session.save()
            
            return redirect('accueil')
        else:
            messages.error(request, 'Identifiants invalides.')
    return render(request, 'utilisateurs/login.html')

@login_required
def after_login(request):
    # Vérifier que les données de session sont bien présentes
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    
    # Loguer les informations pour le débogage
    print(f"Session user_id: {user_id}")
    print(f"Session username: {username}")
    print(f"request.user: {request.user}")
    
    context = {
        'session_user_id': user_id,
        'session_username': username,
    }
    
    # Redirige vers home.html après la connexion avec le contexte
    return render(request, 'utilisateurs/home.html', context)

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
def profile_view(request):
    # Récupérer l'utilisateur courant
    user = request.user
    
    # Récupérer le profil associé à l'utilisateur ou en créer un s'il n'existe pas
    profile, created = Profil.objects.get_or_create(id_utilisateur=user)
    
    context = {
        'user': user,
        'profile': profile,
    }
    
    return render(request, 'utilisateurs/profile.html', context)

@login_required
def user_list_view(request):
    users = Utilisateur.objects.exclude(id=request.user.id)
    
    for user in users:
        # Trouver la conversation entre l'utilisateur courant et cet utilisateur
        conversation = Conversation.objects.filter(
            Q(id_participant1=user, id_participant2=request.user) |
            Q(id_participant1=request.user, id_participant2=user)
        ).first()
        
        if conversation:
            # Récupérer le dernier message de cette conversation
            last_message = Mess.objects.filter(
                id_conversation=conversation
            ).order_by('-horodatage').first()
            
            if last_message:
                user.last_message = last_message.contenu
                user.last_message_date = last_message.horodatage
            else:
                user.last_message = "Pas de message"
                user.last_message_date = None
        else:
            user.last_message = "Pas de message"
            user.last_message_date = None
    
    # Trier les utilisateurs : ceux avec des messages d'abord, triés par date
    users = sorted(
        users,
        key=lambda x: (x.last_message_date or datetime.min),
        reverse=True
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
        other_user = conversation.id_participant2 if conversation.id_participant1 == request.user else conversation.id_participant1

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
            },
            'other_user_id': other_user.id,
            'last_message': message_content
        })

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

    # Trouver l'autre participant de la conversation
    other_user = conversation.id_participant2 if conversation.id_participant1 == request.user else conversation.id_participant1

    return JsonResponse({
        'messages': [{
            'contenu': msg.contenu,
            'expediteur': msg.id_expediteur.nom_utilisateur,
            'horodatage': msg.horodatage.strftime("%Y-%m-%d %H:%M:%S"),
            'is_mine': msg.id_expediteur == request.user,
            'avatar_url': msg.id_expediteur.profil.url_avatar if hasattr(msg.id_expediteur,
                                                                         'profil') and msg.id_expediteur.profil.url_avatar else None
        } for msg in new_messages],
        'other_user_id': other_user.id,
        'last_message': new_messages.last().contenu if new_messages.exists() else None
    })

@login_required
def get_all_last_messages(request):
    latest_messages = []
    most_recent_date = None
    
    # D'abord, trouvez toutes les conversations impliquant l'utilisateur actuel
    conversations = Conversation.objects.filter(
        Q(id_participant1=request.user) | Q(id_participant2=request.user)
    )
    
    for conv in conversations:
        # Déterminer l'autre utilisateur dans la conversation
        other_user = conv.id_participant2 if conv.id_participant1 == request.user else conv.id_participant1
        
        # Obtenir le dernier message de cette conversation
        last_message = Mess.objects.filter(id_conversation=conv).order_by('-horodatage').first()
        
        if last_message:
            if not most_recent_date or last_message.horodatage > most_recent_date:
                most_recent_date = last_message.horodatage
                
            latest_messages.append({
                'user_id': other_user.id,
                'content': last_message.contenu,
                'timestamp': last_message.horodatage.isoformat(),
            })
    
    # Trier les messages par horodatage et marquer le plus récent
    sorted_messages = sorted(latest_messages, key=lambda x: x['timestamp'], reverse=True)
    if sorted_messages:
        sorted_messages[0]['is_most_recent'] = True
    
    return JsonResponse({'last_messages': sorted_messages})

def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')  # Redirige vers la page de connexion après déconnexion


