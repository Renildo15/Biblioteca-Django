from django.contrib import admin

from usuarios_app.models import Usuario

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ('nome', 'email','senha')