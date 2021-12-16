from tinymce import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from BlogSite.utils import unique_slug_generator

User = get_user_model()

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='upload/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='upload/', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    featured = models.BooleanField()
    #previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    #next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    #comment_count = models.IntegerField(default=0)
    #view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)
        # return reverse('post-detail', kwargs={
        #     'id': self.id
        # })

    def get_update_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)
        # return reverse('post-update', kwargs={
        #     'id': self.id
        # })

    def get_delete_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)
        # return reverse('post-delete', kwargs={
        #     'id': self.id
        # })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

# Responsible for creating a slug automatically
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(slug_generator, sender= Post)



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    #profile_picture = models.ImageField()
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Contact(models.Model):
    contact_name =models.TextField()
    contact_email = models.EmailField()
    subject = models.TextField(null=True, blank=True)
    message = models.TextField


