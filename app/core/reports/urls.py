from django.urls import path
from .views.bascula.views import *

urlpatterns = [    
    # REPORTES BASCULA    
    path('rpt_bascula001/', RptBascula001ReportView.as_view(), name='rpt_bascula001'),
    path('rpt_bascula002/', RptBascula002ReportView.as_view(), name='rpt_bascula002'),

]