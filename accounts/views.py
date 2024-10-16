from django.shortcuts import render, redirect
from django.contrib import messages,auth
from .forms import RegistrationForm, EditProfileForm, CustomPasswordResetForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account
from recipe.models import FavoriteRecipe, Comment, Rating, Recipe
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView
from django.utils.translation import gettext_lazy as _
from .forms import CustomPasswordResetForm

from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView
from django.utils.translation import gettext_lazy as _
from .forms import CustomPasswordResetForm

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm  # Use your custom form

    def form_valid(self, form):
        # Simply call the super method to proceed with the password reset process
        return super().form_valid(form)



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # Hash the password before saving
            user.set_password(form.cleaned_data['password'])
            user.save() 
            messages.success(request, "Registration successful!")  # Add a success message
            return redirect('login')  # Redirect to a success page or another URL
        else:
            messages.error(request, "Please correct the errors below.")  # Add error message
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are now logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid login credentials.")
    return render(request,'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"Your logged out!")
    return redirect('login')

@login_required(login_url='login')
def my_profile(request, user_id):
    user = Account.objects.get(id=user_id)
    return render(request, 'accounts/profile.html',{'user':user,})


@login_required(login_url='login')
def saved_post(request, user_id):
    saved_posts = FavoriteRecipe.objects.filter(user=user_id).all()
    return render(request,'accounts/saved_post.html',{'saved_posts':saved_posts,})


@login_required(login_url='login')
def remove_saved_post(request, rec_id):
    favorite = FavoriteRecipe.objects.filter(user=request.user,recipe=rec_id)
    if favorite.exists():
        favorite.delete()
    return redirect('saved_post',user_id=request.user.id)

@login_required(login_url='login')
def my_comments(request):
    comments = Comment.objects.filter(user=request.user.id).all()
    return render(request, 'accounts/my_comments.html',{'comments':comments})

@login_required(login_url='login')
def delete_comment(request,com_id):
    comment = get_object_or_404(Comment, id=com_id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('my_comments')


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            photo = form.cleaned_data.get('photo')
            # Set a default photo if none is provided
            if not photo:
                request.user.photo = 'profile_photos/default-user.png'
            form.save()  # Save the form data
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required(login_url='login')
def my_rating(request):
    user_ratings  = Rating.objects.filter(user=request.user)
    return render(request, 'accounts/my_rating.html',{'user_ratings':user_ratings,})

@login_required(login_url='login')
def my_post(request):
    recipies = Recipe.objects.filter(user=request.user.id).all()
    return render(request, 'accounts/my_post.html',{'recipies':recipies,})

@login_required(login_url='login')
def delete_recipe(request, rec_id, user):
    try:
        recipe = Recipe.objects.get(user=user, id=rec_id)
        recipe.delete()
        messages.success(request, "Your post deleted successfully.")
    except Recipe.DoesNotExist:
        messages.error(request, "The post you're trying to delete does not exist.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('my_post')
    








