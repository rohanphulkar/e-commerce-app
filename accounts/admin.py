from django.contrib import admin
from .models import User,Address
from django.contrib.sessions.models import Session
# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Session)



