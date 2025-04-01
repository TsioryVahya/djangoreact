from django.db.models import Q
from rest_framework import viewsets, filters, pagination
from rest_framework.response import Response
from .models import Probleme
from .serializers import ProblemeSerializer

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProblemeViewSet(viewsets.ModelViewSet):
    queryset = Probleme.objects.all().order_by('-date_creation')
    serializer_class = ProblemeSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            print(f"Searching for: {search_query}")
            # Filter by title or content containing the search query
            queryset = queryset.filter(
                Q(titre__icontains=search_query) | 
                Q(contenu__icontains=search_query)
            )
            print(f"Results count: {queryset.count()}")
         
        return queryset