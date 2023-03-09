import json

from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Message


@login_required
def room(request):
    messages = Message.objects.all()
    data = serializers.serialize("json", messages)

    context = {
        'messages': data,
    }
    return render(request, 'chat/room.html', context)
