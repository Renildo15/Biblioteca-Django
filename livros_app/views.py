from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Emprestimos, Livros, Categoria
from usuarios_app.models import Usuario
from .forms import CadastroLivro, CategoriaLivro

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario'])
        status_categoria = request.GET.get('cadastro_categoria')
        livros = Livros.objects.filter(usuario = usuario)
        form = CadastroLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
        form_categoria = CategoriaLivro()
        usuarios = Usuario.objects.all()

        livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)

        return render(request, 'home.html',{'livros': livros, 'usuario_logado': request.session.get('usuario'), 
        'form' : form,'form_categoria': form_categoria, 'status_categoria': status_categoria, 'usuarios' : usuarios, 'livros_emprestar' : livros_emprestar})
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

            form_categoria = CategoriaLivro()
            usuarios = Usuario.objects.all()
            livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)

            return render(request, 'ver_livro.html', {'livro': livro, 'categoria_livro': categoria_livro, 
            'emprestimos' : emprestimos, 'usuario_logado': request.session.get('usuario'), 'form' : form, 'id_livro': id, 
            'form_categoria': form_categoria, 'usuarios' : usuarios, 'livros_emprestar' : livros_emprestar})
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

def excluir_livro(request, id):
    livro = Livros.objects.get(id=id)
    livro.delete()
    return redirect('/livro/home')


def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)
    nome = form.data['nome']
    descricao = form.data['descricao']
    id_usuario = request.POST.get('usuario')

    if int(id_usuario) == int(request.session.get('usuario')):
        user = Usuario.objects.get(id = id_usuario)
        categoria = Categoria(nome=nome, descricao=descricao, usuario=user)
        categoria.save()
        return redirect('/livro/home?cadastro_categoria=1')
    else:
        return HttpResponse('Erro')

def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado = request.POST.get('livro_emprestado')
        
        if nome_emprestado_anonimo:
            emprestimo = Emprestimos(nome_emprestado_anonimo = nome_emprestado_anonimo,
                                    livro_id = livro_emprestado)
        else:
            emprestimo = Emprestimos(nome_emprestado_id=nome_emprestado,
                                    livro_id = livro_emprestado)
        emprestimo.save()

        livro = Livros.objects.get(id = livro_emprestado)
        livro.emprestado = True

        livro.save()

        return redirect('/livro/home')