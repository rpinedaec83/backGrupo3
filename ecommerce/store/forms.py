from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Direccion
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.urls import reverse_lazy
from django.views.generic import UpdateView

class RegisterForm(UserCreationForm):
    dni = forms.CharField(max_length=8)
    telefono = forms.CharField(max_length=15)
    fecha_nacimiento = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    pais = CountryField().formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class ClienteForm(forms.Form):
    dni = forms.CharField(max_length=8)
    telefono = forms.CharField(max_length=15)
    fecha_nacimiento = forms.DateField()
    pais = forms.CharField(max_length=100)

class DireccionForm(forms.ModelForm):
    pais = CountryField().formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Direccion
        fields = ["pais", "distrito", "ciudad", "codigo_postal", "avenida_calle_jiron", "numero_calle"]

class EditarDireccionView(UpdateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'editar_direccion.html'
    success_url = reverse_lazy('mi_cuenta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['direccion'] = Direccion.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        direccion = form.save(commit=False)
        direccion.cliente = self.request.user.cliente
        direccion.save()
        return super().form_valid(form)