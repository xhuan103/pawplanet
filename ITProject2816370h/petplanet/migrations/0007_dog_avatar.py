# Generated by Django 4.2.14 on 2024-07-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0006_breed_dog'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='dogAvatars/'),
        ),
    ]
