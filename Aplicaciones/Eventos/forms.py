from django import forms
from .models import Notificacion

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ['usuario', 'evento', 'tipo', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }