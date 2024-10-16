from django.shortcuts import render
from recipe.models import Recipe, Category

# Create your views here.

def category_filter(request,category_name):
    recipies = Recipe.objects.filter(category__category_name=category_name)
    categories = Category.objects.all()
    context = {
        'recipies': recipies,
        'categories':categories,
    }
    return render(request, 'recipe/recipe_list.html', context)
    
