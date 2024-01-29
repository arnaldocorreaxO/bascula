import os
from datetime import datetime
from django.http import FileResponse
from pyreportjasper import PyReportJasper
from crum import get_current_user
from config import conn, settings
from core.base.models import Empresa

class JasperReportBase:
	"""
	Clase base para la generación de informes JasperReports en Django.
	"""

	def __init__(self, report_dir='', report_name='', report_title='', filename='', params=None):
		"""
		Inicializa una instancia del informe.

		Args:
			report_dir (str): Directorio del informe.
			report_name (str): Nombre del informe.
			report_title (str): Título del informe.
			filename (str): Nombre del archivo.
			params (dict): Parámetros adicionales del informe.
		"""
		self.dbconn = conn.JASPER_PGSQL
		self.report_dir = report_dir
		self.report_name = report_name
		self.report_title = report_title
		self.filename = filename
		self.params = params or {}

	def get_report(self, output_format):
		"""
		Genera el informe en el formato especificado.

		Args:
			output_format (str): Formato de salida del informe ('pdf' o 'xls').
		"""
		self.input_file = os.path.join(settings.REPORTS_DIR, f'{self.report_name}.jrxml')
		self.output_file = os.path.join(settings.REPORTS_DIR, self.report_name)

		pyreportjasper = PyReportJasper()
		pyreportjasper.config(
			self.input_file,
			self.output_file,
			db_connection=self.dbconn,
			output_formats=[output_format],
			parameters=self._get_params(),
			locale='es_PY',
		)

		pyreportjasper.process_report()

	def _get_params(self):
		"""
		Obtiene los parámetros del informe.

		Returns:
			dict: Parámetros del informe.
		"""
		# Obtener la ruta del logo de la empresa
		logo_path = Empresa.objects.first().imagen.path

		# Convertir fechas de parámetros
		P_FECHA_DESDE = datetime.strptime(self.params['P_FECHA_DESDE'], '%Y-%m-%d').strftime('%d/%m/%Y')
		P_FECHA_HASTA = datetime.strptime(self.params['P_FECHA_HASTA'], '%Y-%m-%d').strftime('%d/%m/%Y')

		# Construir filtros de fecha y hora		
		filtro_fecha_hora = (
		f"<b>FECHA HORA DESDE:</b> {P_FECHA_DESDE} {self.params['P_HORA_SAL_DESDE']} <b>HASTA:</b>  {P_FECHA_HASTA} {self.params['P_HORA_SAL_HASTA']} <br>"
)
		# Crear información adicional para el informe
		reporte = self.report_name
		usuario = str(get_current_user().username)
		hoy = datetime.now()
		info = f"Impresión\n{reporte}\nFecha: {hoy.strftime('%d/%m/%Y')}\nHora: {hoy.strftime('%H:%M:%S')}\nUsuario: {usuario}"

		# Construir diccionario de parámetros
		params = {
			'P_LOGO': logo_path,
			'P_INFO': info,
			'P_RUTA': settings.REPORTS_DIR,
			'P_TITULO1': settings.REPORT_TITULO1 if settings.REPORT_TITULO1 else "",
			'P_TITULO2': settings.REPORT_TITULO2 if settings.REPORT_TITULO2 else "",
			'P_TITULO3': settings.REPORT_TITULO3 if settings.REPORT_TITULO3 else "",
			'P_TITULO4': self.report_title,
			'P_TITULO5': filtro_fecha_hora,
		}
		params.update(self.params)  # Actualizar con parámetros específicos del informe
		return params

	def render_to_response(self, output_format):
		"""
		Renderiza el informe y lo devuelve como una respuesta HTTP.

		Args:
			output_format (str): Formato de salida del informe ('pdf' o 'xls').

		Returns:
			django.http.FileResponse: Respuesta HTTP con el archivo del informe.
		"""
		self.get_report(output_format)
		filepath = f'{self.output_file}.{output_format}'

		if output_format == 'pdf':
			return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(filepath, 'rb'), content_type='application/vnd.ms-excel')
