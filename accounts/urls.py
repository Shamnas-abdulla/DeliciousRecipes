from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView


urlpatterns = [
    path('register/', views.register,name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('my_profile/<int:user_id>/',views.my_profile, name="my_profile"),
    path('saved_post/<int:user_id>/',views.saved_post, name="saved_post"),
    path('remove_saved_post/<int:rec_id>/',views.remove_saved_post, name="remove_saved_post"),
    path('my_comments/',views.my_comments, name="my_comments"),
    path('delete_comment/<int:com_id>/', views.delete_comment, name="delete_comment"),
    path('edit_profile/',views.edit_profile, name="edit_profile"),
    path('my_rating/',views.my_rating, name="my_rating"),
    path('my_post/',views.my_post, name="my_post"),
    path('delete_recipe/<int:rec_id>/<int:user>/', views.delete_recipe, name="delete_recipe"),

    #Forgot password
    path('reset_password/',
         CustomPasswordResetView.as_view(template_name='accounts/password_reset/password_reset.html'),
         name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset/password_reset_form.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]