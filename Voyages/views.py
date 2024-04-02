from django.shortcuts import get_object_or_404, redirect, render
from reservation.models import Administrator, Cart, Client, Contact, Favoris
from django.contrib.auth.decorators import login_required

from .models import Hotel, Promotion, Voyages

#les catégoris de voyages 
def voyages_couples(request):
    user=request.user
    if user.is_authenticated:
            # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0

    couples = Voyages.objects.filter(categories='cat1')
   
    for couple in couples:
        couple.difference_jours = (couple.date_arrive - couple.date_depart).days
    return render(request, 'couples.html', {'couples': couples,'cart_count':cart})

def voyages_equipes(request):
    user=request.user
    if user.is_authenticated:
            # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0

    equipes = Voyages.objects.filter(categories='cat3')
    for equipe in equipes:
        equipe.difference_jours = (equipe.date_arrive - equipe.date_depart).days
    return render(request, 'Equipes.html', {'equipes': equipes,'cart_count':cart})

def voyages_familles(request):
    
    user=request.user
    if user.is_authenticated:
            # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0

    familles = Voyages.objects.filter(categories='cat2')
    for famille in familles:
       famille.difference_jours = (famille.date_arrive - famille.date_depart).days
    return render(request, 'familles.html', {'familles': familles,'cart_count':cart})

def voyages_Hajs(request):
    user=request.user
    if user.is_authenticated:
            # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0

    Hajs = Voyages.objects.filter(categories='cat4')
    for Haj in Hajs:
       Haj.difference_jours = (Haj.date_arrive - Haj.date_depart).days
    return render(request, 'hajs.html', {'Hajs': Hajs,'cart_count':cart})

@login_required(login_url='signin')
def detail(request,id_voyage):
    voyage=Voyages.objects.get(id=id_voyage)
    user=request.user
    client = Client.objects.filter(user=user).first()
    if user.is_authenticated:
            # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0

    favoris=Favoris.objects.filter(client=client,voyage=voyage)
    voyage.difference_jours = (voyage.date_arrive - voyage.date_depart).days
    try:
        promotion_associee = Promotion.objects.get(voyage=voyage)
        
        # Calculer le nouveau prix en cas de promotion
        voyage.prix = voyage.prix - (voyage.prix * (promotion_associee.pourcentage / 100))
    except Promotion.DoesNotExist:
        # S'il n'y a pas de promotion, utiliser le prix normal comme nouveau prix
        voyage.prix = voyage.prix
    return render(request,"detail.html",{'voyage':voyage,'favoris':favoris,'cart_count':cart})


def promo(request):
    voyages_en_promotion = Voyages.objects.filter(promotions=True)
    user=request.user
    if user.is_authenticated:
            # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0

    for voyage in voyages_en_promotion:
        promotion_associee = Promotion.objects.filter(voyage=voyage).first()

        if promotion_associee:
            nouveau_prix = round(voyage.prix - (voyage.prix * (promotion_associee.pourcentage / 100)), 2)
            voyage.nouveau_prix = nouveau_prix
            voyage.difference_jours = (voyage.date_arrive - voyage.date_depart).days
            voyage.pourcentage=promotion_associee.nom
        else:
            # Ajustez le comportement en cas d'absence de promotion
            voyage.nouveau_prix = voyage.prix

    context = { "VoyagesEnPromotion": voyages_en_promotion,'cart_count':cart}
    return render(request, 'promo.html', context)

def DeleteVoyage(request, id):
    voyage = Voyages.objects.get(id=id)
    voyage.delete()
    return redirect("tousvoyages")

def tousvoyages(request):
    user = request.user
    admin = Administrator.objects.filter(user=user).first()
    voyages=Voyages.objects.all()
    hotels=Hotel.objects.all()
    promotions=Promotion.objects.all()
    notif= Contact.objects.filter( is_read=False).count()
    context ={
        'admin': admin,
        'voyages': voyages,
        'hotels': hotels,
        'promotions': promotions,
        'notif':notif,
    }
    return render (request,'tousVoyages.html',context)


def update_voyage(request, voyage_id):
    voyage = Voyages.objects.get(id=voyage_id)
    if request.method == 'POST':
        voyage.titre = request.POST.get('titre')
        voyage.description = request.POST.get('description')
        voyage.programme = request.POST.get('programme')
        voyage.info_pratique = request.POST.get('info_pratique')
        voyage.prix = request.POST.get('prix')
        voyage.date_depart = request.POST.get('date_depart')
        voyage.date_arrive = request.POST.get('date_arrive')
        voyage.destination = request.POST.get('destination')
        voyage.categories = request.POST.get('categories')
        voyage.nombre_de_places = request.POST.get('nombre_de_places')
        voyage.nombre_de_places_adultes = request.POST.get('nombre_de_places_adultes')
        voyage.nombre_de_places_enfants = request.POST.get('nombre_de_places_enfants')
        voyage.nombre_de_pieces = request.POST.get('nombre_de_pieces')
        voyage.promotions = bool(request.POST.get('promotions'))
        voyage.hotel = Hotel.objects.get(id=request.POST.get('hotel'))
        voyage.save()
        return redirect('tousvoyages')
    return render(request, 'tousVoyages.html', {'voyage': voyage})

