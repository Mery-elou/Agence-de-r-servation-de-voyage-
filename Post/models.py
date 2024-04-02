from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField('Content')
    Image = models.ImageField()
    is_the_best= models.BooleanField(default=False) 
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True
    )
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.title

    # Autres méthodes du modèle...
