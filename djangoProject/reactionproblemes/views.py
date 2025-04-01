from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import ReactionProbleme
from problemes.models import Probleme
import json

# Create your views here.

@csrf_exempt
@require_POST
def toggle_reaction(request):
    try:
        data = json.loads(request.body)
        probleme_id = data.get('probleme_id')
        utilisateur = request.user

        if not utilisateur.is_authenticated:
            return JsonResponse({'error': 'Utilisateur non authentifié'}, status=401)

        probleme = Probleme.objects.get(id=probleme_id)
        reaction, created = ReactionProbleme.objects.get_or_create(
            id_probleme=probleme,
            id_utilisateur=utilisateur
        )

        if not created:
            reaction.delete()
            return JsonResponse({'message': 'Réaction supprimée', 'liked': False}, status=200)

        return JsonResponse({'message': 'Réaction ajoutée', 'liked': True}, status=201)

    except Probleme.DoesNotExist:
        return JsonResponse({'error': 'Problème introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
