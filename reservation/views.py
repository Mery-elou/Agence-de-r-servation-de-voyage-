
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from Voyages.models import Hotel, Promotion, Voyages
from reservation.models import Cart, Reservation
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.contrib import messages
from reservation.models import User
from .models import Administrator, Client, Commentaire, Contact, Favoris, Notification
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
import codecs
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponseForbidden
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        address = request.POST.get('ville', None)
        photo = request.FILES.get('image', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        date_naissance = request.POST.get('date_naissance', None)
        telephone = request.POST.get('telephone', None)

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'registerclient.html', {'error': True, 'message': 'Entrez un email valide !!!!!'})

        if password != repassword:
            return render(request, 'registerclient.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        if not name or not email or not password or not repassword:
            return render(request, 'registerclient.html', {'error': True, 'message': 'Veuillez remplir tous les champs nécessaires !'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'registerclient.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})

        # Hash the password and create a new user
        utilisateur = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        utilisateur.is_client = True
        utilisateur.save()

        # Create a client associated with the user
        client = Client.objects.create(
            user=utilisateur,
            address=address,
            date_naissance=date_naissance,
            phone_number=telephone,
            
        )
        client.image=photo
        client.save()
        
        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the dashboard
        return redirect('dashboard')

    return render(request, 'registerclient.html', {'error': False, 'message': ''})



def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.is_client:
                return redirect('dashboard')
            else:
                return redirect('dashboardAdmin')
    return render(request, 'Loginclient.html', {'error': True, 'message': "Mot de passe incorrect ou Utilisateur n'existe pas!"})


#se deconecter 
@login_required(login_url="signin")
def Logout(request):
    user = request.user
    client = Client.objects.filter(user=user).first()
    if client:
        Cart.objects.filter(client=client).delete()
    logout(request)
    return redirect('/')



@login_required(login_url="signin")
def dashboard(request):
    user = request.user
    client = Client.objects.filter(user=user).first()
    notification=Notification.objects.filter(client=client, is_read=False).count()
    return render(request, 'dashbord.html', {'client': client,'notif':notification})

#apdate information of a client 
@login_required(login_url='signin')
def ClientupdateProfil(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name', None)
        
        PhoneNumber = request.POST.get('telephone', None)

        address = request.POST.get('ville', None)
        date_naissance = request.POST.get('date_naissance', None)
        client = Client.objects.filter(user=user).first()
        user.first_name = name
       
        client.phone_number = PhoneNumber
        client.address = address
        client.date_naissance=date_naissance
        photo = request.FILES.get('image', None)

        if photo is not None:
            # Process the uploaded file
            # client.image.delete()
            client.image = photo
            
        """
        if isinstance(image, InMemoryUploadedFile):
            client.image.save(image.name,image)
        """
        user.save()
        client.save()

        return redirect("dashboard")
    
 #add a reservation   
@login_required(login_url='signin')
def forgot_password(request):
    error = False
    success = False
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        client = User.objects.filter(email=email).first()
        if client:
            token = default_token_generator.make_token(client)
            uid = urlsafe_base64_encode(force_bytes(client.id))
            current_site = request.META['HTTP_HOST']
            context = {
                "token":token,
                "uid":uid,
                "domaine":f"http://{current_site}"
            }

            print("processing forgot password")
            html = render_to_string("email.html", context)

            msg = EmailMessage(
                "Modification de mot de passe!",
                 html, 
                 "Travelscape <elouadymariem@gmail.com>" ,
                 [client.email]
 
            )

            msg.content_subtype = 'html'
            msg.send()
            
            message = "processing forgot password"
            success = True
        else:
            print("user does not exist")
            error = True
            message = "user does not exist"
    
    context = {
        'success': success,
        'error':error,
        'message':message
    }
    return render(request, "forgot_password.html", context)

@login_required(login_url='signin')
def update_password(request, token, uid):
        
    try:
        user_id = urlsafe_base64_decode(uid)
        decode_uid = codecs.decode(user_id, 'utf-8')
        user = User.objects.get(id=decode_uid)
    except:
        return HttpResponseForbidden("Vous n'aviez pas la permission de modifier ce mot de pass. Utilisateur introuvable")
    
    check_token = default_token_generator.check_token(user, token)
   
    if not check_token:
        return HttpResponseForbidden("Vous n'aviez pas la permission de modifier ce mot de pass. Votre Token est invalid ou a espiré")
    
    error = False
    success = False
    message = ""
    if request.method == "POST":
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        print(password , repassword)
        if repassword == password:
            try:
                validate_password(password, user)
                user.set_password(password)
                user.save()
                
                success = True
                message = "votre mot de pass a été modifié avec succès!"
                
            except ValidationError as e:
                error = True
                message = str(e)
        else:
            error = True
            message = "Les deux mot de pass ne correspondent pas"
           
    context = {
        "error": error,
        "success": success,
        "message": message
    }
    
   

    return render(request, "update_password.html", context)


    
def AddReservation(request, id, price,adult,enfant):
    if request.method == 'POST':
        user = request.user
        client = Client.objects.filter(user=user).first()
        voyage = Voyages.objects.filter(id=id).first()

        
        if voyage.nombre_de_places_adultes >= adult and voyage.nombre_de_places_enfants >= enfant:
                reservation = Reservation.objects.create(client=client, voyage=voyage, adult=adult, enfant=enfant, price=price)
                reservation.save()

                voyage.nombre_de_places_adultes -= adult
                voyage.nombre_de_places_enfants -= enfant
                voyage.save()

                # Check if the available places are now 0
                if voyage.nombre_de_places_adultes == 0 :
                    # Perform your additional logic here when places become 0
                    # For example, render a specific template or return an HttpResponse
                    return HttpResponse("No more available places pour les adults!")
                if  voyage.nombre_de_places_enfants == 0:
                   
                    return HttpResponse("No more available places pour les enfants!")
                return redirect("/")

#add a travel in the cart 

def add_to_Cart(request, id_voyage):
    user = request.user
    client = Client.objects.filter(user=user).first()
    voyage = Voyages.objects.get(id=id_voyage)
    
    if request.method == 'POST':
        adult = int(request.POST.get("adult"))  
        enfant = int(request.POST.get("enfant"))  

        sub_total = adult * voyage.prix + enfant * voyage.prix

        # Create a Cart object and store the total price
        cart_item = Cart.objects.create(client=client, voyage=voyage, adult=adult, enfants=enfant, prix=sub_total)

        # Update the total in the Cart model
        
        cart_item.save()
        return redirect('detail',id_voyage=voyage.id)


       
    # Your existing code

        

    return render(request, 'index.html')


#panier of client 
def panier(request):
    user=request.user
    client = Client.objects.filter(user=user).first()
    panier=Cart.objects.filter(client=client)
    notification= Notification.objects.filter(client=client, is_read=False).count()
    total_adult = sum(cart_item.prix*cart_item.adult for cart_item in panier)
    total_enfant= sum(cart_item.prix*cart_item.enfants for cart_item in panier)
    total_amount=total_enfant+total_adult
    context={'panier':panier,
             'notif':notification,
             'client':client,
             'total':total_amount}
    return render(request,'Panier.html',context)

def reservation(request):
    user=request.user
    client = Client.objects.filter(user=user).first()
    unread_count = Notification.objects.filter(client=client, is_read=False).count()

    reser=Reservation.objects.filter(client=client)
    
    context={'reser':reser,
             'notif':unread_count,
             'client':client}
    
    return render(request,'reservation.html',context)




#update number of children and adult

def updateAdulte(request, id):
    
        cart_item = Cart.objects.all()
        for cart in cart_item:
            if cart.id==id:
                if request.method == 'POST':
                    adult = request.POST.get('adulte')
                   
                    cart.adult = adult
                    
            cart.save()



        return redirect("panier")
 
def updateEnfants(request, id):
        
        cart_item = Cart.objects.all()
        for cart in cart_item:
            if cart.id==id:
                if request.method == 'POST':
                    adult = request.POST.get('enfant')
                   
                    cart.enfants = adult
                    
            cart.save()



        return redirect("panier")
    
 #delete element in the cart   
def DeleteVoyageCart(request, id):
    cart_item = Cart.objects.get(id=id)
    cart_item.delete()
    return redirect("panier")



@login_required(login_url="signin")
def payment(request):
    user = request.user
    client = Client.objects.filter(user=user).first()
    cart_items = Cart.objects.filter(client=client)

    total_adult = sum(cart_item.prix*cart_item.adult for cart_item in cart_items)
    total_enfant= sum(cart_item.prix*cart_item.enfants for cart_item in cart_items)
    total_amount=total_enfant+total_adult

    paypal_dict = {
        "business": "sb-beoyt29126624@business.example.com",
        "amount": str(total_amount),
        "item_name": "Voyages réservés",
        "invoice": str(client.id),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('payment_cancel')),
        "custom": "premium_plan",
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

        # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)
    
    



@login_required(login_url="/signin")
def payment_success(request):
    user = request.user
    client = Client.objects.filter(user=user).first()
    cart_items = Cart.objects.filter(client=client)
    
    # Calcul du montant total
    total_adult = sum(cart_item.prix * cart_item.adult for cart_item in cart_items)
    total_enfant = sum(cart_item.prix * cart_item.enfants for cart_item in cart_items)
    total_amount = total_enfant + total_adult

    # Créez une réservation pour chaque élément du panier
    for cart_item in cart_items:
        reservation = Reservation.objects.create(
            client=client,
            voyage=cart_item.voyage,
            adult=cart_item.adult,
            enfants=cart_item.enfants,
            prix=total_amount,
            status='en_attente'   
        )
        reservation.save()
        # cart_item.voyage.nombre_de_places-=(cart_item.adult+cart_item.enfants)
        cart_item.voyage.nombre_de_places_adultes -= cart_item.adult
        cart_item.voyage.nombre_de_places_enfants -= cart_item.enfants
        cart_item.voyage.save()
  
    cart_items.delete()
     
    messages.success(request, 'Paiement effectué avec succès.')

    # Reste de votre logique de succès de paiement
    return redirect('panier')


@login_required(login_url="signin")
def payment_cancel(request):
    
    messages.error(request, 'Vous avez annulé le paiement.')
    return redirect('panier')


#admin
def signupadmin(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        photo = request.FILES.get('image', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
       

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'adminregister.html', {'error': True, 'message': 'Entrez un email valide !!!!!'})

        if password != repassword:
            return render(request, 'adminregister.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        if not name or not email or not password or not repassword:
            return render(request, 'adminregister.html', {'error': True, 'message': 'Veuillez remplir tous les champs nécessaires !'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'adminregister.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})

        # Hash the password and create a new user
        utilisateur = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        utilisateur.is_client = False
        utilisateur.is_administrateur=True
        utilisateur.save()

        # Create a client associated with the user
        admin = Administrator.objects.create(
            user=utilisateur,
   
            
        )
        admin.image=photo
        admin.save()
        
        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the dashboard
        return redirect('dashboardAdmin')

    return render(request, 'adminregister.html', {'error': False, 'message': ''})

@login_required(login_url="/signin")
def dashboardAdmin(request):
    user = request.user
    admin = Administrator.objects.filter(user=user).first()
    clients=Client.objects.all()
    reservation=Reservation.objects.all()
    voyages=Voyages.objects.all()
    hotels=Hotel.objects.all()
    promotions=Promotion.objects.all()
    notif= Contact.objects.filter( is_read=False).count()
    context = {
        'admin': admin,
        'clients': clients,
        'reservations': reservation,
        'voyages': voyages,
        'hotels': hotels,
        'promotions': promotions,
        'notif':notif,
    }
    return render(request, 'dashboardAdmin.html', context)

def clients(request):
     user = request.user
     admin = Administrator.objects.filter(user=user).first()
     clients=Client.objects.all()
     notif= Contact.objects.filter( is_read=False).count()
     reservations=Voyages.objects.all()

     context ={
        'admin': admin,
        'clients': clients,
        'client_reservations': reservations,
        'notif':notif,
    }
     return render (request,'clients.html',context)
 
 
 
def tousreservation(request):
     user = request.user
     admin = Administrator.objects.filter(user=user).first()
     reservation=Reservation.objects.all()
     notif= Contact.objects.filter( is_read=False).count()
     context ={
        'admin': admin,
        'reservations': reservation,
        'notif':notif,
    }
     return render (request,'tousreservations.html',context)
 


def Deleteclient(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect("clients")

def Deletereservation(request, id):
    reservation = Reservation.objects.get(id=id)
    reservation.delete()
    return redirect("tousreservation")


def notification(request):
    user=request.user
    client=Client.objects.filter(user=user).first()
    voyages=Voyages.objects.all()
    notification=Notification.objects.filter(client=client)
    notif= Notification.objects.filter(client=client, is_read=False).count()
    context={
        'notification':notification,
        'voyages':voyages,
        'client':client,
        'notif':notif,
    }
    return render (request, "notifivation.html",context) 

def notify_user_about_upcoming_voyage(request,user_id):
    client=Client.objects.get(id=user_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        voyage_id=request.POST.get('voyage')
        voyage=Voyages.objects.get(id=voyage_id)
        date = datetime.now() 
        Notification.objects.create(client=client, date=date, voyage=voyage, message=message,is_read=False)
        return redirect('clients')
    return render(request,'index.html')

def deletenotif(request,id):
    notif = Notification.objects.get(id=id)
    notif.delete()
    return redirect("notification")

def mark_notifications_as_read(request, id):
    notif = Notification.objects.filter(id=id).first()

    if notif:
        notif.is_read = True
        notif.save()
    print(notif.is_read)
    return redirect("notification")



def toggle_favorite(request, voyage_id):
    voyage = Voyages.objects.get(id=voyage_id)
    user = request.user
    client = Client.objects.filter(user=user).first()
    favori = Favoris.objects.filter(client=client, voyage=voyage).first()

    if favori is not None:
        favori.delete()
        is_favorite = False
    else:
        Favoris.objects.create(client=client, voyage=voyage)
        is_favorite = True
    return redirect('favoris')

def favoris(request):
    user=request.user
    client = Client.objects.filter(user=user).first()
    unread_count = Notification.objects.filter(client=client, is_read=False).count()
    favoris=Favoris.objects.filter(client=client)
    context={'favoris':favoris,
             'notif':unread_count,
             'client':client}
    return render (request, "favoris.html",context)  

def deletefavoris(request,id):
    favoris=Favoris.objects.get(id=id)
    favoris.delete()
    return redirect('favoris')


def contacter(request):
    if request.method == 'POST':
        name=request.POST.get('contact_name')
        email=request.POST.get('contact_email')
        subject=request.POST.get('contact_subject')
        message=request.POST.get('contact_message')
        contact=Contact.objects.create(name=name,email=email,subject=subject,message=message)
    return redirect('index')
def contact(request):
    user = request.user
    admin = Administrator.objects.filter(user=user).first()
    contact=Contact.objects.all()
    notif=Contact.objects.filter(is_read=False).count()
    context={
        'contact':contact,
        'notif':notif,
        'admin':admin,
    }
    return render(request,'contact.html',context)
def mark__as_read(request, id):
    notif = Contact.objects.filter(id=id).first()

    if notif:
        notif.is_read = True
        notif.save()
    
    return redirect("contact")

def Deletecontact(request, id):
    client = Contact.objects.get(id=id)
    client.delete()
    return redirect("contact")
def com(request):
    user = request.user
    comment=Commentaire.objects.all()
    admin = Administrator.objects.filter(user=user).first()
    notif=Contact.objects.filter(is_read=False).count()
    context={
        'notif':notif,
        'admin':admin,
        "commentaire":comment
        
        }
    
    
    return  render(request,"comment.html",context)