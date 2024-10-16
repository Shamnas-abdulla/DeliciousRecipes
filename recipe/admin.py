from django.contrib import admin
from .models import Recipe, Comment, Rating, FavoriteRecipe
# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title','recipe_type','category','created_at','updated_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','recipe','subject','updated_at')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user','recipe','rate','updated_at')


admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Rating,RatingAdmin)
admin.site.register(FavoriteRecipe)
