"""ITProject2816370h URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from petplanet.views import _init_,community,profile,dog,post,party,application
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}, name='media'),

    path('admin/', admin.site.urls),
    path('', _init_.homepage),
    path('about/', _init_.about),
    path('login/', _init_.login),
    path('signup/', _init_.signup),
    path('logout/', _init_.logout),

    path('community/mainpage/', community.mainpage),
    path('community/post/', community.post),

    path('community/party/', party.party_main),
    path('community/party/add/form/', party.party_add_form),
    path('community/party/add/img/', party.party_add_img),
    path('community/party/delete/img/', party.party_delete_img),
    path('community/party/add/location/', party.party_add_location),
    path('community/party/add/dog/', party.party_add_dog),
    path('community/party/detail/', party.party_detail),
    path('community/party/application/', party.party_application),
    path('community/party/map/', party.party_map),
    path('profile/party/edit/', party.party_edit),
    path('profile/party/delete/', party.party_delete),

    path('profile/', profile.profile),
    path('profile/party/', profile.profile_party),
    path('profile/message/', profile.message),
    path('profile/setting/', profile.setting),
    path('profile/setting/avatar/', profile.change_avatar),
    path('profile/application/delete/', profile.application_delete),

    path('profile/application/accept/', application.accept_application),
    path('profile/application/reject/', application.reject_application),

    path('profile/dogs/', dog.dogs),
    path('profile/dogs/edit/', dog.edit),
    path('profile/dogs/delete/', dog.delete),

    path('profile/posts/add/upload/', post.post_image_upload),
    path('profile/posts/add/image/', post.post_add_with_img),
    path('profile/posts/delete/image/', post.image_delete),
    path('profile/posts/add/', post.post_add),
    path('profile/posts/edit/', post.post_edit),
    path('profile/posts/delete/', post.post_delete),
    

]

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
