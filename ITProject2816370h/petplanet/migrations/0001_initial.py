# Generated by Django 4.2.14 on 2024-07-17 11:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='AccountCreateTime')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('location', models.SmallIntegerField(choices=[(1, 'Glasgow City Centre'), (2, 'West End'), (3, 'Southside'), (4, 'East End'), (5, 'North Glasgow'), (6, 'Prefer not to say')])),
            ],
        ),
    ]
