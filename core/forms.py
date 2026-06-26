from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import AvanceFisico, Rutina, PerfilUsuario

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'space-y-2'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-akela-500 focus:border-akela-500 outline-none transition bg-white'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-akela-500 focus:border-akela-500 outline-none transition', 'rows': 4})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-akela-500 focus:border-akela-500 outline-none transition'})
            else:
                field.widget.attrs.update({'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-akela-500 focus:border-akela-500 outline-none transition'})

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    telefono = forms.CharField(max_length=20, required=False, label='Teléfono')
    fecha_nacimiento = forms.DateField(
        required=False, label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-akela-500 focus:border-akela-500 outline-none transition'})
            else:
                field.widget.attrs.update({'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-akela-500 focus:border-akela-500 outline-none transition'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            perfil = PerfilUsuario.objects.get(user=user)
            perfil.telefono = self.cleaned_data.get('telefono', '')
            perfil.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
            perfil.save()
        return user

class AvanceFisicoForm(BaseForm):
    class Meta:
        model = AvanceFisico
        fields = ['peso', 'porcentaje_grasa', 'notas']

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso and peso <= 0:
            raise forms.ValidationError('El peso debe ser un valor positivo.')
        if peso and peso > 500:
            raise forms.ValidationError('El peso ingresado no es válido.')
        return peso

    def clean_porcentaje_grasa(self):
        grasa = self.cleaned_data.get('porcentaje_grasa')
        if grasa is not None and (grasa < 0 or grasa > 100):
            raise forms.ValidationError('El porcentaje de grasa debe estar entre 0 y 100.')
        return grasa

class RutinaForm(BaseForm):
    class Meta:
        model = Rutina
        fields = ['nombre', 'descripcion', 'nivel', 'asignada_a']
        widgets = {
            'asignada_a': forms.CheckboxSelectMultiple(),
        }
