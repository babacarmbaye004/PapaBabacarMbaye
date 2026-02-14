from django.shortcuts import render, redirect, get_object_or_404
from .models import Livre, Emprunt
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.utils import timezone

def liste_livres(request):
    livres_list = Livre.objects.all()
    
    # Pagination
    paginator = Paginator(livres_list, 5) # 5 livres par page
    page_number = request.GET.get('page')
    livres = paginator.get_page(page_number)
    
    # Nombre de livres dispo
    total_livres = Livre.objects.count()
    livres_empruntes = Emprunt.objects.filter(dateRetour__isnull=True).count()
    livres_dispo = total_livres - livres_empruntes
    
    # Auteur avec le plus de livres
    auteur_prolifique = Livre.objects.values('auteur').annotate(num_livres=Count('id')).order_by('-num_livres').first()
    
    context = {
        'livres': livres,
        'livres_dispo': livres_dispo,
        'auteur_prolifique': auteur_prolifique,
    }
    return render(request, 'gestion_biblio/liste_livres.html', context)

def ajouter_livre(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        auteur = request.POST.get('auteur')
        isbn = request.POST.get('isbn')
        if titre and auteur and isbn:
            Livre.objects.create(titre=titre, auteur=auteur, isbn=isbn)
            messages.success(request, "Livre ajouté avec succès !")
            return redirect('liste_livres')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    return render(request, 'gestion_biblio/ajouter_livre.html')

def ajouter_emprunt(request):
    livres = Livre.objects.all()
    if request.method == 'POST':
        livre_id = request.POST.get('livre')
        date_emprunt = request.POST.get('dateEmprunt')
        
        if livre_id and date_emprunt:
            livre = get_object_or_404(Livre, id=livre_id)
            Emprunt.objects.create(livre=livre, dateEmprunt=date_emprunt)
            messages.success(request, "Emprunt enregistré !")
            return redirect('liste_livres')
        else:
            messages.error(request, "Champs manquants.")
            
    return render(request, 'gestion_biblio/ajouter_emprunt.html', {'livres': livres})
