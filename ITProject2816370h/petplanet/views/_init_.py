from django.shortcuts import render,redirect
from django import forms
from petplanet import models
from petplanet.utils.bootstrap import BootStrapForm,BootStrapModelForm

# Create your views here.
def homepage(request):
    return render(request, "public/homepage.html")


def about(request):
    return render(request, "public/about.html")


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class':"form-control"}),
        required=True
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':"form-control"}),
        required=True
    )


def login(request):
    if request.session.get('info'):
        return redirect("/community/mainpage/") 

    if request.method == "GET":
        form = LoginForm()
        return render(request, "public/login.html", {'form':form})
    
    form = LoginForm(data=request.POST)
    
    if form.is_valid():
        admin_object = models.User.objects.filter(**form.cleaned_data).first()
        if admin_object is None:
            form.add_error("password","error")
            return render(request, "public/login.html", {'form':form})
        
        request.session["info"] = {'id':admin_object.id,'name':admin_object.nickname,'avatar':admin_object.avatar.url}
        return redirect("/community/mainpage/") 
    
    return render(request, "public/login.html", {'form':form})


class SignupModelForm(BootStrapModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'password','nickname','email']
        widgets = {
            'password': forms.PasswordInput(attrs={"class": "form-control", "placeholder": "password"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'password': 
                field.widget.attrs.update({"class": "form-control", "placeholder": field.label})


def signup(request):
    if request.method == "GET":
        form = SignupModelForm()
        return render(request, 'public/signup.html', {'form': form})
    
    form = SignupModelForm(data=request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.avatar = 'avatars/default.png'
        user.save()
        return redirect('/login/')
    
    print(form.errors)
    
    return render(request, "public/signup.html",{"form": form})

def logout(request):
    request.session.clear()
    return redirect('/login/')