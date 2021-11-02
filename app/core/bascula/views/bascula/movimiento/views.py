#SYSTEM
import json
import os
import datetime

from config import settings
from core.bascula.forms import (ChoferForm, MovimientoEntradaForm,
								MovimientoSalidaForm, SearchForm, VehiculoForm)
#LOCALS
from core.views import printSeparador
from core.bascula.models import Chofer, Cliente, ClienteProducto, ConfigSerial, Movimiento, Producto, Vehiculo
from core.base.comserial import *
from core.base.models import Empresa
from core.security.mixins import PermissionMixin

#DJANGO
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from weasyprint import CSS, HTML

"""LISTADO DE MOVIMIENTO DE BASCULA"""
class MovimientoList(PermissionMixin,FormView):	
	model = Movimiento
	template_name = 'movimiento/list.html'
	permission_required = 'view_movimiento'
	form_class = SearchForm
	
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
		
	def post(self,request,*args,**kwargs):
		data ={}		
		try:
			action = request.POST['action']
			if action == 'search':
				data =[]
				start_date = request.POST['start_date']
				end_date = request.POST['end_date']
				cliente = request.POST.getlist('cliente') if 'cliente' in request.POST else None
				producto = request.POST.getlist('producto') if 'producto' in request.POST else None	
				vehiculo = request.POST.getlist('vehiculo') if 'vehiculo' in request.POST else None
				chofer = request.POST.getlist('chofer') if 'chofer' in request.POST else None

				cliente= ",".join(cliente) if cliente!=[''] else None
				producto = ",".join(producto) if producto!=[''] else None
				vehiculo= ",".join(vehiculo) if vehiculo!=[''] else None
				chofer = ",".join(chofer) if chofer!=[''] else None

				_where = "1 = 1"
				if cliente:
					_where += f" AND bascula_movimiento.cliente_id IN ({cliente})"
				if producto:
					_where += f" AND bascula_movimiento.producto_id IN ({producto})"
				if chofer:
					_where += f" AND bascula_movimiento.chofer_id IN ({chofer})"
				if vehiculo:
					_where += f" AND bascula_movimiento.vehiculo_id IN ({vehiculo})"
				# peso_salida__lte=0
				# qs = Movimiento.objects.filter()\
				# 					.extra(where=[_where])\
				# 					.order_by('id')
				
				search = Movimiento.objects.filter()
				if len(start_date) and len(end_date):
					search = search.filter(fecha__range=[start_date, end_date])\
									.extra(where=[_where])\
									.order_by('-id')
				for i in search:
					data.append(i.toJSON())
			else:	
				data['error']= 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		# return JsonResponse(data,safe=False)
		return HttpResponse(json.dumps(data), content_type='application/json')

	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = ' Movimiento de Bascula'
		context['create_url'] = reverse_lazy('movimiento_create')
		context['list_url'] = reverse_lazy('movimiento_list')
		context['entity'] = 'Movimiento'
		return context


