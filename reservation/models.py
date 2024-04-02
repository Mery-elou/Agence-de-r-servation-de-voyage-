from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, User, Group, Permission
from Voyages.models import Voyages
# Create your models here.
class User(AbstractUser):
    is_client = models.BooleanField(default=True)
    is_administrateur = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='reservation_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='reservation_user_permissions')
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='dashboard')
    image = models.ImageField(upload_to='Client_images', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    def calculerAge(self):
        if self.date_naissance:
            birth_year = self.date_naissance.year
            current_year = datetime.now().year
            age = current_year - birth_year
            print(age)
            return age
        else:
            return None  
    def __str__(self):
        return "Client Name :"+self.user.first_name
    
class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='dashboard_admin')
    image = models.ImageField(upload_to='administrator/profile', default='Default/user.png')

    objects = models.Manager()

    def __str__(self):
        return "Administrator Name : " + self.user.first_name
    
# class Notification(models.Model):
#     Voyage = models.ForeignKey(Voyages, on_delete=models.CASCADE, null=True, blank=True)
#     Administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE, null=True, blank=True)
#     message = models.TextField()
#     date = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     objects = models.Manager()
    
class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,  null=True)  # Replace '1' with the appropriate default client ID
    voyage = models.ForeignKey(Voyages, on_delete=models.CASCADE)
    adult = models.PositiveIntegerField(default=1)
    enfants = models.PositiveIntegerField(default=0)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('en_attente', 'En Attente'), ('passe', 'Passé')])
    objects = models.Manager()
    
class Cart(models.Model):
   client = models.ForeignKey(Client, on_delete=models.CASCADE,  null=True)  # Replace '1' with the appropriate default client ID
   voyage = models.ForeignKey(Voyages, on_delete=models.CASCADE)
   adult = models.PositiveIntegerField(default=1)
   enfants = models.PositiveIntegerField(default=0)
   prix = models.DecimalField(max_digits=10, decimal_places=2)
   
class Notification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,  null=True)
    date = models.DateTimeField(auto_now_add=True)
    voyage = models.ForeignKey(Voyages, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)    

class Favoris(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,  null=True)
    voyage = models.ForeignKey(Voyages, on_delete=models.CASCADE, blank=True, null=True)

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name} - {self.date}'
   
   
class Commentaire(models.Model):
    name = models.CharField(max_length=255)
    message = models.CharField(max_length=255)