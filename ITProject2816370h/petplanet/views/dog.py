import os
from django.conf import settings
from django.shortcuts import render,redirect
from django import forms
from petplanet import models
from petplanet.utils.bootstrap import BootStrapForm,BootStrapModelForm

class DogModelForm(BootStrapModelForm):
    class Meta:
        model = models.Dog
        fields = ['avatar','name', 'gender','breed','age_year','age_month','status']
        # widgets = {
        #     'password': forms.PasswordInput(attrs={"class": "form-control", "placeholder": "password"})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'status': 
                field.label = "Has your pet been spayed or neutered?"
            elif name == 'age':
                field.label = "What type of breed is your pet?"
            elif name == 'name':
                field.label = "What's your pet's name?"
            elif name == 'avatar':
                field.label = "Upload a photo for your pet"
            else:
                field.widget.attrs.update({"class": "form-control", "placeholder": field.label})


def dogs(request):
    ownerId = request.GET.get('nid')
    owner = models.User.objects.filter(id=ownerId).first()
    dogset = models.Dog.objects.filter(owner=owner)
    form = DogModelForm(data=request.POST)

    if request.method == "GET":
        form = DogModelForm()

        context = {'current_page': 'Dogs',
               'form': form,
               'dogset':dogset,
               }

        return render(request, "profile/dog/dogs.html", context)
    

    if form.is_valid():
        dog = form.save(commit=False)
        image = request.FILES.get("avatar")

        if image:
            avatar_path = "media/dogAvatars/"+image.name
            avatar_database_path = "dogAvatars/"+image.name
            f = open(avatar_path, mode='wb')
            for chunk in image.chunks():
                f.write(chunk)
            f.close()
        else:
            avatar_database_path = "dogAvatars/default.png"

        dog.avatar = avatar_database_path
        dog.owner = owner
        dog.save()
        destination = '/profile/dogs/?nid='+ownerId
        return redirect(destination)
    
    context = {'current_page': 'Dogs',
               'form': form,
               'dogset':dogset,
               }
    
    return render(request, "profile/dog/dogs.html", context)


def edit(request):
    dogId = request.GET.get('nid')
    oid = request.GET.get('oid')
    dog = models.Dog.objects.filter(id=dogId).first()
    if request.method == "GET":
        form = DogModelForm(instance=dog)
        return render(request, 'profile/dog/dogs_edit.html',{"form":form})
    
    form = DogModelForm(data=request.POST, instance=dog)
    if form.is_valid():
        form.save()
        destination = f'/profile/dogs/?nid={oid}'
        return redirect(destination)

    return render(request, "profile/dog/dogs_edit.html",{"form":form})


def delete(request):
    dogId = request.GET.get('nid')
    dog = models.Dog.objects.filter(id=dogId).first()
    oid = dog.owner.id
    dog.delete()
    context = {'current_page': 'Dogs',
               }
    destination = f'/profile/dogs/?nid={oid}'
    return redirect(destination)