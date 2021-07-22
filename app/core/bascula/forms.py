import datetime

from django import forms
from django.db.models import Max
from django.forms import ModelForm
from core.base.forms import readonly_fields

from core.bascula.models import (Categoria, ClienteProducto, Movimiento, Chofer, Vehiculo, 
                                 Cliente,Producto,MarcaVehiculo)



''' 
====================
===   SHEARCH    ===
==================== '''
class SearchForm(forms.ModelForm):
    # Extra Fields
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    class Meta:
        model = Movimiento
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control select2', }),
            'producto': forms.Select(attrs={'class': 'form-control select2', }),
            'vehiculo': forms.Select(attrs={'class': 'form-control select2', }),
            'chofer': forms.Select(attrs={'class': 'form-control select2', }),
            # 'tipo_voto': forms.Select(attrs={'class': 'form-control select2', }),
        }
      

''' 
====================
===    CLIENTE    ===
==================== '''
class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese un Cliente'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
''' 
======================
=== MARCA VEHICULO ===
====================== '''
class MarcaVehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = MarcaVehiculo
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Marca Vehiculo'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
''' 
====================
===   CATEGORIA   ===
==================== '''
class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Categoria'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' 
====================
===   PRODUCTO   ===
==================== '''
class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese un Producto'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    

"""FORMULARIO DE VEHICULO"""
class VehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Vehiculo
        fields =['matricula','marca',]    
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }
        
    '''Eliminamos espacios de la matricula '''
    def clean_matricula(self):
        data = self.cleaned_data['matricula']
        data = data.replace(" ","")
        return data
   
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

"""FORMULARIO DE CHOFER"""
class ChoferForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Chofer
        fields =['codigo','nombre','apellido']
                   
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

"""FORMULARIO DE CLIENTE PRODUCTO"""
class ClienteProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = ClienteProducto
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
                }
            ),
            'producto': forms.SelectMultiple(
                attrs={'class': 'form-control select2', 'multiple': 'multiple', 'style': 'width:100%'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


"""FORMULARIO PARA MOVIMIENTO DE ENTRADA"""
class MovimientoEntradaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['vehiculo'].queryset = Vehiculo.objects.none()
        # '''MAX NRO. TICKET'''
        # max_nro_ticket = Movimiento.objects.aggregate(Max('nro_ticket'))['nro_ticket__max']
        # if max_nro_ticket is None:
        #     max_nro_ticket = 0  

        # '''VALORES INICIALES'''
        self.initial['fecha'] = datetime.date.today
        self.initial['nro_ticket'] = 0
        
        '''ATRIBUTOS'''
        for form in self.visible_fields():
            pass
            # form.field.widget.attrs['readonly'] = 'readonly'
            # form.field.widget.attrs['class'] = 'form-control'
            # form.field.widget.attrs['autocomplete'] = 'off'
       
    class Meta:
        model = Movimiento
        fields =['fecha','nro_ticket','vehiculo','chofer',
                 'nro_mic','nro_remision','peso_embarque',
                 'cliente','producto','peso_entrada','sucursal']
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
                }
            ),
            'chofer': forms.Select(attrs={
                'class': 'custom-select select2',
                #  'style': 'width: 100%'
                }
            ),
            'cliente': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
                }
            ),
            'producto': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
                }
            ),
            'fecha': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
            'nro_ticket': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
            'peso_entrada': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


"""FORMULARIO PARA MOVIMIENTO DE SALIDA"""  
class MovimientoSalidaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        max_nro_ticket = Movimiento.objects.aggregate(Max('nro_ticket'))['nro_ticket__max']
        if max_nro_ticket is None:
            max_nro_ticket = 0  

        '''VALORES INICIALES'''
        # self.initial['fecha'] = datetime.date.today
        self.initial['nro_ticket'] = max_nro_ticket + 1

        for form in self.visible_fields():
            # form.field.widget.attrs['readonly'] = 'readonly'
            form.field.widget.attrs['class'] = 'form-control'
            # form.field.widget.attrs['autocomplete'] = 'off'
      
    class Meta:
        model = Movimiento
        fields =['fecha','nro_ticket','vehiculo','chofer',
                 'nro_mic','nro_remision','peso_embarque',
                 'cliente','producto','peso_entrada','peso_salida','sucursal']
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'custom-select',
                'disabled': True,
                }
            ),
            'chofer': forms.Select(attrs={
                'class': 'custom-select',
                'disabled': True,
                }
            ),
            'cliente': forms.Select(attrs={
                'class': 'custom-select',
                'disabled': True,
                }
            ),
            'producto': forms.Select(attrs={
                'class': 'custom-select',
               'disabled': True,
                }
            ),
            'fecha': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
            'nro_ticket': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                # '-'
                }
            ),
            'peso_entrada': forms.TextInput(attrs={
                'readonly': True,
                'type': 'hidden',
                # 'style': 'width: 100%'
                }
            ),
            'peso_salida': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
            'nro_mic': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
            'nro_remision': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
            'peso_embarque': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
        }
   
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
