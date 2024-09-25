# Generated by Django 4.2.14 on 2024-07-31 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0023_remove_party_updated_at_party_dog_limit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='dog_limit',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='party',
            name='dogs',
            field=models.ManyToManyField(blank=True, related_name='parties', to='petplanet.dog'),
        ),
        migrations.AlterField(
            model_name='party',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='party',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]