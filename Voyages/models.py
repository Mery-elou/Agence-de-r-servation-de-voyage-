from django.db import models

# Create your models here.
from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='siteWEB', null=True, blank=True)

class Voyages(models.Model):
    CATEGORIES_CHOICES = [
        ('cat1', 'Couples'),
        ('cat2', ' Familles'),
        ('cat3', ' Equipes'),
        ('cat4', 'Haj & Omra ')
        # Ajoutez d'autres catégories si nécessaire
    ]

    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255)
    description = HTMLField('Description')
    programme=HTMLField('Programme')
    info_pratique=HTMLField('Info_pratique')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_depart = models.DateField()
    date_arrive = models.DateField()
    destination = models.CharField(max_length=255)
    photos = models.ManyToManyField(Image)
    categories = models.CharField(max_length=50, choices=CATEGORIES_CHOICES)
    nombre_de_places = models.PositiveIntegerField()
    nombre_de_places_adultes = models.PositiveIntegerField()
    nombre_de_places_enfants = models.PositiveIntegerField()
    nombre_de_pieces = models.PositiveIntegerField()
    promotions = models.BooleanField(default=False)
    hotel = models.ForeignKey('Hotel', on_delete=models.SET_NULL, null=True, blank=True)
    isthebest_destination = models.BooleanField(default=False)
   
    def __str__(self):
        return self.titre

class Hotel(models.Model):
    choices=[('repas1', 'Petit déjeuner'), 
             ('repas2', 'Déjeuner'),
             ('repas3', 'Dîner')]
    
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    site_web = models.URLField()
    repas = models.CharField(max_length=20, choices=choices)
    photos = models.ManyToManyField(Image)
    num_chambre = models.PositiveIntegerField()

    def __str__(self):
        return self.nom

    
class Promotion(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2)
    date_debut = models.DateField()
    date_fin = models.DateField()
    voyage = models.ForeignKey(Voyages, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.voyage.titre}"
    
