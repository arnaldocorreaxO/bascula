import locale
import datetime
from django.db.models.aggregates import Count

from django.db.models.fields import FloatField
from django.db.models.query_utils import Q

from core.bascula.models import Categoria, Cliente, Movimiento, Producto
from core.base.models import Empresa
from core.dashboard.forms import DashboardForm
from core.security.models import Dashboard
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import TemplateView
from core.user.models import User

locale.setlocale(locale.LC_TIME, '')


class DashboardView(LoginRequiredMixin, TemplateView):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		self.usuario = User.objects.filter(id=self.request.user.id).first()
		return super().dispatch(request, *args, **kwargs)

	def get_template_names(self):
		dashboard = Dashboard.objects.filter()
		if dashboard.exists():
			if dashboard[0].layout == 1:
				return 'vtcpanel.html'
		return 'hztpanel.html'

	def get(self, request, *args, **kwargs):
		request.user.set_group_session()
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			sucursal = request.POST['sucursal']
			fecha = request.POST['fecha']
			# Convertir un string a datetime con formato 
			fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y')\
									 .strftime('%Y-%m-%d')
			fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')  

			if action == 'get_graph_1_1':
				info = []
				# hoy = datetime.datetime.now()
				now = fecha
				qs = Movimiento.objects.values('producto__denominacion') \
						.filter(sucursal=sucursal,fecha=now, peso_neto__gt=0)\
						.exclude(anulado=True)\
						.annotate(tot_recepcion=Sum('peso_neto', output_field=FloatField())) \
						.order_by('-tot_recepcion')
				for i in qs:
					info.append([i['producto__denominacion'],
								 i['tot_recepcion']/1000])
				# print(qs.query)
				data = {
					'name': 'Stock de Productos',
					'type': 'pie',
					'colorByPoint': True,
					'data': info,
				}
			elif action == 'get_graph_1_2':
				info = []
				data = []
				categorias=[]
				val_tot_toneladas_series=[]
				val_tot_toneladas_series_data=[]
				val_ctd_viajes_series=[]
				val_ctd_viajes_series_data=[]				
				'''MOVIMIENTO ASOCIADO'''
				suc_envio = 1  # Villeta
				suc_destino = 2  # Vallemi
				# print(self.request.user.sucursal.id)
				# print(term)
				if sucursal == '1':  # Usuario de Villeta
					suc_envio = 2  # Vallemi
					suc_destino = 1  # Villeta

				_where = '1=1'
				_where += f" AND bascula_movimiento.sucursal_id = {suc_envio} \
				AND bascula_movimiento.destino_id = {suc_destino} \
				AND bascula_movimiento.fecha <= '{fecha}' \
				AND bascula_movimiento.id NOT IN \
				(SELECT movimiento_padre FROM bascula_movimiento\
				WHERE movimiento_padre is NOT NULL)"

				qs = Movimiento.objects.extra(where=[_where])
				
				movi = qs.values('producto__denominacion', 'cliente__denominacion','transporte__denominacion') \
                                    .filter()\
                                    .annotate(tot_toneladas=Sum('peso_neto', output_field=FloatField()),
                                              ctd_viajes=Count(True)) \
                                    .order_by('-tot_toneladas')
				for i in movi:
					categorias.append(i['producto__denominacion']   + ' <br> ' +\
									  i['transporte__denominacion']    + ' <br> ' +\
									  i['cliente__denominacion'] + ' <br> ')
				
					# SERIES           
					val_tot_toneladas_series_data.append(i['tot_toneladas']/1000)          
					val_ctd_viajes_series_data.append(i['ctd_viajes'])
				
				val_tot_toneladas_series = {
					'name': 'Toneladas',
					'data': val_tot_toneladas_series_data,
					'dataLabels': {
											'enabled': 'true',
											'format': "<b>{point.y:.2f}",
											'style': {
												'fontSize': "20 + 'px'"
											}
										}
				}
				val_ctd_viajes_series = {
					'name': 'Viajes',
					'data': val_ctd_viajes_series_data,
					'dataLabels': {
											'enabled': 'true',
											'format': "<b>{point.y:.0f}",
											'style': {
												'fontSize': "20 + 'px'"
											}
										}
				}
				data = {
				'categories': categorias,
				'series': [val_tot_toneladas_series,val_ctd_viajes_series]
				}
				# print(data)
				

			elif action == 'get_graph_2':
				filtrar = request.POST['filtrar']
				data = []
				categorias=[]
				val_tot_recepcion_series=[]
				val_tot_recepcion_series_data=[]
				val_ctd_recepcion_series=[]
				val_ctd_recepcion_series_data=[]
				# now = datetime.datetime.now()
				now = fecha
				
				movi = Movimiento.objects\
							.values('producto__denominacion', 'cliente__denominacion','transporte__denominacion') \
							.filter(sucursal=sucursal,fecha=now, peso_neto__gt=0)\
							.exclude(anulado=True)\
							.annotate(tot_recepcion=Sum('peso_neto', output_field=FloatField()),
									  ctd_recepcion=Count(True)) \
							.order_by('-tot_recepcion')
				
				if filtrar =='true':
					# Filtar producto clinker que no sea interno
					movi = movi.filter(producto__exact=2)\
							   .exclude(transporte__exact=1)

				for i in movi:
					# CATEGORIAS DENOMINACION DE LOS PRODUCTOS + CLIENTES + TRANSPORTE
					categorias.append(i['producto__denominacion']   + ' <br> ' +\
									  i['transporte__denominacion']    + ' <br> ' +\
									  i['cliente__denominacion'] + ' <br> ')
					 # SERIES           
					val_tot_recepcion_series_data.append(i['tot_recepcion']/1000)          
					val_ctd_recepcion_series_data.append(i['ctd_recepcion'])
				
				val_tot_recepcion_series = {
					'name': 'Toneladas',
					'data': val_tot_recepcion_series_data,
					'dataLabels': {
											'enabled': 'true',
											'format': "<b>{point.y:.2f}",
											'style': {
												'fontSize': "20 + 'px'"
											}
										}
				}
				val_ctd_recepcion_series = {
					'name': 'Viajes',
					'data': val_ctd_recepcion_series_data,
					'dataLabels': {
											'enabled': 'true',
											'format': "<b>{point.y:.0f}",
											'style': {
												'fontSize': "20 + 'px'"
											}
										}
				}
				data = {
				'categories': categorias,
				'series': [val_tot_recepcion_series,val_ctd_recepcion_series]
				}
				# print(data)

			elif action == 'get_graph_3':
				data = []
				categorias=[]
				val_tot_recepcion_series=[]
				val_tot_recepcion_series_data=[]
				val_ctd_recepcion_series=[]
				val_ctd_recepcion_series_data=[]
				
				now = fecha
				month = now.month
				year = now.year    

				# Envia Vallemi recibe Villeta
				cliente_id = 2 #Vallemi
				destino_id = 1 #Villeta
				
				movimientos = Movimiento.objects\
							.values('fecha') \
							.filter( sucursal=sucursal,
									 cliente=cliente_id,
									 destino=destino_id,
									 producto=2, 
									 fecha__month=month, 
									 fecha__year=year,
									 peso_neto__gt=0)\
							.exclude(anulado=True)\
							.annotate(tot_recepcion=Sum('peso_neto', output_field=FloatField()),
									  ctd_recepcion=Count(True)) \
							.order_by('fecha')
				#.exclude(anulado=True)\ Este debe ir solo no combinar con otros campos la razon es que 
				# no genera de forma correcta el query 
				# NOT (anulado=True and otro_campo=1) 
				# esto es igual a (False and True) = False
				# print(movimientos.query)
				for mov in movimientos:
					# CATEGORIAS Dias 1 al 31
					categorias.append(mov['fecha'].strftime('%d'))
					# SERIES           
					val_tot_recepcion_series_data.append(mov['tot_recepcion']/1000)          
					val_ctd_recepcion_series_data.append(mov['ctd_recepcion'])
				   
				val_tot_recepcion_series = {
					'name': 'Toneladas',
					'data': val_tot_recepcion_series_data,
					'color':'#f9975d',
					'dataLabels': {
											'enabled': 'true',
											'format': "<b>{point.y:.2f}",
											'style': {
												'fontSize': "20 + 'px'"
											}
										}
				}
				val_ctd_recepcion_series = {
					'name': 'Viajes',
					'data': val_ctd_recepcion_series_data,
					 'color':'#090910',
					'dataLabels': {
											'enabled': 'true',
											'format': "<b>{point.y:.0f}",
											'style': {
												'fontSize': "20 + 'px'"
											}
										}
				}
				data = {
				'categories': categorias,
				'series': [val_tot_recepcion_series,val_ctd_recepcion_series]
				}
				# print(data)
				# data['series'] = data
				# print(data)
			elif action == 'get_graph_4':
				data = []
				categorias=[]
				val_tot_recepcion_series=[]
				val_tot_recepcion_series_data=[]
				val_ctd_recepcion_series=[]
				val_ctd_recepcion_series_data=[]
				
				now = fecha
				year = now.year

				# Envia Vallemi recibe Villeta
				cliente_id = 2 #Vallemi
				destino_id = 1 #Villeta

				movimientos = Movimiento.objects\
							.values('fecha__month') \
							.filter(sucursal=sucursal,
									cliente=cliente_id,
									destino=destino_id,
									producto=2, fecha__year=year, peso_neto__gt=0)\
							.exclude(cliente=1)\
							.exclude(anulado=True)\
							.annotate(tot_recepcion=Sum('peso_neto', output_field=FloatField()),
									  ctd_recepcion=Count(True)) \
							.order_by('fecha__month')
				for mov in movimientos:
					# CATEGORIAS MESES
					#Utilizamos una fecha cualquiera para retornar solo el mes ;)
					mes = datetime.date(1900, mov['fecha__month'], 1).strftime('%B').capitalize()
					categorias.append(mes)
					# SERIES           
					val_tot_recepcion_series_data.append(mov['tot_recepcion']/1000)          
					val_ctd_recepcion_series_data.append(mov['ctd_recepcion'])
				
				val_tot_recepcion_series = {
					'name': 'Toneladas',
					'data': val_tot_recepcion_series_data,
					'color':'#a9ff96',
					'dataLabels': {
											'enabled': 'true',
											'format': "<b>{point.y:.2f}",                          
											'style': {
												'fontSize': '14px'
											}
										}
				}
				val_ctd_recepcion_series = {
					'name': 'Viajes',
					'data': val_ctd_recepcion_series_data,
					'color':'#090910',
					'dataLabels': {
											'enabled': 'true',                                            
											'format': "<b>{point.y:.0f}",
											'style': {
												'fontSize': '14px'
											}
										}
				}
				data = {
				'categories': categorias,
				'series': [val_tot_recepcion_series,val_ctd_recepcion_series]
				}

				# print(data)

			elif action == 'get_graph_5':
				now = fecha
				qs = Movimiento.objects \
									.values('producto__denominacion', 'cliente__denominacion','transporte__denominacion') \
									.filter(sucursal=sucursal,fecha=now)\
									.exclude(anulado=True)\
									.annotate(vehiculo_entrada_count=Count('id'),
											  vehiculo_salida_count=Count('id', filter=Q(peso_neto__gt=0)),
											  vehiculo_pendiente_count=Count('id', filter=Q(peso_neto=0))) \
									.order_by('producto__denominacion')
				# print(dataset)

				categorias = list()
				vehiculo_entrada_series_data = list()
				vehiculo_salida_series_data = list()
				vehiculo_pendiente_series_data = list()

				for row in qs:
					text_denom = row['transporte__denominacion']
					if text_denom == 'DEL PROVEEDOR':
						text_denom = row['cliente__denominacion']                    

					categorias.append(
						'%s <br> %s' % (row['producto__denominacion'],
										text_denom
										))
					vehiculo_entrada_series_data.append(
						row['vehiculo_entrada_count'])
					vehiculo_salida_series_data.append(
						row['vehiculo_salida_count'])
					vehiculo_pendiente_series_data.append(
						row['vehiculo_pendiente_count'])

				vehiculo_entrada_series = {
					'name': 'Entraron',
					'data': vehiculo_entrada_series_data,
					# 'color': 'green'
				}

				vehiculo_salida_series = {
					'name': 'Salieron',
					'data': vehiculo_salida_series_data,
					# 'color': 'red'
				}

				vehiculo_pendiente_series = {
					'name': 'Pendientes',
					'data': vehiculo_pendiente_series_data,
					# 'color': 'red'
				}

				data = {
					'xAxis': {'categories': categorias},
					'series': [vehiculo_entrada_series, vehiculo_salida_series, vehiculo_pendiente_series]
				}			
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		usu_sucursal = self.usuario.sucursal.id
		context['title'] = 'Panel de administración'
		context['fecha_actual'] = datetime.datetime.today().strftime("%d/%m/%Y")
		context['fecha_hora_actual'] = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
		context['mes_actual'] = datetime.datetime.today().strftime("%B").capitalize()
		context['anho_actual'] = datetime.datetime.today().strftime("%Y")
		context['empresa'] = Empresa.objects.first()
		context['clientes'] = Cliente.objects.all().count()
		context['categorias'] = Categoria.objects.filter().count()
		context['productos'] = Producto.objects.all().count()
		context['movimientos'] = Movimiento.objects.filter(sucursal=usu_sucursal).order_by('-id')[0:10]   
		context['usuario'] = self.usuario
		context['form'] = DashboardForm()
		return context


@requires_csrf_token
def error_404(request, exception):
	return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
	return render(request, '500.html', {})
