from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.core.validators import validate_email
from django.contrib.auth import  login,logout

from Voyages.models import Voyages

from .models import CustomUser
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


from django.contrib.auth import get_user_model
def user_login(request):
    print("machi hadi")
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        print(f"Email: {email}, Password: {password}")

        user = CustomUser.objects.filter(email=email).first()
        if user:
            print(f"{user.email}")
            
            if (user.email==email and user.password==password):
                  return redirect('dashboard', user_id=user.id)
    
            else:
                print("Mot de passe incorrect ou Utilisateur n'existe pas")
        #pbkdf2_sha256$260000$keq2OquT6PYV0h6SINhEHP$Lr+NuycsOkaPJY2o1LLFfdMxltRMITvttd0Wk79ZYfI=

    return render(request, 'login.html', {'error': True, 'message': "Mot de passe incorrect ou Utilisateur n'existe pas!"})
    


def log_in(request):
    print("hadi")
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        print(f"Email: {email}, Password: {password}")

        user = CustomUser.objects.filter(email=email).first()
        if user:
            print(f"{user.email}")
            print(f"{user.password}")
            
            if (user.email==email and user.password==password):
                return redirect('dashboard', user_id=user.id)
    
            else:
                print("Mot de passe incorrect ou Utilisateur n'existe pas")
        

    return render(request, 'login.html', {'error': True, 'message': "Mot de passe incorrect ou Utilisateur n'existe pas!"})




def creer_client(request):
    if request.method == "POST":
        civilite = request.POST.get('civilite', None)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        ville = request.POST.get('ville', None)
        photo = request.FILES.get('image', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        date_naissance = request.POST.get('date_naissance', None)
        telephone = request.POST.get('telephone', None)

        try:
            validate_email(email)
        except:
            return render(request, 'register.html', {'error': True, 'message': 'Entrez un email valide !!!!!'})

        if password != repassword:
            return render(request, 'register.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        # Vérifiez si l'utilisateur existe déjà
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})

        user = CustomUser.objects.create_user(
            civilite=civilite,
            username=name,
            email=email,
            password=password,
            telephone=telephone,
            ville=ville,
            date_naissance=date_naissance,
        )
        user.photo = photo
        user.save()

        if user:
            return redirect('login')  # Rediriger vers la page de connexion
        else:
            return render(request, 'register.html', {'error': True, 'message': 'Failed to authenticate user'})

    return render(request, 'register.html', {'error': False, 'message': ''})
@login_required(login_url='login')
def dashboard(request,user_id):
    user = CustomUser.objects.get(id=user_id)
   
    print(f"Type de l'utilisateur : {type(user)}")  # Vérifiez le type de l'utilisateur dans la console
    return render(request, 'dashbord.html', {'user': user})




@login_required(login_url='signin')
def log_out(request):
    logout(request)
    return redirect('login')

# def update_password(request, token, uid):
    
#     try:
#         user_id = urlsafe_base64_decode(uid)
#         decode_uid = codecs.decode(user_id, 'utf-8')
#         user = User.objects.get(id=decode_uid)
#     except:
#         return HttpResponseForbidden("Vous n'aviez pas la permission de modifier ce mot de pass. Utilisateur introuvable")
    
#     check_token = default_token_generator.check_token(user, token)
   
#     if not check_token:
#         return HttpResponseForbidden("Vous n'aviez pas la permission de modifier ce mot de pass. Votre Token est invalid ou a espiré")
    
#     error = False
#     success = False
#     message = ""
#     if request.method == "POST":
#         password = request.POST.get("password")
#         repassword = request.POST.get("repassword")
#         print(password , repassword)
#         if repassword == password:
#             try:
#                 validate_password(password, user)
#                 user.set_password(password)
#                 user.save()
                
#                 success = True
#                 message = "votre mot de pass a été modifié avec succès!"
                
#             except ValidationError as e:
#                 error = True
#                 message = str(e)
#         else:
#             error = True
#             message = "Les deux mot de pass ne correspondent pas"
           
#     context = {
#         "error": error,
#         "success": success,
#         "message": message
#     }
    
   

#     return render(request, "update_password.html", context)



# def Panier(request):




# from django.contrib import messages
# from django.utils import timezone
# from datetime import timedelta

# def notify_clients_one_day_before(request):
#     # Récupérer tous les voyages qui ont une date de début dans un jour
#     one_day_before = timezone.now() + timedelta(days=1)
#     upcoming_voyages = Voyages.objects.filter(date_debut=one_day_before)

#     # Ajouter une notification pour chaque voyage à venir
#     for voyage in upcoming_voyages:
#         messages.success(request, f'Votre voyage pour {voyage.destination} commence dans un jour. Profitez de votre voyage!')
