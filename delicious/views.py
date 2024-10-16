from django.shortcuts import render
from recipe.models import Recipe
from category.models import Category
from django.db.models import Avg, Count



def home(request):
    categories = Category.objects.all()
    recipe = Recipe.objects.all()
    top_recipies = recipe.annotate(avg_rating=Avg('rating__rate')).order_by('-avg_rating')[:6]
    new_recipies = recipe.annotate(comment_count=Count('comment')).order_by('-created_at')[:9]
    hero_slides = recipe.annotate(avg_rating=Avg('rating__rate')).order_by('-avg_rating')[:3]
    context = {
        'categories':categories,
        'top_recipies':top_recipies,
        'new_recipies':new_recipies,
        'hero_slides':hero_slides,
    }


    return render(request,'index.html', context)


def about(request):
    return render(request, 'about.html')


def gluten_free(request):
    return render(request, 'gluten_free.html')

