# Generated by Django 4.2.14 on 2024-07-19 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0008_alter_breed_id_alter_dog_id_alter_dog_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='avatar',
            field=models.ImageField(blank=True, default='default.png', upload_to='dogAvatars/'),
        ),
    ]