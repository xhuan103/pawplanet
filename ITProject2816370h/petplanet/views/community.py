import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django import forms
from petplanet import models
from petplanet.utils.bootstrap import BootStrapForm,BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import OuterRef, Subquery

def mainpage(request):
    partyset = models.Party.objects.all()
    subquery_party = models.PartyImage.objects.filter(party=OuterRef('pk')).values('pk')[:1]
    party_with_one_image = models.Party.objects.annotate(image_id=Subquery(subquery_party))
    images_party = models.PartyImage.objects.filter(pk__in=party_with_one_image.values('image_id'))



    postset = models.Post.objects.all().order_by("-updated_at")
    subquery = models.Image.objects.filter(post=OuterRef('pk')).values('pk')[:1]
    posts_with_one_image = models.Post.objects.annotate(image_id=Subquery(subquery))
    images = models.Image.objects.filter(pk__in=posts_with_one_image.values('image_id'))
    for image in images:
        print(image)

    context = {'posts': postset,
               'imageset': images,
               'partyset': partyset,
               'images_party': images_party
               }

    return render(request, "mainpage.html", context)


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields=["content"]
      

@csrf_exempt
def post(request):
    id = request.GET.get('nid')
    post = models.Post.objects.filter(id=id).first()
    imageset = models.Image.objects.filter(post=post).all()
    author_id = request.GET.get('oid')
    author = models.User.objects.filter(id=author_id).first()
    if request.method == "GET":
        form = CommentModelForm()
        commentset =  models.Comment.objects.filter(post_comment=post).all().order_by("-id")
        context = {'post': post,
               'imageset': imageset,
               'form':form,
               'commentset': commentset}
        return render(request, "post.html", context)
    
    print(request.POST)
  
    form = CommentModelForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post_comment = post
        comment.author = author
        comment.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status":False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

 