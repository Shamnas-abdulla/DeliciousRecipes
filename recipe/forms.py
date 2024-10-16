from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredients',
            'instructions',
            'cooking_time',
            'servings',
            'recipe_type',
            'category',
            'image',
        ]
        def __init__(self, *args, **kwargs):
            super(RecipeForm, self).__init__(*args, **kwargs)
            self.fields['recipe_type'].required = True
            self.fields['category'].required = True
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': 'form-control custom-input',
        #         'placeholder': 'Enter recipe title',
        #         'id': 'recipeTitle',
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': 'form-control custom-textarea',
        #         'placeholder': 'Brief description of the recipe',
        #         'rows': 4,
        #         'id': 'recipeDescription',
        #     }),
        #     'ingredients': forms.Textarea(attrs={
        #         'class': 'form-control custom-textarea',
        #         'placeholder': 'List the ingredients here',
        #         'rows': 6,
        #         'id': 'recipeIngredients',
        #     }),
        #     'instructions': forms.Textarea(attrs={
        #         'class': 'form-control custom-textarea',
        #         'placeholder': 'Step-by-step cooking instructions',
        #         'rows': 6,
        #         'id': 'recipeInstructions',
        #     }),
        #     'recipe_type': forms.Select(attrs={
        #         'class': 'form-control custom-select',
        #         'id': 'recipeType',
        #     }),
        #     'image': forms.ClearableFileInput(attrs={
        #         'class': 'form-control-file custom-file-upload',
        #         'id': 'recipeImage',
        #     }),
        #     'cooking_time': forms.NumberInput(attrs={
        #         'class': 'form-control custom-input',
        #         'placeholder': 'Cooking time in minutes',
        #         'id': 'cookingTime',
        #     }),
        #     'servings': forms.TextInput(attrs={
        #         'class': 'form-control custom-input',
        #         'placeholder': 'Number of servings',
        #         'id': 'servings',
        #     }),
        #     'category': forms.Select(attrs={
        #         'class': 'form-control custom-select',
        #         'id': 'recipeCategory',
        #     }),
        # }