def ajouter_voyage(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        programme = request.POST.get('programme')
        info_pratique = request.POST.get('info_pratique')
        prix = request.POST.get('prix')
        date_depart = request.POST.get('date_depart')
        date_arrive = request.POST.get('date_arrive')
        destination = request.POST.get('destination')
        categories = request.POST.get('categories')
        nombre_de_places = request.POST.get('nombre_de_places')
        nombre_de_places_adultes = request.POST.get('nombre_de_places_adultes')
        nombre_de_places_enfants = request.POST.get('nombre_de_places_enfants')
        nombre_de_pieces = request.POST.get('nombre_de_pieces')
        promotions = bool(request.POST.get('promotions'))
        hotel_id = request.POST.get('hotel')
        isthebest_destination = bool(request.POST.get('isthebest_destination'))
        
        # Créez une instance de Voyage avec les données du formulaire
        voyage = Voyages.objects.create(
            titre=titre,
            description=description,
            programme=programme,
            info_pratique=info_pratique,
            prix=prix,
            date_depart=date_depart,
            date_arrive=date_arrive,
            destination=destination,
            categories=categories,
            nombre_de_places=nombre_de_places,
            nombre_de_places_adultes=nombre_de_places_adultes,
            nombre_de_places_enfants=nombre_de_places_enfants,
            nombre_de_pieces=nombre_de_pieces,
            promotions=promotions,
            isthebest_destination=isthebest_destination
        )

        # Ajoutez les images associées au voyage
        images = request.FILES.getlist('image')
        for image in images:
            voyage.photos.create(image=image)

        # Associez l'hôtel au voyage
        if hotel_id:
            voyage.hotel = Hotel.objects.get(id=hotel_id)
            voyage.save()

        return redirect('tousvoyages')

    return render(request, 'index.html')

def hotel(request):
    user = request.user
    hotels = Hotel.objects.all()
    admin = Administrator.objects.filter(user=user).first()
    notif= Contact.objects.filter( is_read=False).count()
    context={
        'admin': admin,
        'hotels': hotels,
        'notif':notif,
    }
    return render(request,'hotels.html',context)

def Deletehotel(request, id):
    hotel = Hotel.objects.get(id=id)
    hotel.delete()
    return redirect("hotel")

def update_hotel(request,hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    if request.method == 'POST':
        hotel.nom = request.POST.get('nom')
        hotel.adresse = request.POST.get('adress')
        hotel.telephone = request.POST.get('phone')
        hotel.email = request.POST.get('email')
        hotel.num_chambre = int(request.POST.get('chambre'))
        hotel.repas = request.POST.get('repas')
        hotel.save()
        return redirect('hotel')
    return render(request,'index.html')

def ajouter_hotel(request):
     if request.method == 'POST':
       nom = request.POST.get('nom')
       adresse = request.POST.get('adress')
       telephone = request.POST.get('phone')
       email = request.POST.get('email')
       num_chambre = int(request.POST.get('chambre'))
       repas = request.POST.get('repas')
       siteweb=request.POST.get('siteweb')
       hotel=Hotel.objects.create(
           nom=nom,
           adresse=adresse,
           code_postal=adresse,
           ville=adresse,
           pays=adresse,
           telephone=telephone,
           email=email,
           num_chambre=num_chambre,
           repas=repas,
           site_web=siteweb
           )
       
       images = request.FILES.getlist('image')
       for image in images:
            hotel.photos.create(image=image)
       return redirect('hotel')

     return render(request, 'index.html')
            
def promotion(request):
    user = request.user
    admin = Administrator.objects.filter(user=user).first()
    voyages=Voyages.objects.all()
    promotion=Promotion.objects.all()
    notif= Contact.objects.filter( is_read=False).count()
    context ={
        'admin': admin,
        'voyages': voyages,
        'promotion': promotion,
        'notif':notif,
    }
    print(promotion)
    return render(request,'promotions.html',context)    
    
def deletepromo(request,id):
    promo = Promotion.objects.get(id=id)
    promo.delete()
    return redirect("promotion") 

def update_promo(request,promo_id):
    promo = Promotion.objects.get(id=promo_id)
    if request.method == 'POST':
        promo.nom = request.POST.get('nom')
        promo.date_debut = request.POST.get('debut')
        promo.date_fin = request.POST.get('fin')
        promo.pourcentage = request.POST.get('pourcentage')
        voyage_id = request.POST.get('voyage')
        voyage = get_object_or_404(Voyages, id=voyage_id)
        promo.voyage = voyage
        promo.save()
        return redirect('promotion')
    return render(request,'index.html')

def ajouter_promo(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        date_debut = request.POST.get('debut')
        date_fin = request.POST.get('fin')
        voyage_id = request.POST.get('voyage')
        pourcentage = request.POST.get('pourcentage')
        voyage = get_object_or_404(Voyages, id=voyage_id)
        # Create the Promotion object
        promot = Promotion.objects.create(
            nom=nom,
            date_debut=date_debut,
            date_fin=date_fin,
            pourcentage=pourcentage,
            voyage=voyage
        )

     

        return redirect('promotion')

    return render(request, 'index.html')
