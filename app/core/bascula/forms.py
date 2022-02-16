import datetime

from django import forms
from django.db.models import Max
from django.forms import ModelForm
from core.base.forms import readonly_fields

from core.bascula.models import (Categoria, ClienteProducto, Movimiento, Chofer, Transporte, Vehiculo, 
								 Cliente,Producto,MarcaVehiculo)

''' 
====================
===   SHEARCH    ===
==================== '''

class SearchForm(forms.Form):
	# Extra Fields
	date_range = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'autocomplete': 'off'
	}))

	# cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(activo__exact=True).order_by('denominacion'),empty_label="(Todos)")
	transporte = forms.ModelChoiceField(queryset=Transporte.objects.filter(activo=True),empty_label="(Todos)")
	cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(activo=True),empty_label="(Todos)")
	destino = forms.ModelChoiceField(queryset=Cliente.objects.filter(activo=True,ver_en_destino=True),empty_label="(Todos)")
	# producto = forms.ModelChoiceField(queryset=Producto.objects.filter(activo__exact=True).order_by('denominacion'), empty_label="(Todos)")
	producto = forms.ModelChoiceField(queryset=Producto.objects.none(), empty_label="(Todos)")
	# vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.filter(activo__exact=True).order_by('matricula'), empty_label="(Todos)")
	vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.none(), empty_label="(Todos)")
	# chofer = forms.ModelChoiceField(queryset=Chofer.objects.filter(activo__exact=True).order_by('nombre','apellido'), empty_label="(Todos)")
	chofer = forms.ModelChoiceField(queryset=Chofer.objects.none(), empty_label="(Todos)")
   
	transporte.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
	cliente.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
	destino.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
	producto.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
	vehiculo.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
	chofer.widget.attrs.update({'class': 'form-control select2','multiple':'true'})  

''' 
====================
=== TRANSPORTE   ===
==================== '''
class TransporteForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	class Meta:
		model = Transporte
		fields = '__all__'
		exclude = readonly_fields
		widgets = {
			'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese denominacion Transporte'}),
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

''' 
====================
===   VEHICULO   ===
==================== '''
class VehiculoForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	class Meta:
		model = Vehiculo
		fields = '__all__'
		exclude = readonly_fields    
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

