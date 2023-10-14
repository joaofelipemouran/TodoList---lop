from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from  django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import  FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy
from .models import Task

# Create your views here.

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'task'
    # essa função faz conque o usuario não acessa a pagina sem que ele esteja logado
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete = False).count()

        search_input = self.request.GET.get('buscar') or ''
        if search_input:
            context['task'] = context['task'].filter(title__startswith = search_input)
            context['search_input'] = search_input
        return context


# criação do conteudo da tarefa
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/detail.html'

# Criação de nova tarefa
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
# Updade de uma tarefa
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task-list')

# Criando a area para excluir uma tarefa
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')
# login
class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task-list')
# registro de usuario
class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)