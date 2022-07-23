from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Emprestimos, Livros, Categoria
from usuarios_app.models import Usuario
from .forms import CadastroLivro

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario'])
        livros = Livros.objects.filter(usuario = usuario)
        form = CadastroLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
        return render(request, 'home.html',{'livros': livros, 'usuario_logado': request.session.get('usuario'), 
        'form' : form})
    else: 
        return redirect('/auth/login/?status=2')

def ver_livros(request, id):
    if request.session.get('usuario'):
        livro = Livros.objects.get(id=id)
        if request.session.get('usuario') == livro.usuario.id:
            categoria_livro = Categoria.objects.filter(usuario = request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro = livro)
            form = CadastroLivro()
            usuario = Usuario.objects.get(id = request.session['usuario'])
            form.fields['usuario'].initial = request.session['usuario']
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
            return render(request, 'ver_livro.html', {'livro': livro, 'categoria_livro': categoria_livro, 
            'emprestimos' : emprestimos, 'usuario_logado': request.session.get('usuario'), 'form' : form})
        else:
            return HttpResponse('Esse livro não é seu')
    return redirect('/auth/login/?status=2')


def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/livro/home')
        else:
            usuario = Usuario.objects.get(id = request.session['usuario'])
            livros = Livros.objects.filter(usuario = usuario)
            form = CadastroLivro()
            return render(request, 'home.html',{'livros': livros, 'usuario_logado': request.session.get('usuario'), 
            'form' : form})