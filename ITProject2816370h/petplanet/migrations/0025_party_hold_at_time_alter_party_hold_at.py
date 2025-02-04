# Generated by Django 4.2.14 on 2024-07-31 20:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0024_alter_party_dog_limit_alter_party_dogs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='hold_at_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='party',
            name='hold_at',
            field=models.DateField(),
        ),
    ]
