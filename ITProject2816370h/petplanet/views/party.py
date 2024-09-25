import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django import forms
from petplanet import models
from petplanet.utils.bootstrap import BootStrapForm,BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import OuterRef, Subquery



def party_main(request):
    partyset = models.Party.objects.all()
    subquery = models.PartyImage.objects.filter(party=OuterRef('pk')).values('pk')[:1]
    party_with_one_image = models.Party.objects.annotate(image_id=Subquery(subquery))
    images = models.PartyImage.objects.filter(pk__in=party_with_one_image.values('image_id'))
    for image in images:
        print(image)

    context = {'parties': partyset,
               'imageset': images}

    return render(request, "party/party_main.html", context)


def party_map(request):
    partyset = models.Party.objects.all()
    context = {'partyset': partyset}

    return render(request, "party/party_on_map.html", context)


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields=["content"]


class ApplicationModelForm(forms.ModelForm):
    dogs = forms.ModelMultipleChoiceField(
        queryset=models.Dog.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    

    class Meta:
        model = models.Application
        fields=["message","dogs"]


    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super(ApplicationModelForm, self).__init__(*args, **kwargs)
        if owner:
            self.fields['dogs'].queryset = models.Dog.objects.filter(owner=owner)


@csrf_exempt
def party_detail(request):
    party_id = request.GET.get('nid')
    party = models.Party.objects.filter(id=party_id).first()
    imageset = models.PartyImage.objects.filter(party=party).all()
    author_id = request.GET.get('oid')
    author = models.User.objects.filter(id=author_id).first()
    session_user_id = request.session['info'].get('id')
    session_user = models.User.objects.filter(id=session_user_id).first()
    application = ApplicationModelForm(owner=session_user)
    print(request.session['info'])
    if request.method == "GET":
        form = CommentModelForm()
        print(request.session['info'])
        commentset =  models.Comment.objects.filter(party_comment=party).all().order_by("-id")
        context={
            'party': party,
            'imageset': imageset,
            'form': form,
            'commentset': commentset,
            'application': application
        }
        return render(request, "party/party_detail.html", context)
    
    form = CommentModelForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.party_comment = party
        comment.author = author
        comment.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    
    return render(request, "party/party_detail.html", context)


class PartyModelForm(forms.ModelForm):
    class Meta:
        model = models.Party
        fields=["title","content","hold_at","hold_at_time","dog_limit"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'title': 
                field.label = "Party Theme"
            elif name == 'content':
                field.label = "Describe your party"
            elif name == 'hold_at':
                field.label = "When is the party date?"
            elif name == 'hold_at_time':
                field.label = "When is the party start?"
            elif name == 'dog_limits':
                field.label = "How many dogs allowed to attend your party?"
            else:
                field.widget.attrs.update({"class": "form-control", "placeholder": field.label})


def party_add_form(request):
    ownerId = request.GET.get('nid')
    owner = models.User.objects.filter(id=ownerId).first()
    form = PartyModelForm(data=request.POST)

    if request.method == "GET":
        form = PartyModelForm()
        return render(request, 'party/party_add_form.html',{"form":form})
    
    if form.is_valid():
        party = form.save(commit=False)
        party.author = owner
        party.save()
        party_id = party.id
        destination = f'/community/party/add/location/?pid={party_id}'
        return redirect(destination)
    
    print(form.errors)

    context = {}
    return render(request, "party/party_add_form.html", context)

def party_edit(request): 
    nid = request.GET.get('nid')
    party = models.Party.objects.filter(id=nid).first()
    form = PartyModelForm(data=request.POST, instance=party)
    if request.method == "GET":
        form = PartyModelForm(instance=party)
        return render(request, 'party/party_add_form.html',{"form":form})
    
    if form.is_valid():
        party = form.save(commit=False)
        party.save()
        party_id = party.id
        destination = f'/community/party/add/location/?pid={party_id}'
        return redirect(destination)
    
    print(form.errors)

    context = {}
    return render(request, "party/party_add_form.html", context)


class ImageModelForm(BootStrapModelForm):
    class Meta:
        model = models.PartyImage
        fields = ['image']


def party_add_img(request):
    party_id = request.GET.get('pid')
    party = models.Party.objects.filter(id=party_id).first()
    imageset = models.PartyImage.objects.filter(party=party_id).all()
    form = ImageModelForm(data=request.POST,files=request.FILES)
    if request.method == "GET":
        context = {
        "imageset":imageset,
        'pid':party_id,
        'form':form
        }
        return render(request, "party/party_add_img.html", context)
    
    if form.is_valid():
        img = form.save(commit=False)
        image = request.FILES.get("image")

        if image:
            img_path = "media/partyImgs/"+image.name
            img_database_path = "partyImgs/"+image.name
            f = open(img_path, mode='wb')
            for chunk in image.chunks():
                f.write(chunk)
            f.close()
        else:
            img_database_path = "partyImgs/default.png"

        img.image = img_database_path
        img.caption = img_database_path
        img.party = party
        img.save()

        destination = f'/community/party/add/img/?pid={party_id}'
        return redirect(destination)
    

    context = {
        "imageset":imageset,
        'pid':party_id
        }
    return render(request, "party/party_add_img.html", context)


def party_delete_img(request):
    party_id = request.GET.get('pid')
    image_id = request.GET.get('img')
    models.PartyImage.objects.filter(id=image_id).delete()
    
    destination = f'/community/party/add/img/?pid={party_id}'
    return redirect(destination)


@csrf_exempt
def party_add_location(request):
    party_id = request.GET.get('pid')
    party = models.Party.objects.filter(id=party_id).first()

    if request.method == "GET":
        context = {
            'party': party
        }
        return render(request, "party/party_add_location.html",context)
    
    loacation = request.POST

    pid = loacation.get('partyId')
    party_update = models.Party.objects.filter(id=pid).first()
    latitude = float(loacation.get('lat'))
    longitude = float(loacation.get('lng'))
    party_update.latitude = latitude
    party_update.longitude = longitude
    party_update.save()
    data_dict = {"status": True}
    return HttpResponse(json.dumps(data_dict))


class DogSelectionForm(forms.Form):
    dogs = forms.ModelMultipleChoiceField(
        queryset=models.Dog.objects.none(), 
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super(DogSelectionForm, self).__init__(*args, **kwargs)
        if owner:
            self.fields['dogs'].queryset = models.Dog.objects.filter(owner=owner)


def party_add_dog(request):
    party_id = request.GET.get('pid')
    party = models.Party.objects.filter(id=party_id).first()
    author = party.author
    print(author)

    if request.method == "GET":
        form = DogSelectionForm(owner=author)
        context = {
            'form': form,
            'party': party
        }
        return render(request, "party/party_add_dog.html", context)
    
    form = DogSelectionForm(request.POST, owner=author)
    if form.is_valid():
        selected_dogs = form.cleaned_data['dogs']
        party.dogs.set(selected_dogs)
        return redirect('/community/party/', party_id=party.id)

    print(form.errors)
    context = {

    }
    return redirect('/community/party/', party_id=party.id)

def party_delete(request):
    nid = request.GET.get('nid')
    party = models.Party.objects.filter(id=nid).first()
    user = party.author.id
    print(user)
    models.Party.objects.filter(id=nid).delete()

    destination = f'/profile/party/?nid={user}'
    return redirect(destination)


@csrf_exempt
def party_application(request):
    party_id = request.GET.get('nid')
    party = models.Party.objects.filter(id=party_id).first()
    user_id = request.GET.get('oid')
    user = models.User.objects.filter(id=user_id).first()
    form = ApplicationModelForm(data=request.POST)
    if form.is_valid():
        selected_dogs = form.cleaned_data['dogs']
        application = form.save(commit=False)
        application.party = party
        application.party_author = party.author
        application.owner = user
        application.save()
        application.dogs.set(selected_dogs)  
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    
