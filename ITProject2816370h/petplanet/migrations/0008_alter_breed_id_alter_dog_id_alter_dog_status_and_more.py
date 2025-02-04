# Generated by Django 4.2.14 on 2024-07-19 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0007_dog_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breed',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Yes'), (2, 'No')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
