from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('livro/', include('livros_app.urls')),
    path('auth/', include('usuarios_app.urls')),
]
