from django.urls import path
from .import views

urlpatterns = [
    path('create_recipe/', views.create_recipe, name="create_recipe"),
    path('recipe_list/',views.recipe_list, name="recipe_list"),
    path('recipe_detail/<int:rec_id>/',views.recipe_detail,name="recipe_detail"),
    path('comment_save/<int:rec_id>/',views.comment_save, name="comment_save"),
    path('rating/<int:rec_id>/', views.rating, name="rating"),
    path('filter_recipe/', views.filter_recipe, name="filter_recipe"),
    path('save_recipe/<int:rec_id>/', views.save_recipe, name="save_recipe"),
    path('edit_recipe/<int:rec_id>/', views.edit_recipe, name="edit_recipe"),
     path('search/', views.search, name='search'),  # Add this search URL
]