"""CREAR MOVIMIENTO DE BASCULA"""
class MovimientoCreate(PermissionMixin,CreateView):
	model = Movimiento
	form_class=MovimientoEntradaForm
	success_url = reverse_lazy('movimiento_list')
	template_name = 'movimiento/create.html'
	permission_required = 'add_movimiento'	

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	
	def validate_data(self):
		data = {'valid': True}
		try:
			type = self.request.POST['type']
			obj = self.request.POST['obj'].strip()
			if type == 'nro_ticket':
				if not obj=='0': #Ticket Cero puede repetirse
					if Movimiento.objects.filter(nro_ticket=obj):
						data['valid'] = False
			elif type == 'peso_entrada':
				if float(obj) <= 0.00:
					data['valid'] = False
			elif type == 'vehiculo':
				if not Vehiculo.objects.filter(id=obj):
					data['valid'] = False
			elif type == 'chofer':
				if not Chofer.objects.filter(id=obj):
					data['valid'] = False
			elif type == 'cliente':
				if not Cliente.objects.filter(id=obj):
					data['valid'] = False
			elif type == 'producto':
				if not Producto.objects.filter(id=obj):
					data['valid'] = False
		except:
			pass
		return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']			
			if action == 'add':
				with transaction.atomic():
					form = self.get_form()
					data = form.save()
			elif action == 'validate_data':
				return self.validate_data()				
			elif action == 'create-vehiculo':
				with transaction.atomic():
					frmVehiculo = VehiculoForm(request.POST)
					data = frmVehiculo.save()
			elif action == 'create-chofer':
				with transaction.atomic():
					frmChofer = ChoferForm(request.POST)
					data = frmChofer.save()
			elif action == 'search_peso_tara_interno':
				data = {'peso':'0'}
				if request.POST['id']:
					vehiculo = Vehiculo.objects.filter(id=request.POST['id']).first()
					movimiento = Movimiento.objects.filter(fecha = datetime.datetime.now() ,
														vehiculo=vehiculo)\
												.order_by('-id')
					if movimiento:
						peso_tara = movimiento.first().peso_tara
						if peso_tara > 0:						
							data = {'peso':peso_tara}				
							# Retornamos data como diccionario y recuperos directo data['peso']
							# Si enviamos como lista de diccionarios debemos definir una lista 
							# data[] y usar append
							# data.append({'peso':movimiento.first().peso_tara}) y recuperar
							# data[0]['peso'], pero en este caso solo enviamos una clave y valor 											
						# print(data)
						else:

							data['error'] = 'Movimiento de Entrada ya está registrado para el vehiculo %s' % (vehiculo)

			elif action == 'search_producto_id':
				data = [{'id': '', 'text': '------------'}]
				for i in ClienteProducto.objects.values('producto__id','producto__codigo','producto__denominacion').filter(cliente_id=request.POST['id']):	
					data.append({'id': i['producto__id'], 'text': i['producto__codigo'] +" - "+ i['producto__denominacion']})
			
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		# return JsonResponse(data,safe=False)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Entrada Bascula'
		context['entity'] = 'Bascula'
		context['list_url'] = self.success_url
		context['action'] = 'add'
		context['sucursal'] = self.request.user.sucursal.id
		context['frmVehiculo'] = VehiculoForm()
		context['frmChofer'] = ChoferForm()
		context['puerto_bascula1'] = ConfigSerial.objects.get(cod__exact='BSC1').puerto
		context['puerto_bascula2'] = ConfigSerial.objects.get(cod__exact='BSC2').puerto
		return context


"""ACTUALIZAR MOVIMIENTO DE BASCULA"""
class MovimientoUpdate(PermissionMixin,UpdateView):
	model = Movimiento
	form_class=MovimientoSalidaForm
	success_url = reverse_lazy('movimiento_list')
	template_name = 'movimiento/create.html'
	permission_required = 'change_movimiento'
	
	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.tipo_salida = kwargs['tipo_salida']
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		# Una vez tenga PESO NETO ya no se puede modificar la salida
		try:		
			obj = self.model.objects.get(pk=self.kwargs['pk'],peso_neto__exact=0)
			return obj
		except self.model.DoesNotExist:
			raise Http404("INFORMACION: Movimiento de Bascula NO existe o ya fue realizada la SALIDA")

	def validate_data(self):
		data = {'valid': True}
		try:
			type = self.request.POST['type']
			obj = self.request.POST['obj'].strip()
			if type == 'nro_ticket':
				if not obj=='0': #Ticket Cero puede repetirse
					if Movimiento.objects.filter(nro_ticket=obj):
						data['valid'] = False
			elif type == 'peso_salida':
				if float(obj) <= 0.00:
					data['valid'] = False
			elif type == 'vehiculo':
				if not Vehiculo.objects.filter(id=obj):
					data['valid'] = False
			elif type == 'chofer':
				if not Chofer.objects.filter(id=obj):
					data['valid'] = False
			elif type == 'cliente':
				if not Cliente.objects.filter(id=obj):
					data['valid'] = False
			elif type == 'producto':
				if not Producto.objects.filter(id=obj):
					data['valid'] = False
		except:
			pass
		return JsonResponse(data)	


	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'edit':
				with transaction.atomic():					
					# max_nro_ticket = Movimiento.objects.aggregate(Max('nro_ticket'))['nro_ticket__max']
					# if max_nro_ticket is None:
					# 	max_nro_ticket = 0
					# movimiento.nro_ticket = max_nro_ticket + 1
					form = self.get_form()
					data = form.save()
					movimiento = self.get_object()
					if movimiento.peso_entrada > movimiento.peso_salida:
						movimiento.peso_neto = movimiento.peso_entrada - movimiento.peso_salida
						movimiento.peso_bruto = movimiento.peso_entrada
						movimiento.peso_tara = movimiento.peso_salida
					else:
						movimiento.peso_neto = movimiento.peso_salida - movimiento.peso_entrada
						movimiento.peso_bruto = movimiento.peso_salida
						movimiento.peso_tara = movimiento.peso_entrada
				
				movimiento.fec_salida = movimiento.fec_modificacion
				movimiento.save()
			elif action == 'validate_data':
				return self.validate_data()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = '%s %s' % ('Salida Bascula Camión',str(self.tipo_salida).capitalize())
		context['entity'] = 'Bascula'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		context['sucursal'] = self.request.user.sucursal.id
		context['frmVehiculo'] = VehiculoForm()
		context['frmChofer'] = ChoferForm()
		context['puerto_bascula1'] = ConfigSerial.objects.get(cod__exact='BSC1').puerto
		context['puerto_bascula2'] = ConfigSerial.objects.get(cod__exact='BSC2').puerto
		context['tipo_salida'] = self.tipo_salida
		return context

