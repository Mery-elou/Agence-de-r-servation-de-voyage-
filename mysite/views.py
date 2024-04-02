from django.shortcuts import redirect, render

from Voyages.models import Promotion, Voyages
from django.db.models import Q

from reservation.models import Cart, Client, Commentaire
def about(request):
    user=request.user
    cart= Cart.objects.count()
    context={
        "cart_count":cart,
        "user":user,
        
        }
    
    
    return render(request, 'about.html',context)


def index(request):
    user=request.user
    # client=Client.objects.filter(user=user).first()
    tous_Voyages=Voyages.objects.all()
    if user.is_authenticated:
        # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0

    voyages_en_promotion = Voyages.objects.filter(promotions=True)

    for voyage in voyages_en_promotion:
        promotion_associee = Promotion.objects.filter(voyage=voyage).first()

        if promotion_associee:
            nouveau_prix = voyage.prix - (voyage.prix * (promotion_associee.pourcentage / 100))
            voyage.nouveau_prix = nouveau_prix
        else:
            # Ajustez le comportement en cas d'absence de promotion
            voyage.nouveau_prix = voyage.prix

    context = {"Voyages": tous_Voyages, "VoyagesEnPromotion": voyages_en_promotion, "user": user,"cart_count":cart}

    return render(request, 'index.html', context)


def Search(request):
    sort_option = request.GET.get('sort')    
    destination = request.GET.get('destination')
    room = request.GET.get('room')
    adult = request.GET.get('adult')
    children = request.GET.get('children')
    check_in = request.GET.get('check-in')
    check_out = request.GET.get('check-out')

    if any([destination, room, adult, children, check_in, check_out]):
        # Build the filter conditions using Q objects
        filters = Q()

        if destination:
            filters &= Q(destination__icontains=destination)
        if room:
            filters &= Q(nombre_de_pieces__gte=room)
        if adult:
            # Ensure the number of adults is less than or equal to the available places for adults
            filters &= Q(nombre_de_places_adultes__gte=adult)
        if children:
            filters &= Q(nombre_de_places_enfants__gte=children)
        if check_in:
            filters |= Q(date_depart=check_in)
        if check_out:
            filters |= Q(date_arrive=check_out)

        # Apply the filters to the Voyages model
        results = Voyages.objects.filter(filters)
        # Check the sorting option
        if sort_option == 'prix':
            results = results.order_by('prix')
        elif sort_option == 'date_depart':
            results = results.order_by('date_depart')
    else:
        results = Voyages.objects.none()
    
    user=request.user
    if user.is_authenticated:
            # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0
    for result in results:
        result.difference_jours = (result.date_arrive - result.date_depart).days
    # Do something with difference_jours

    context={
        'cart_count':cart,
        'user':user,
        'VoyagesDispo': results,
        'destination': destination,
        'room': room,
        'adult': adult,
        'children': children,
        'check_in': check_in,
        'check_out': check_out
        }
    return render(request, 'VoyagesDispo.html',context)



def comment(request):
    """Ajoute un commentaire à une réservation"""
    comment=Commentaire.objects.all()
    user=request.user
    if user.is_authenticated:
            # Si l'utilisateur est authentifié, récupérez le panier
        cart = Cart.objects.filter(client__user=user).count()
    else:
        # Si l'utilisateur n'est pas authentifié, initialisez le panier à zéro
        cart = 0

    context={
        "cart_count":cart,
        "user":user,
        "commentaire":comment
        
        }
    
    return render(request,'commentaire.html',context)
def ajout_comment(request):
    if request.method == 'POST':
        nom=request.POST.get('comment_name')
        message=request.POST.get('comment_message')
        Commentaire.objects.create(name=nom,message=message)
        return redirect ('comment')
def deletecomment(request,id):
    comment=Commentaire.objects.get(id=id)
    comment.delete()
    return redirect('com')




def batch(sequence, count):
    """
    Splits the sequence into lists of the given size (count).
    """
    return [sequence[i:i + count] for i in range(0, len(sequence), count)]