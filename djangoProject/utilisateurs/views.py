import json
from django.db.models import Q, Max, Subquery, OuterRef, Value, TextField, Count, Exists
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Exists, OuterRef
from conversations.models import Conversation
from mess.models import Mess
from .models import Utilisateur
from problemes.models import Probleme
from reactionproblemes.models import ReactionProbleme

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
    print(f"Getting conversation with user_id: {user_id}")
    other_user = get_object_or_404(Utilisateur, id=user_id)
    print(f"Other user found: {other_user.nom_utilisateur}")

    conversation = Conversation.objects.filter(
        (Q(id_participant1=request.user) & Q(id_participant2=other_user)) |
        (Q(id_participant1=other_user) & Q(id_participant2=request.user))
    ).first()

    if not conversation:
        print("Creating new conversation")
        conversation = Conversation.objects.create(
            id_participant1=request.user,
            id_participant2=other_user
        )
    else:
        print(f"Found existing conversation: {conversation.id}")

    messages = Mess.objects.filter(id_conversation=conversation).order_by('horodatage')
    print(f"Found {messages.count()} messages")

    response_data = {
        'messages': [{
            'contenu': msg.contenu,
            'expediteur': msg.id_expediteur.nom_utilisateur,
            'horodatage': msg.horodatage.strftime("%Y-%m-%d %H:%M:%S"),
            'is_mine': msg.id_expediteur == request.user
        } for msg in messages],
        'conversation_id': conversation.id
    }
    print("Returning response:", response_data)
    return JsonResponse(response_data)

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

@login_required
def get_posts(request):
    page = request.GET.get('page', 1)
    
    posts = (Probleme.objects
        .select_related('auteur')
        .prefetch_related('reactions')
        .annotate(
            comments=Count('reponses', distinct=True),
            has_liked=Exists(
                ReactionProbleme.objects.filter(
                    id_probleme=OuterRef('pk'),
                    id_utilisateur=request.user
                )
            ),
            likes_count=Count('reactions', distinct=True)
        )
        .order_by('-date_creation')
    )
    
    paginator = Paginator(posts, 10)
    
    try:
        posts_page = paginator.page(page)
    except:
        return JsonResponse({'posts': []})
    
    posts_data = [{
        'id': post.id,
        'content': post.contenu,
        'title': post.titre,
        'username': 'Anonyme' if post.est_anonyme else post.auteur.nom_utilisateur,
        'user_id': None if post.est_anonyme else post.auteur.id,
        'created_at': post.date_creation.isoformat(),
        'likes_count': post.likes_count,  # Nombre réel de likes de la base de données
        'comments': post.comments,        # Nombre de commentaires
        'is_anonymous': post.est_anonyme,
        'has_liked': post.has_liked      # Si l'utilisateur actuel a liké
    } for post in posts_page]
    
    return JsonResponse({
        'posts': posts_data,
        'has_next': posts_page.has_next()
    })

@login_required
def toggle_like(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')  # Changé de probleme_id à post_id
            
            print(f"Toggling like for post: {post_id}")  # Debug log
            
            if post_id is None:
                return JsonResponse({
                    'success': False,
                    'error': 'Post ID is required'
                }, status=400)

            probleme = get_object_or_404(Probleme, id=post_id)
            
            # Check if user has already liked this post
            reaction = ReactionProbleme.objects.filter(
                id_probleme=probleme,
                id_utilisateur=request.user
            ).first()
            
            if reaction:
                # Unlike
                print(f"Removing like for post {post_id}")  # Debug log
                reaction.delete()
                is_liked = False
            else:
                # Like
                print(f"Adding like for post {post_id}")  # Debug log
                ReactionProbleme.objects.create(
                    id_probleme=probleme,
                    id_utilisateur=request.user
                )
                is_liked = True

            likes_count = probleme.reactions.count()
            print(f"New likes count: {likes_count}")  # Debug log
            
            return JsonResponse({
                'success': True,
                'is_liked': is_liked,
                'likes_count': likes_count
            })
            
        except Exception as e:
            print(f"Error in toggle_like: {str(e)}")  # Debug log
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request method'
    }, status=405)


