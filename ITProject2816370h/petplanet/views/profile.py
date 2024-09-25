import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django import forms
from petplanet import models
from petplanet.utils.bootstrap import BootStrapForm,BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt


def profile(request):
    ownerid = request.GET.get('nid')
    owner = models.User.objects.filter(id=ownerid).first()
    dogset = models.Dog.objects.filter(owner=owner).all()
    postset = models.Post.objects.filter(author=owner).all()
    print(postset)

    context = {'current_page': 'Posts',
               'dogs': dogset,
               'posts': postset,
               'user': owner}

    return render(request, "profile/profile.html", context)


def profile_party(request):
    user_id = request.session['info'].get('id')
    user= models.User.objects.filter(id=user_id).first()
    partyset = models.Party.objects.filter(author=user).all()

    context = {
        'current_page': 'Parties',
        'party_set': partyset
    }
    return render(request, "profile/profile_party.html",context)



def message(request):
    user_id = request.session['info'].get('id')
    user= models.User.objects.filter(id=user_id).first()
    application_set = models.Application.objects.filter(owner=user).all()
    message_set = models.Application.objects.filter(party_author=user).all()
    context = {
        'current_page': 'Message',
        'application_set': application_set,
        'message_set': message_set
    }
    return render(request, 'profile/profile_message.html',context)


def application_delete(request):
    nid = request.GET.get('nid')
    application = models.Application.objects.filter(id=nid).first()
    user = application.party_author.id
    print(user)
    application.delete()

    destination = '/profile/message/'
    return redirect(destination)


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields=["nickname","email"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class":"form-control", "placeholder":field.label}
            

def setting(request):
    # get nid
    nid = request.GET.get('nid')
    print(nid)
    user = models.User.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelForm(instance=user)
        context = {'current_page': 'Setting',
                   'user':user,
                    "form":form}
        return render(request, 'profile/setting.html',context)
    
    form = UserModelForm(data=request.POST, instance=user)
    
    if form.is_valid():
        form.save()
        context = {'current_page': 'Setting',
                   'user':user,
               "form":form}
        return render(request, 'profile/setting.html',context)

    context = {'current_page': 'Setting',
               'user':user,
               "form":form}

    return render(request, "profile/setting.html", context)


@csrf_exempt
def change_avatar(request):
    oid = request.GET.get('oid')
    print(oid)
    user = models.User.objects.filter(id=oid).first()
    image = request.FILES['file']
    print(image)
    img_path = "media/avatars/"+image.name
    img_database_path = "avatars/"+image.name
    f = open(img_path, mode='wb')
    for chunk in image.chunks():
        f.write(chunk)
    f.close()

    user.avatar = img_database_path
    user.save()

    data_dict = {"status": True}
    return HttpResponse(json.dumps(data_dict))
    return render(request, "profile/setting.html", context)
