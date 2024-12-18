# Register your models here.
from chat.models import Event, Group, Message
from django.contrib import admin

admin.site.register(Message)
admin.site.register(Event)
admin.site.register(Group)
