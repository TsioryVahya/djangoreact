from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def recherche_view(request):
    return render(request, 'problemes/recherche.html')
