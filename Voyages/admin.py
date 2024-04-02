from django.contrib import admin

# Register your models here.
from .models import Voyages
from .models import Image
from .models import Hotel
from .models import Promotion
admin.site.register(Voyages)
admin.site.register(Image)
admin.site.register(Hotel)
admin.site.register(Promotion)