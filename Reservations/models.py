from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from Voyages.models import Voyages

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'other_required_fields', ...]
    civilite = models.CharField(max_length=20, choices=[('Monsieur', 'Monsieur'), ('Madame', 'Madame'), ('Mademoiselle', 'Mademoiselle')])
    telephone = models.CharField(max_length=15)
    ville=models.CharField(max_length=15)
    date_naissance = models.DateField(null=True, blank=True)
    photo = models.ImageField()
    #is_client = models.BooleanField(default=True)
    #is_administrateur = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username
    
# class Client(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
#     image = models.ImageField(upload_to='Client_images', null=True, blank=True)
#     phone_number = models.CharField(max_length=20, null=True, blank=True)
#     address = models.CharField(max_length=200, null=True, blank=True)
#     update = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     objects = models.Manager()


    def calculer_age(self):
        if self.date_naissance:
            birth_year = self.date_naissance.year
            current_year = datetime.now().year
            age = current_year - birth_year
            print(age)
            return age
        else:
            return None  
        
