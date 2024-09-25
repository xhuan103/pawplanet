from django import forms
from petplanet import models
from petplanet.utils.bootstrap import BootStrapModelForm 


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length = 3,
        Label= "Username",
        widget=forms.TextInput(attrs={"class":"form-control"})
    )