import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django import forms
from petplanet import models
from petplanet.utils.bootstrap import BootStrapForm,BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt


class PostModelForm(BootStrapModelForm):
    class Meta:
        model = models.Post
        fields = ['title','content']


class ImageModelForm(BootStrapModelForm):
    class Meta:
        model = models.Image
        fields = ['image']



def post_image_upload(request):
    nid = request.GET.get('nid')
    user = models.User.objects.filter(id=nid).first()
    form = ImageModelForm(data=request.POST,files=request.FILES)
    post_id = request.GET.get('pid')
    post = models.Post.objects.filter(id=post_id).first()

    if request.method == "GET":
        imageset = models.Image.objects.filter(post=post).all()
        if imageset:
            models.Post.objects.filter(id=post_id).update(has_image=True)
        return render(request, 'post_image.html',{'form':form,
                                                  'imageset': imageset,
                                                  'nid':nid,
                                                  'pid':post_id})
    
    if form.is_valid():
        img = form.save(commit=False)
        image = request.FILES.get("image")

        if image:
            img_path = "media/postImgs/"+image.name
            img_database_path = "postImgs/"+image.name
            f = open(img_path, mode='wb')
            for chunk in image.chunks():
                f.write(chunk)
            f.close()
        else:
            img_database_path = "postImgs/default.png"

        img.image = img_database_path
        img.caption = img_database_path
        img.post = post
        img.save()

        destination = f'/profile/posts/add/upload/?nid={nid}&pid={post_id}'
        return redirect(destination)
    

def image_delete(request):
    nid = request.GET.get('nid')
    post_id = request.GET.get('pid')
    image_id = request.GET.get('img')
    models.Image.objects.filter(id=image_id).delete()
    
    destination = f'/profile/posts/add/upload/?nid={nid}&pid={post_id}'
    return redirect(destination)
    

def post_add_with_img(request):
    nid = request.GET.get('nid')
    user = models.User.objects.filter(id=nid).first()
    pid = request.GET.get('pid')
    post = models.Post.objects.filter(id=pid).first()
    print(user)
    form = PostModelForm(data=request.POST, instance=post)

    if request.method == "GET":
        form = PostModelForm(instance=post)
        print(user)
        return render(request, 'post_add_imgs.html',{"form":form,'user':user})
    

    if form.is_valid():
        post_update = form.save(commit=False)
        post_update.is_active = True
        post_update.has_image = True
        post_update.save()
        return redirect("/community/mainpage/")
    
    print(form.errors)
    
    return render(request, "post_add_imgs.html",{"form":form,'user':user})
    

def post_add(request):
    nid = request.GET.get('nid')
    user = models.User.objects.filter(id=nid).first()
    print(user)
    form = PostModelForm(data=request.POST)
    if request.method == "GET":
        print(user)
        return render(request, 'post_add.html',{"form":form,'user':user})
    
    if form.is_valid():
        post = form.save(commit=False)
        post.author = user
        post.save()
        print("submit")
        destination = f'/profile/posts/add/upload/?nid={user.id}&pid={post.id}'
        return redirect(destination)
    
    print(form.errors)
    
    return render(request, "post_add.html")


def post_delete(request):
    nid = request.GET.get('nid')
    post = models.Post.objects.filter(id=nid).first()
    user = post.author.id
    print(user)
    models.Post.objects.filter(id=nid).delete()

    destination = f'/profile/?nid={user}'
    return redirect(destination)


def post_edit(request): 
    nid = request.GET.get('nid')
    post = models.Post.objects.filter(id=nid).first()
    user = post.author
    form = PostModelForm(data=request.POST, instance=post)
    if request.method == "GET":
        form = PostModelForm(instance=post)
        return render(request, 'post_add.html',{"form":form,'user':user})
    
    if form.is_valid():
        post.save()
        print("submit")
        destination = f'/profile/posts/add/upload/?nid={user.id}&pid={post.id}'
        return redirect(destination)
    
    print(form.errors)
    
    return render(request, "post_add.html")
