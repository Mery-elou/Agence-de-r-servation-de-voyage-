
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models import Q



# Create your views here.
# views.py
def CreerComte(request):
    error = False
    message = ""
    if request.method == "POST":
        Civilite=request.POST.get('Civilite', None)
        name = request.POST.get('name', None)
        prenon=request.POST.get('prenon', None)
        email = request.POST.get('email', None)
        ville=request.POST.get('ville', None)
        image=request.POST.get('image', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        
        # Email
        try:
            validate_email(email)
        except:
            error = True
            message = "Enter un email valide !!!!!"
        # password
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mot de passe ne correspondent pas!"
            else:
                # password length validation
                if len(password) < 8:
                    error = True
                    message = "Le mot de passe doit avoir au moins 8 caractères !!!!"
        
        # Exist
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {name} exist déjà'!"
        
        # register
        if error == False:
            user = User(
                username = name,
                email = email,
            )
            user.save()

            user.password = password
            user.set_password(user.password)
            user.save()

            return redirect('login')

            #print("=="*5, " NEW POST: ",name,email, password, repassword, "=="*5)

    context = {
        'error':error,
        'message':message
    }
    return render(request, 'register.html', context)
