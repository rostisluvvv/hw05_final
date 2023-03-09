import json

from django.core import serializers
from django.shortcuts import render

from .models import Message


def room(request):
    messages = Message.objects.all()
    data = serializers.serialize("json", messages)

    context = {
        'messages': data,
    }
    return render(request, 'chat/room.html', context)
