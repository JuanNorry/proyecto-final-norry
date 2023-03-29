from django.shortcuts import render
from proyectoFinal.models import  Componente, Mensaje, Perfil
from proyectoFinal.forms import UsuarioForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    return render(request, 'proyectoFinal/index.html')

class ComponenteList(ListView):
    model = Componente
    context_object_name = "componentes"

class ComponenteMineList(LoginRequiredMixin, ComponenteList):
    
    def get_queryset(self):
        return Componente.objects.filter(publisher=self.request.user.id).all()


class ComponenteDetail(DetailView):
    model = Componente
    context_object_name = "componente"


class ComponenteUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Componente
    success_url = reverse_lazy("componente-list")
    fields = '__all__'

    def test_func(self):
        user_id = self.request.user.id
        Componente_id =  self.kwargs.get("pk")
        return Componente.objects.filter(publisher=user_id, id=Componente_id).exists()


class ComponenteDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Componente
    context_object_name = "Componentes"
    success_url = reverse_lazy("componente-list")

    def test_func(self):
        user_id = self.request.user.id
        Componente_id =  self.kwargs.get("pk")
        return Componente.objects.filter(publisher=user_id, id=Componente_id).exists()


class ComponenteCreate(LoginRequiredMixin, CreateView):
    model = Componente
    success_url = reverse_lazy("componente-list")
    fields = '__all__'


class ComponenteSearch(ListView):
    model = Componente
    context_object_name = "componentes"

    def get_queryset(self):
        criterio = self.request.GET.get("criterio")
        result = Componente.objects.filter(tipo__icontains=criterio).all()
        return result

class Login(LoginView):
    next_page = reverse_lazy("index")


class SignUp(CreateView):
    form_class = UsuarioForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('componente-list')


class Logout(LogoutView):
    template_name = "registration/logout.html"


class PerfilCreate(LoginRequiredMixin, CreateView):
    model = Perfil
    success_url = reverse_lazy("index")
    fields = ['avatar']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PerfilUpdate(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Perfil
    success_url = reverse_lazy("componente-list")
    fields = ['avatar']

    def test_func(self):
        return Perfil.objects.filter(user=self.request.user).exists()


class MensajeCreate(CreateView):
    model = Mensaje
    success_url = reverse_lazy('mensaje-create')
    fields = '__all__'


class MensajeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mensaje
    context_object_name = "mensaje"
    success_url = reverse_lazy("mensaje-list")

    def test_func(self):
        return Mensaje.objects.filter(destinatario=self.request.user).exists()
    

class MensajeList(LoginRequiredMixin, ListView):
    model = Mensaje
    context_object_name = "mensajes"

    def get_queryset(self):
        import pdb; pdb.set_trace
        return Mensaje.objects.filter(destinatario=self.request.user).all()
    