''' 
====================
===   CHOFER     ===
==================== '''
class ChoferForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	class Meta:
		model = Chofer
		fields = '__all__'
		exclude = readonly_fields
				   
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
''' 
============================
===   CLIENTE PRODUCTO   ===
============================ '''
class ClienteProductoForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	class Meta:
		model = ClienteProducto
		fields = '__all__'
		exclude = readonly_fields
		widgets = {
			'sucursal': forms.Select(attrs={
				'class': 'custom-select select2',
				# 'style': 'width: 100%'
				}
			),
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


''' 
==============================
===   MOVIMIENTO ENTRADA   ===
============================== '''
class MovimientoEntradaForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['vehiculo'].queryset = Vehiculo.objects.none()
		self.fields['chofer'].queryset = Chofer.objects.none()
		self.fields['cliente'].queryset = Cliente.objects.exclude(activo=False).order_by('id')[:5]
		self.fields['producto'].queryset = Producto.objects.none()
		self.fields['destino'].queryset = Cliente.objects.filter(activo=True,ver_en_destino=True)
		qs = Cliente.objects.exclude(activo=False,ver_en_destino=False)
		print(qs.query)
		# '''MAX NRO. TICKET'''
		# max_nro_ticket = Movimiento.objects.aggregate(Max('nro_ticket'))['nro_ticket__max']
		# if max_nro_ticket is None:
		#     max_nro_ticket = 0  

		# '''VALORES INICIALES'''
		self.initial['fecha'] = datetime.date.today
		self.initial['nro_ticket'] = 0     
	   
	class Meta:
		model = Movimiento
		fields =['fecha','nro_ticket','vehiculo','chofer',
				 'nro_mic','nro_remision','peso_embarque',
				 'cliente','producto','peso_entrada',
				 'transporte','destino','sucursal','referencia']
		widgets = {
			'fecha': forms.TextInput(attrs={
				'readonly': True,                
				}
			),
			'nro_ticket': forms.TextInput(attrs={
				'readonly': True,                
				}
			),
			'peso_entrada': forms.TextInput(attrs={
				'readonly': True,                
				}
			),
			'vehiculo': forms.Select(attrs={
				'class': 'custom-select select2',
				'style': 'width: 90%'
				}
			),
			'chofer': forms.Select(attrs={
				'class': 'custom-select select2',
				 'style': 'width: 90%'
				}
			),
			'cliente': forms.Select(attrs={
				'class': 'custom-select select2',
				'style': 'width: 100%'
				}
			),            
			'producto': forms.Select(attrs={
				'class': 'custom-select select2',
				'style': 'width: 100%'
				}
			),
			'transporte': forms.Select(attrs={
				'class': 'custom-select select2',
				'style': 'width: 100%'
				}
			),
			'destino': forms.Select(attrs={
				'class': 'custom-select select2',
				'style': 'width: 100%'
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


''' 
==============================
===   MOVIMIENTO SALIDA    ===
============================== ''' 
class MovimientoSalidaForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print((self.instance.vehiculo_id))
		'''NUMERACION TICKET'''
		max_nro_ticket = Movimiento.objects.filter(sucursal_id=self.instance.sucursal.id)\
											.aggregate(Max('nro_ticket'))['nro_ticket__max']
		if max_nro_ticket is None:
			max_nro_ticket = 0 
		# '''NUMERACION REMISION'''
		# year = datetime.datetime.now().year 
		# if not self.instance.nro_remision:
		# 	max_nro_remision = Movimiento.objects.filter(fecha__year=year).aggregate(Max('nro_remision'))['nro_remision__max']
		# 	if max_nro_remision==0:
		# 		max_nro_remision = year * 100000000
		# 	max_nro_remision += 1
		# else:
		# 	max_nro_remision = self.instance.nro_remision 

		'''VALORES INICIALES'''
		self.initial['nro_ticket'] = max_nro_ticket + 1
		# self.initial['nro_remision'] = max_nro_remision 

		self.fields['vehiculo'].queryset = Vehiculo.objects.filter(id=self.instance.vehiculo_id)
		self.fields['chofer'].queryset = Chofer.objects.filter(id=self.instance.chofer_id)
		self.fields['cliente'].queryset = Cliente.objects.filter(id=self.instance.cliente_id)
		self.fields['producto'].queryset = Producto.objects.filter(id=self.instance.producto_id)

		for form in self.visible_fields():
			# form.field.widget.attrs['readonly'] = 'readonly'
			form.field.widget.attrs['class'] = 'form-control'
			# form.field.widget.attrs['autocomplete'] = 'off'
	  
	class Meta:
		model = Movimiento
		fields =['fecha','nro_ticket','vehiculo','chofer',
				 'nro_mic','nro_remision','peso_embarque',
				 'cliente','producto','peso_entrada','peso_salida',
				 'transporte','destino','sucursal','referencia']
		widgets = {
			'fecha': forms.TextInput(attrs={
				'readonly': True,                
				}
			),
			'nro_ticket': forms.TextInput(attrs={
				'readonly': True,
				}
			),
			'transporte': forms.Select(attrs={
				'class': 'custom-select',
				'style': 'width: 100%',
				'disabled': True,
				}
			),
			'vehiculo': forms.Select(attrs={
				'class': 'custom-select',
				'style': 'width: 100%',
				'disabled': True,
				}
			),
			'chofer': forms.Select(attrs={
				'class': 'custom-select',
				'style': 'width: 100%',
				'disabled': True,
				}
			),
			'cliente': forms.Select(attrs={
				'class': 'custom-select',
				'style': 'width: 100%',
				'disabled': True,
				}
			),
			'producto': forms.Select(attrs={
				'class': 'custom-select',
				'style': 'width: 100%',
			   'disabled': True,
				}
			),
			'destino': forms.Select(attrs={
				'class': 'custom-select',
				'style': 'width: 100%',
			   'disabled': True,
				}
			),
			
			'peso_entrada': forms.TextInput(attrs={
				'readonly': True,
				'type': 'hidden',                
				}
			),
			'peso_salida': forms.TextInput(attrs={
				'readonly': True,                
				}
			),
			'nro_mic': forms.TextInput(attrs={
				'readonly': True,                
				}
			),
			'nro_remision': forms.TextInput(attrs={
				'readonly': True,                
				}
			),
			'peso_embarque': forms.TextInput(attrs={
				'readonly': True,                
				}
			),
			'referencia': forms.TextInput(attrs={
				'readonly': True,                
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