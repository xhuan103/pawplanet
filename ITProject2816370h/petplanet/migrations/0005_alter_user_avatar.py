# Generated by Django 4.2.14 on 2024-07-17 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0004_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars/'),
        ),
    ]
