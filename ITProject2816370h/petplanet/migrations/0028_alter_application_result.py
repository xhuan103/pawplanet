# Generated by Django 4.2.14 on 2024-08-01 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0027_alter_application_is_accept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='result',
            field=models.TextField(blank=True),
        ),
    ]
