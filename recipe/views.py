from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RecipeForm
from .models import Recipe, Comment, Rating, FavoriteRecipe
from django.contrib import messages,auth
from django.http import Http404
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from category.models import Category

# Create your views here.

@login_required(login_url='login')
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.ingredients = request.POST.get('ingredients')  
            recipe.save()       
            messages.success(request, 'Your recipe has been saved successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors below.')
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
    }
    return render(request, 'recipe/create_recipe.html', context)


def recipe_list(request):
    # if request.user.is_authenticated:
    #     user = request.user
    #     recipies = Recipe.objects.exclude(user=user).annotate(comment_count=Count('comment')).order_by('-created_at')
    # else:
    #     recipies = Recipe.objects.annotate(comment_count=Count('comment')).order_by('-created_at')
    recipies = Recipe.objects.annotate(comment_count=Count('comment')).order_by('-created_at')
    categories = Category.objects.all()
    context = {
        'recipies':recipies,
        'categories':categories,
    }
    return render(request,'recipe/recipe_list.html',context)


@login_required(login_url='login')
def recipe_detail(request, rec_id):
    user_rating = Rating.objects.filter(user=request.user,recipe_id=rec_id).first()
    favorite = FavoriteRecipe.objects.filter(user=request.user,recipe=rec_id).exists()
    try:
        recipe = Recipe.objects.get(id=rec_id)
        instr_list = recipe.instructions.split(',')
        ingr_list = recipe.ingredients.split(',')
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")
    comments = Comment.objects.filter(recipe_id=rec_id).all()
    comment_count = comments.count()
    
    context = {
        "recipe": recipe,
        'instr_list':instr_list,
        'ingr_list':ingr_list,
        'comments':comments,
        'user_rating':user_rating,
        'favorite':favorite,
        'comment_count':comment_count,
    }
    return render(request, 'recipe/recipe_detail.html', context)


@login_required(login_url='login')
def comment_save(request, rec_id):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        if not content:
            messages.error(request, 'Content cannot be null')
            return redirect('recipe_detail', rec_id=rec_id)

        is_commented = Comment.objects.filter(user=request.user, recipe_id=rec_id).exists()

        if is_commented:
            Comment.objects.filter(user=request.user, recipe_id=rec_id).update(
                subject=subject,
                content=content
            )
        else:
            Comment.objects.create(
                user=request.user,
                recipe_id=rec_id,
                subject=subject,
                content=content
            )
        
        return redirect('recipe_detail', rec_id=rec_id)
    return redirect('recipe_detail', rec_id=rec_id)

from django.http import HttpResponse

from django.shortcuts import render
from .models import Rating  # Assuming Rating model is imported
from django.shortcuts import render, get_object_or_404


@login_required(login_url='login')
def rating(request, rec_id):
    recipe = get_object_or_404(Recipe, id=rec_id)
    comments = Comment.objects.filter(recipe_id=rec_id).all()
    instr_list = recipe.instructions.split(',')
    ingr_list = recipe.ingredients.split(',')
    user_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()  # Get the user's rating
    favorite = FavoriteRecipe.objects.filter(user=request.user,recipe=rec_id)
    

    if request.method == 'POST':
        rating_value = request.POST.get('rating')

        if user_rating:
            # Update the existing rating
            user_rating.rate = rating_value
            user_rating.save()
        else:
            # Create a new rating
            Rating.objects.create(user=request.user, recipe=recipe, rate=rating_value)

        return redirect('recipe_detail', rec_id=rec_id)  # Redirect to the same page to show updated rating

    # Context for GET requests
    context = {
        'recipe': recipe,
        'comments': comments,
        'instr_list': instr_list,
        'ingr_list': ingr_list,
        'user_rating': user_rating,
        'favorite':favorite,
    }
    return render(request, 'recipe/recipe_detail.html', context)


def filter_recipe(request):
    recipies = Recipe.objects.all()
    recipies=recipies.annotate(comment_count=Count('comment')).all()
    categories = Category.objects.all()

    if request.method == 'GET':
        recipe_type = request.GET.get('filter_recipe_type')
        recipe_cat = request.GET.get('filter_category').lower()
        most_rated = request.GET.get('most_rated')
        

        # Apply filters based on the user's selections
        if recipe_type:  # If user selected a recipe type, filter by it
            recipies = recipies.annotate(comment_count=Count('comment')).filter(recipe_type=recipe_type)

        if recipe_cat:  # If user selected a category, filter by it
            recipies = recipies.annotate(comment_count=Count('comment')).filter(category__slug=recipe_cat)

        if most_rated == 'true':  # If user checked 'Most Rated', order by the average rating
            # recipies = Recipe.objects.annotate(comment_count=Count('comment')).order_by('-created_at')
            recipies = recipies.annotate(avg_rating=Avg('rating__rate'),comment_count=Count('comment')).order_by('-avg_rating')
    context = {'recipies': recipies, 
               'categories':categories,}    
    return render(request, 'recipe/recipe_list.html', context)


@login_required(login_url='login')
def save_recipe(request, rec_id):
    favorite = FavoriteRecipe.objects.filter(user=request.user,recipe=rec_id)
    if favorite.exists():
        favorite.delete()
    else:
        FavoriteRecipe.objects.create(user=request.user, recipe_id=rec_id)

    return redirect('recipe_detail', rec_id=rec_id)

@login_required(login_url='login')
def edit_recipe(request,rec_id):
    recipe = get_object_or_404(Recipe, id=rec_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request,"Your recipe edited successfully")
            return redirect('recipe_detail', rec_id=rec_id)
        else:
            messages.error(request,"Invalid form submission")
            return redirect('edit_recipe' ,rec_id=rec_id)
    else:
        form = RecipeForm(instance=recipe)

    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipe/edit_recipe.html', context)

def search(request):
    keyword = request.GET.get('keyword', None)

    if keyword != None:
        recipies = Recipe.objects.annotate(comment_count=Count('comment')).order_by('created_at').filter(
            Q(description__icontains=keyword) | Q(title__icontains=keyword)
        )
    else:
        recipies = Recipe.objects.annotate(comment_count=Count('comment')).order_by('-created_at')


    context = {
        'recipies': recipies,
        'keyword': keyword,  # Pass the keyword for possible future use (e.g., displaying in the template)
    }

    return render(request, 'recipe/recipe_list.html', context)














    


