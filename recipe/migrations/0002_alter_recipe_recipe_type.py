# Generated by Django 5.1.1 on 2024-10-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_type',
            field=models.CharField(choices=[('Veg', 'Vegetarian'), ('Non-Veg', 'Non-Vegetarian'), ('Pescatarian', 'Pescatarian')], max_length=50),
        ),
    ]
