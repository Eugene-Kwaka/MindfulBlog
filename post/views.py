from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author, PostView, Contact
from .forms import *
from marketing.models import Signup
from django.core.mail import send_mail
from django.conf import settings

from django.template.defaultfilters import slugify

# for User Creation & Authentication
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users


# Register User
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + username)
            return redirect('loginPage')
        else:
            form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


# Login
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username OR Password is incorrect!")

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loginPage')


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


# This view will serve the Search functionality which will be based on text
def search(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'post_list': post_list
    }
    return render(request, 'search_results.html', context)


# This view is to show the number of blogposts under a particular category
def get_category_count():
    queryset = Post.objects.values(
        'category__title').annotate(Count('category__title'))
    return queryset


# View for the Index.html page (Home page)
def index(request):
    queryset = Post.objects.filter(featured=True)
    """This code is responsible for the 'Latest From the Blog' section of the index page."""
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST.get("email", False)
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': queryset,
        'latest': latest,
    }
    return render(request, 'index.html', context)


# View page for the blog.html page that shows the list of blogposts
def blog(request):
    category_count = get_category_count()
    """The 'most_recent' variable is same to the 'latest' variable in the index view"""
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post_list = Post.objects.all()

    paginator = Paginator(post_list, per_page=1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # paginator = Paginator(post_list, 1)
    # page_request_var = 'page'
    # page = request.GET.get(page_request_var)
    # try:
    #     paginated_queryset = paginator.page(page)
    # except PageNotAnInteger:
    #     paginated_queryset = paginator.page(1)
    # except EmptyPage:
    #     paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'post_list': page_obj.object_list,
        'most_recent': most_recent,
        'category_count': category_count,
        'paginator': paginator,
        'page_number': int(page_number),
        # 'page_request_var': page_request_var,
        }
    return render(request, 'blog.html', context)


# View for the post.html page that is intended to show individual posts
def post(request,category_slug, slug):  #id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post = get_object_or_404(Post, slug=slug) #id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            # return redirect(reverse('post-detail', kwargs={
            #     'id': post.id
            # }))
            return redirect('post-detail', category_slug=category_slug , slug=slug)
    context = {
        'form': form,
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'post.html', context)

@allowed_users(allowed_roles=['admin'])
def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author
            #post.slug = slugify(post.title)
            # form.instance.author = author
            post.save()
            # return redirect(reverse("post-detail", kwargs={
            #     'id': form.instance.id
            # }))
            return redirect('post-list')
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

@allowed_users(allowed_roles=['admin'])
def post_update(request, category_slug, slug): #id
    title = 'Update'
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            # return redirect(reverse("post-detail", kwargs={
            #     'id': form.instance.id
            # }))
            return redirect('post-detail', category_slug=category_slug , slug=slug)
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

@allowed_users(allowed_roles=['admin'])
def post_delete(request, category_slug, slug): #id):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect(reverse("post-list"))


@allowed_users(allowed_roles=['admin'])
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = CategoryForm()
    context={
        'form':form,
    }
    return render(request, 'add_category.html', context)

def category(request, slug):
    category_count = get_category_count()
    category = get_object_or_404(Category, slug=slug)
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    all_posts = Post.objects.all()
    # This will filter the active posts that exists in the specified category
    post_list = category.posts.all()
    context={
        'category':category,
        'all_posts':all_posts,
        'post_list':post_list,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'category.html', context)

def contact(request):
    form = ContactForm()
    if request.method=='POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                f"{contact_name} sent an email",
                message,
                subject,
                contact_email,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            return redirect('email')
        else:
            form = ContactForm()
    context={
        'form': form,
    }
    return render(request, 'contact.html', context)

def email(request):
    context = {
        'success': True,
    }
    return render(request, 'email.html', context)