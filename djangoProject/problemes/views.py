from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import Probleme
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)

def get_problemes(request):
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
                } if probleme.id_utilisateur else None
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

# Create your views here.