'''ELIMINAR MOVIMIENTO DE BASCULA'''
class MovimientoDelete(PermissionMixin, DeleteView):
	model = Movimiento
	template_name = 'bascula/movimiento/delete.html'
	success_url = reverse_lazy('movimiento_list')
	permission_required = 'delete_movimiento'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			self.get_object().delete()
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Notificación de eliminación'
		context['list_url'] = self.success_url
		return context

"""PRUEBAS DE LECTURA"""
def test_bascula(request):
	return render(
		request=request,
		template_name='bascula/bascula.html',
	)

"""OBTENER PESO DIRECTAMENTE DEL PUERTO SERIAL"""
@method_decorator(csrf_exempt)
def leer_puerto_serial(request,puerto):
	config = ConfigSerial.objects.get(puerto=puerto)	
	buffer = leerPuertoSerial(config)
	printSeparador()
	print('# BUFFER DATO DIRECTO SERIAL')	
	print(buffer)
	if 'error' in buffer:
		return JsonResponse({'error': buffer})
	if buffer:		
		data = getPeso(config,buffer)
	printSeparador()
	print('Resultado\t:', data)
	printSeparador()
	return JsonResponse({ 'peso': data })          

"""OBTENER PESO DE ARCHIVO TXT"""
@method_decorator(csrf_exempt)
def leer_peso_bascula(request):
	data = 0
	if os.path.exists("peso.txt"):
		with open("peso.txt", "r") as archivo:
			archivo.seek(0)
			linea = archivo.readline()
			print(linea)
			if linea: 
				data = float(linea[29:8])
				print(data)
				#os.remove("peso.txt")			
	return JsonResponse({ 'peso': data })          

def getPeso(config,buffer):
	"""OBTENER VALORES DEL BUFFER DE LA BASCULA 1"""
	if config.cod == 'BSC1': 
		pos_ini = buffer.find('+') + 1
		print('Posicion Inicial:', pos_ini)
		pos_fin = pos_ini + (config.pos_fin - config.pos_ini)
		print('Posicion Final\t:', pos_fin)
		return buffer[pos_ini:pos_fin]
	
	"""OBTENER VALORES DEL BUFFER DE LA BASCULA 2"""
	if config.cod == 'BSC2': 
		pos_ini = config.pos_ini
		print('Posicion Inicial:', pos_ini)
		pos_fin = config.pos_fin
		print('Posicion Final\t:', pos_fin)
		return buffer[pos_ini:pos_fin]


'''IMPRESION DE TICKET'''
class MovimientoPrint(View):
	success_url = reverse_lazy('movimiento_list')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	@method_decorator(csrf_exempt)
	def get_height_ticket(self):
		movimiento = Movimiento.objects.get(pk=self.kwargs['pk'])
		height = 180		
		# increment = movimiento.all().count() * 5.45
		increment = 1 * 5.45
		height += increment
		print(round(height))
		return round(height)		
	
	@method_decorator(csrf_exempt)
	def get(self, request, *args, **kwargs):
		data = {}
		try:
			movimiento = Movimiento.objects.filter(pk=self.kwargs['pk'],fec_impresion__isnull=True).first()
			if movimiento:
				if 'print_ticket' in request.GET:
					#Permitir imprimir una vez en la llamada de ajax
					pass					
				else:
					movimiento.fec_impresion = datetime.datetime.now()
					if movimiento.peso_neto > 0: 
						movimiento.save()
					context = {'movimiento': movimiento, 'company': Empresa.objects.first()}
					context['height'] = self.get_height_ticket()
					template = get_template('movimiento/ticket.html')
					html_template = template.render(context).encode(encoding="UTF-8")
					url_css = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.3.1/css/bootstrap.min.css')
					pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(
						stylesheets=[CSS(url_css)], presentational_hints=True)
					response = HttpResponse(pdf_file, content_type='application/pdf')
					# response['Content-Disposition'] = 'filename="generate_html.pdf"'
					return response
			else:
				data['info'] ='La impresión ya fue realizada'
				return HttpResponse(json.dumps(data), content_type='application/json')
			
		except Exception as e:
			print(str(e))
		return HttpResponseRedirect(self.success_url)
