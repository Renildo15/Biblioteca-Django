from django.shortcuts import redirect, render
from django.http import HttpResponse

from usuarios_app.models import Usuario

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario'])
        return HttpResponse(f'Olá, {usuario}')
    else:
        return redirect('/auth/login/?status=2')