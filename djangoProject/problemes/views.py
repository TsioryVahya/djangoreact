from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json
from .models import Probleme
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def probleme_list_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            titre = data.get('titre')
            contenu = data.get('contenu')
            est_anonyme = data.get('est_anonyme', False)

            if not titre or not contenu:  # Correction ici
                return JsonResponse({
                    'error': 'Le titre et le contenu sont requis'
                }, status=400)

            # Créer le nouveau problème
            probleme = Probleme.objects.create(
                titre=titre,
                contenu=contenu,
                est_anonyme=est_anonyme,
                id_utilisateur=request.user if request.user.is_authenticated else None
            )

            # Préparer la réponse
            response_data = {
                'id': probleme.id,
                'titre': probleme.titre,
                'contenu': probleme.contenu,
                'est_anonyme': probleme.est_anonyme,
                'date_creation': probleme.date_creation.isoformat(),
                'id_utilisateur': {
                    'nom_utilisateur': request.user.nom_utilisateur if request.user.is_authenticated else 'Anonyme'
                } if not probleme.est_anonyme else None
            }

            return JsonResponse(response_data, status=201)

        except Exception as e:
            logger.error(f"Erreur lors de la création du problème: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    # GET request - liste des problèmes
    try:
        problemes = Probleme.objects.select_related('id_utilisateur', 'id_utilisateur__profil').all().order_by('-date_creation')
        logger.info(f"Nombre de problèmes trouvés: {problemes.count()}")
        
        page_number = request.GET.get('page', 1)
        paginator = Paginator(problemes, 10)  # 10 problèmes par page
        page_obj = paginator.get_page(page_number)
        
        results = []
        for probleme in page_obj:
            result = {
                'id': probleme.id,
                'contenu': probleme.contenu,
                'est_anonyme': probleme.est_anonyme,
                'date_creation': probleme.date_creation.isoformat(),
                'id_utilisateur': {
                    'nom_utilisateur': probleme.id_utilisateur.nom_utilisateur,
                    'profil': {
                        'url_avatar': probleme.id_utilisateur.profil.url_avatar if hasattr(probleme.id_utilisateur, 'profil') else None
                    }
                } if probleme.id_utilisateur else None,
                'likes': probleme.reactions.count()  # Nombre de réactions
            }
            results.append(result)
        
        response_data = {
            'results': results,
            'has_next': page_obj.has_next(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages
        }
        
        logger.info(f"Données renvoyées: {response_data}")
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des problèmes: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def recherche_view(request):
    return render(request, 'problemes/recherche.html')
