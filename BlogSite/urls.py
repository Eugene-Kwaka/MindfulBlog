from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path

#from post.views import *

# Responsible for password reset
#from django.contrib.auth import views as auth_views

# ALL THE URLS USED IN THE PROJECT WERE INCLUDED IN THIS MAIN URLS.PY FILE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
