# Generated by Django 4.2.14 on 2024-08-06 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0031_remove_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='result',
            field=models.TextField(default='Wait for response'),
        ),
    ]
