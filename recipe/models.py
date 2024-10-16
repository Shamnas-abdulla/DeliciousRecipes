from django.db import models
from accounts.models import Account
from category.models import Category
from django.db.models import Avg


class Recipe(models.Model):
    VEGETARIAN = 'Veg'
    NON_VEGETARIAN = 'Non-Veg'
    PESCATARIAN = 'Pescatarian'
    RECIPE_TYPE_CHOICES = [
        (VEGETARIAN, 'Vegetarian'),
        (NON_VEGETARIAN, 'Non-Vegetarian'),
        (PESCATARIAN, 'Pescatarian'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    recipe_type = models.CharField(max_length=50, choices=RECIPE_TYPE_CHOICES)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipies/')
    cooking_time = models.PositiveIntegerField()
    servings = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def rating_avg(self):
        reviews = Rating.objects.filter(recipe=self).aggregate(average=Avg('rate'))  # Use 'rating' if it's the field in Rating model
        avg = 0
        if reviews['average'] is not None:
            avg = round(float(reviews['average']), 1)  # Round to one decimal place
        return avg

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Rating(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)