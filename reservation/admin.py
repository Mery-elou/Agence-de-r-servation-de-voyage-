from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Administrator)
admin.site.register(Reservation)
admin.site.register(Notification)
admin.site.register(Cart)

# Register your models here.
