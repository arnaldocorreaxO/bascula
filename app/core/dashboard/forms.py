''' 
=============================
===    FORM DE BUSQUEDA   ===
============================= '''


from django import forms

from core.base.models import Sucursal

class SucursalModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_short_name()

class DashboardForm(forms.Form):
    # Extra Fields
    fecha = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    sucursal = SucursalModelChoiceField(queryset=Sucursal.objects.filter(
        activo__exact=True).order_by('denominacion_corta'), empty_label=None)
    
    #Widgets
    sucursal.widget.attrs.update(
        {'class': 'form-control select2'})
