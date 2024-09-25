import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django import forms
from petplanet import models
from petplanet.utils.bootstrap import BootStrapForm,BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import OuterRef, Subquery

def accept_application(request):
    application_id = request.GET.get('nid')
    application = models.Application.objects.filter(id=application_id).first()
    party = application.party
    dogs_on_party = party.dogs.all()
    dogs = application.dogs.all()
    for dog in dogs:
        if dog not in dogs_on_party:
            party.dogs.add(dog)
    party.save()
    application.is_accept = True
    application.save()

    destination = '/profile/message/'
    return redirect(destination)


def reject_application(request):
    application_id = request.GET.get('nid')
    reason = request.GET.get('reason')
    application = models.Application.objects.filter(id=application_id).first()
    application.result = reason
    application.is_accept = False
    application.save()

    destination = '/profile/message/'
    return redirect(destination)
