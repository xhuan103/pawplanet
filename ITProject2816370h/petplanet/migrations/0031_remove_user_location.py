# Generated by Django 4.2.14 on 2024-08-03 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0030_application_party_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
    ]
