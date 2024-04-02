# models.py

from django.db import models

class Client(models.Model):
    CIVILITE_CHOICES = [
        ('M', 'Monsieur'),
        ('Mme', 'Madame'),
        ('Autre', 'Autre'),
    ]

   

    nom = models.CharField(max_length=100)
    civilite = models.CharField(max_length=10, choices=CIVILITE_CHOICES)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)  # Vous pouvez utiliser un champ de mot de passe sécurisé
    ville = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='mysite\templates\static\img', null=True, blank=True)
    # Ajoutez d'autres champs du client selon vos besoins

    def __str__(self):
        return f"{self.prenom} {self.nom}"
