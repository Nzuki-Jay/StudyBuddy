from django.contrib import admin
from .models import Room, Topic, Message, UserProfile, Reply

# Register your models here.
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(UserProfile)
admin.site.register(Reply)
