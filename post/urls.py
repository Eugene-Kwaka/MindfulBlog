from django.urls import path
from post.views import *
from django.contrib.auth import views as auth_views


# REGISTER & LOGIN URL PATHS
urlpatterns = [
    path('register/', registerPage, name='registerPage'),
    path('login/', loginPage, name='loginPage'),
    path('logout/', logoutUser, name='logout'),
    path('search/', search, name="search"),
    path('contact/', contact, name='contact'),
    path('email.html/', email, name="email"),

    path('', index, name="home"),
    path('blog/', blog, name="post-list"),

    path('add_category/', add_category, name="add_category"),
    # path('<slug:slug>/', category, name='category'),
    path('create/', post_create, name="post-create"),
    path('post/<id>/', post, name="post-detail"),
    # path('<slug:category_slug>/<slug:slug>/', post, name="post-detail"),
    path('post/<id>/update/', post_update, name="post-update"),
    # path('<slug:category_slug>/<slug:slug>/update/',  post_update, name="post-update"),
    path('post/<id>/delete/', post_delete, name="post-delete"),
    # path('<slug:category_slug>/<slug:slug>/delete/', post_delete, name="post-delete"),
    
    
    # PASSWORD RESET URL PATHS
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_form.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_done.html"), name="password_reset_complete"),

]