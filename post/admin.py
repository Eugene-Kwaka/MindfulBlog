from django.contrib import admin


from .models import *

class CommentItemInline(admin.TabularInline):
    model = Comment
    row_id_fields = ['post']

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'overview', 'content']
    list_display = ['title', 'slug','timestamp']
    list_filter = ['author', 'timestamp']
    # prepopulates the slug fields
    prepopulated_fields = {'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'post', 'timestamp']


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostView)
admin.site.register(Contact)

