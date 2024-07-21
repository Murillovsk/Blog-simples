from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Posts
from .forms import PostsForm

# Create your views here.
def post_list(request):
    template_name = 'post-list.html' # template
    posts = Posts.objects.all() # query com todas as postagens
    context = { # cria context para chamar no template
        'posts': posts
        }
    return render(request, template_name, context) # render

def post_create(request):
    if request.method == 'POST': # para metodo POST
        form = PostsForm(request.POST, request.FILES) # pega as informações do form
        if form.is_valid(): # se for valido
            form = form.save(commit=False)
            form.save() # salva
            
            messages.success(request, 'O post foi criado com sucesso') # mensagem quando cria o post
            return HttpResponseRedirect(reverse('post-list')) # coloquei para retornar post-list
        
    form = PostsForm() # senão carrega o formulario  
    return render(request, 'post-form.html', {"form": form}) # nesse template

def post_detail(request, id):
    template_name = 'post-detail.html' # template
    post = Posts.objects.get(id=id) # Metodo Get
    context = { # cria context para chamar no template
        'post': post
        }
    return render(request, template_name, context) # render

def post_update(request, id):
    post = get_object_or_404(Posts, id=id)
    form = PostsForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()

        messages.success(request, 'O post foi atualizado com sucesso.')
        return HttpResponseRedirect(reverse('post-detail', args=[post.id]))
    return render(request, 'post-form.html', {"form": form})

def post_delete(request, id):
    post = Posts.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'O post fora deletado com sucesso.')
        return HttpResponseRedirect(reverse('post-list'))
    return render(request, 'post-delete.html')