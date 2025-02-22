# Generated by Django 5.1.1 on 2024-10-08 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
