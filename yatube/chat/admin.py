from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['message', 'username', 'pub_date']


admin.site.register(Message, MessageAdmin)
