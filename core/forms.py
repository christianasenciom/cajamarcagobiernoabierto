from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Organizacion, Persona, Evento, Documento, Eje


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
        }),
        label="Contraseña"
    )
    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña',
        }),
        label="Confirma tu contraseña"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu nombre',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu apellido',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un usuario',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu correo electrónico',
            }),
        }

    def __init__(self, *args, **kwargs):

        self.is_editing = kwargs.pop('is_editing', False)
        super().__init__(*args, **kwargs)

        if self.is_editing:

            self.fields['password'].required = False
            self.fields['password_confirm'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not self.is_editing:

            if password and password_confirm and password != password_confirm:
                self.add_error('password_confirm', "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
        }),
        label="Nombre de usuario"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
        }),
        label="Contraseña"
    )

class OrganizacionForm(forms.ModelForm):
    class Meta:
        model = Organizacion
        fields = ['logo', 'razon_social', 'direccion', 'rubro', 'provincias']

# Formulario para la clase Persona
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['condicion', 'nombres', 'apellidos', 'correo_electronico', 'cargo', 'organizacion']

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['categoria', 'nombre', 'url']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del documento'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace de Google Drive'}),
        }
        labels = {
            'categoria': 'Categoría',
            'nombre': 'Nombre del Documento',
            'url': 'Enlace de Google Drive',
        }

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'nombre_evento','detalle' ,'plazo', 'fechainicio','fechafin', 'horainicio','horafin', 'medio', 'direccion', 'url']
        labels = {
            'titulo': 'Título',
            'nombre_evento': 'Nombre del Evento',
            'detalle' : 'Detalle',
            'plazo': 'Plazo',
            'fechainicio': 'Fecha de Inicio',
            'fechafin' : 'Fecha de Fin (Opcional)',
            'horainicio': 'Hora de Inicio',
            'horafin': 'Hora de Fin',
            'medio': 'Medio',
            'direccion': 'Dirección (Opcional)',
            'url':'URL (Opcional)'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el título del evento',
            }),
            'nombre_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el nombre del evento',
            }),
            'detalle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el detalle del evento',
            }),
            'plazo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el plazo del evento',
            }),
            'fechainicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'fechafin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Opcional',
            }),
            'horainicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'horafin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'medio': forms.Select(attrs={
                'class': 'form-control',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe la dirección del evento',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe la URL del evento (opcional)',
            }),
        }

from .models import Compromiso, Hito

# class CompromisoForm(forms.ModelForm):
#     eje = forms.ModelChoiceField(
#         queryset=Eje.objects.all(),  # Trae todos los registros de la tabla Eje
#         empty_label="Seleccionar Eje",  # Etiqueta de la opción vacía
#         widget=forms.Select(attrs={'class': 'form-control'})  # Clase para el estilo
#     )
#     class Meta:
#         model = Compromiso
#         fields = [
#             'titulo','eje', 'problema', 'estado_inicial', 'accion', 'relevancia', 'otros_actores',
#             'area_responsable', 'responsables', 'correo_contacto', 'telefono_contacto',
#             'avance', 'estado_avance'
#         ]
#         widgets = {
#             'problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'estado_inicial': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'accion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'relevancia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'otros_actores': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
#         }

class CompromisoForm(forms.ModelForm):
    eje = forms.ModelChoiceField(
        queryset=Eje.objects.all(),
        empty_label="Seleccionar Eje",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Compromiso
        fields = [
            'titulo', 'eje', 'problema', 'estado_inicial', 'accion', 'relevancia',
            'otros_actores', 'area_responsable', 'responsables', 'correo_contacto',
            'telefono_contacto', 'avance', 'estado_avance'
        ]
        widgets = {
            'problema': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'oninput': 'this.style.height = "";this.style.height = this.scrollHeight + "px";'
            }),
            'estado_inicial': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'oninput': 'this.style.height = "";this.style.height = this.scrollHeight + "px";'
            }),
            'accion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'oninput': 'this.style.height = "";this.style.height = this.scrollHeight + "px";'
            }),
            'relevancia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'oninput': 'this.style.height = "";this.style.height = this.scrollHeight + "px";'
            }),
            'otros_actores': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'oninput': 'this.style.height = "";this.style.height = this.scrollHeight + "px";'
            }),
        }

class HitoForm(forms.ModelForm):
    compromiso = forms.ModelChoiceField(
        queryset=Compromiso.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Seleccionar Compromiso"
    )

    class Meta:
        model = Hito
        fields = ['compromiso', 'titulo', 'estado', 'fecha_inicio', 'fecha_final', 'avance', 'evidencia']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avance': forms.NumberInput(attrs={'class': 'form-control'}),
            'evidencia': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe la URL de la evidencia (opcional)',
            }),
        }

