from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    password= models.CharField(max_length=64)
    nickname = models.CharField(max_length=32)
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(verbose_name="AccountCreateTime", default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(verbose_name="staff", default=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self):
        return self.username
    

    def isStaff(self):
        return self.is_staff
    

class Breed(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    
class Dog(models.Model):
    name = models.CharField(max_length=32)
    gender_choices = (
        (1, "Female"),
        (2, "Male")
        )
    gender = models.SmallIntegerField(choices=gender_choices)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    age_year = models.PositiveIntegerField(default=0)
    age_month = models.PositiveIntegerField(default=0)

    status_choices = (
        (1, "Yes"),
        (2, "No")
        )
    status = models.SmallIntegerField(choices=status_choices)
    avatar = models.ImageField(upload_to="dogAvatars/", blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    has_image = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    
class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='postImgs/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.post.title} with caption: {self.caption}"


class Party(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hold_at = models.DateField()
    hold_at_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    dog_limit = models.PositiveIntegerField(default=1)
    dogs = models.ManyToManyField(Dog, related_name='parties', blank=True)
    
    def __str__(self):
        return self.title
    

class PartyImage(models.Model):
    party = models.ForeignKey(Party, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='partyImgs/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.party.title} with caption: {self.caption}"
    

class Comment(models.Model):
    post_comment = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    party_comment = models.ForeignKey(Party, null=True, blank=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    

class Application(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    party_author = models.ForeignKey(User, related_name='party_author', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    dogs = models.ManyToManyField(Dog, related_name='application', blank=True)
    is_accept = models.BooleanField(blank=True, null=True)
    result = models.TextField(default="Wait for response")

    def __str__(self):
        return self.message

