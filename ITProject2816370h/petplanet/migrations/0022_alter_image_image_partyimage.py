# Generated by Django 4.2.14 on 2024-07-29 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petplanet', '0021_remove_party_has_image_party_dogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='postImgs/'),
        ),
        migrations.CreateModel(
            name='PartyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='partyImgs/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='petplanet.party')),
            ],
        ),
    ]
