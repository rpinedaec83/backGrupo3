from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, TemplateView
from django.views.generic.edit import FormView, UpdateView
from .forms import CambiarPasswordForm, DireccionForm, LoginForm, RegisterForm
from .models import Categoria, Cliente, Cupon, Direccion, Pedido, Producto
from django.db.models import Q
from django.db import IntegrityError


@method_decorator(login_required, name='dispatch')
class CambiarPasswordView(FormView):
    template_name = 'cambiar_contraseña.html'
    form_class = CambiarPasswordForm

    def get_form_kwargs(self):
        kwargs = super(CambiarPasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        old_password = form.cleaned_data.get('old_password')
        new_password = form.cleaned_data.get('new_password1')
        if not user.check_password(old_password):
            form.add_error(None, 'Tu contraseña antigua es incorrecta.')
            return self.form_invalid(form)
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Tu contraseña ha sido actualizada exitosamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mi_cuenta')


@method_decorator(login_required, name='dispatch')
class EliminarDireccionView(DeleteView):
    model = Direccion
    template_name = 'eliminar_direccion.html'
    success_url = reverse_lazy('mi_cuenta')

    def get_object(self, queryset=None):
        """Hook to ensure object is owned by request.user. """
        obj = super().get_object()
        if not obj.cliente == self.request.user.cliente:
            raise Http404
        return obj
    
@method_decorator(login_required, name='dispatch')
class AgregarDireccionView(TemplateView):
    template_name = 'agregar_direccion.html'

    def get(self, request, *args, **kwargs):
        form = DireccionForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.cliente = request.user.cliente
            try:
                direccion.save()
                return redirect('mi_cuenta')
            except IntegrityError:
                form.add_error(None, 'Esta dirección ya existe.')
        return self.render_to_response({'form': form})

@method_decorator(login_required, name='dispatch')
class EditarDireccionView(UpdateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'editar_direccion.html'
    success_url = reverse_lazy('mi_cuenta')

    def get_object(self, queryset=None):
        """Hook to ensure object is owned by request.user. """
        obj = super().get_object()
        if not obj.cliente == self.request.user.cliente:
            raise Http404
        return obj

    def form_valid(self, form):
        form.instance.cliente = self.request.user.cliente
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class MiCuentaView(TemplateView):
    template_name = 'mi_cuenta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.request.user.cliente
        context['direcciones'] = Direccion.objects.filter(cliente=cliente)
        context['pedidos'] = Pedido.objects.filter(cliente=cliente)
        context['cupones'] = Cupon.objects.filter(activo=True)
        context['form'] = DireccionForm()  # Nuevo
        return context

    def post(self, request, *args, **kwargs):
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.cliente = request.user.cliente
            direccion.save()
        return super().get(request, *args, **kwargs)


def home_view(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.all()

    query = request.GET.get('q')
    categoria = request.GET.get('categoria')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )

    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    if min_price:
        productos = productos.filter(precio__gte=min_price)

    if max_price:
        productos = productos.filter(precio__lte=max_price)

    context = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'home.html', context)


def producto_detalle_view(request, id):
    producto = get_object_or_404(Producto, id=id)
    context = {
        'producto': producto,
    }
    return render(request, 'producto_detalle.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                dni = form.cleaned_data.get('dni')
                telefono = form.cleaned_data.get('telefono')
                fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
                pais = form.cleaned_data.get('pais')
                cliente = Cliente.objects.create(user=user, dni=dni, telefono=telefono, fecha_nacimiento=fecha_nacimiento, pais=pais)
                cliente.save()
                messages.success(request, 'Te has registrado con éxito.')
                return redirect('home')
            except IntegrityError:
                form.add_error(None, 'El nombre de usuario o el correo electrónico ya existen.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def account_view(request):
    return render(request, 'account.html')