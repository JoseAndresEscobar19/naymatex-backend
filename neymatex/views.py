import datetime
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.db.models.aggregates import Count
from django.http.response import JsonResponse
from django.shortcuts import render, resolve_url
from django.utils import timezone

from .models import *

# Admin.


class PersonalPermissionRequieredMixin(PermissionRequiredMixin, AccessMixin):
    raise_exception = False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


@login_required
def home(request):
    context = {
        'title': 'Principal',
    }
    return render(request, 'principal.html', context)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days+1)):
        yield start_date + datetime.timedelta(n)


def dashboard_filter_ventas(request):
    if request.GET:
        fecha_inicio = request.GET.get(
            'fecha_inicio', None)
        fecha_fin = request.GET.get(
            'fecha_fin', None)
        if fecha_fin and fecha_inicio:
            # Obtenemos data segun el rango de fechas
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
            labels = []
            dataset = []
            titulo = '# Ventas entre {} - {}'.format(
                str(fecha_inicio.date().strftime('%d/%m/%Y')), str(fecha_fin.date().strftime('%d/%m/%Y')))
            for fecha in daterange(fecha_inicio, fecha_fin):
                labels.append("{}/{}".format(fecha.day, fecha.month))
                dataset.append(Orden.objects.filter(
                    estado__in=[Orden.Status.PAID, Orden.Status.DES], fecha_pagado__date=fecha).count())
        else:
            # Obtenemos lo de la presente semana y lo del dia actual
            fecha_inicio = fecha_fin = timezone.now().astimezone().date()
            current_week = datetime.date.today().isocalendar()[1]
            domingo = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=1).count()
            lunes = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=2).count()
            martes = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=3).count()
            miercoles = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=4).count()
            jueves = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=5).count()
            viernes = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=6).count()
            sabado = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=7).count()
            titulo = '# Ventas esta semana'
            labels = ['Lunes', 'Martes', 'Miércoles',
                      'Jueves', 'Viernes', 'Sábado', 'Domingo']
            dataset = [lunes, martes, miercoles,
                       jueves, viernes, sabado, domingo]

        ventas_rango = Orden.objects.filter(estado__in=[Orden.Status.PAID, Orden.Status.DES],
                                            fecha_pagado__date__gte=fecha_inicio, fecha_pagado__date__lte=fecha_fin).count()
        ventas_metros_rollos_rango = Orden.objects.filter(estado__in=[Orden.Status.PAID, Orden.Status.DES],
                                                          fecha_pagado__date__gte=fecha_inicio, fecha_pagado__date__lte=fecha_fin).aggregate(total_metros=Sum('detalles__cantidad_metro'))
        venta_metros = ventas_metros_rollos_rango['total_metros'] or 0
        return JsonResponse({
            'data': {
                'ventas_metros': venta_metros,
                'ventas_rango': ventas_rango,
                'chart_title': titulo,
                'data_chart': {
                    'labels': labels,
                    'datasets': [{
                        'label': '# Ventas',
                        'data': dataset,
                        'backgroundColor': ["rgba(255, 99, 132, 0.2)"],
                        'borderColor': ["rgba(255, 99, 132, 1)"],
                        'borderWidth': 1,
                    }]
                }
            },
            'status': 200
        })
    else:
        return JsonResponse({
            'data': 'No es un método válido.',
            'status': 400
        })


def dashboard_filter_recaudacion(request):
    if request.GET:
        fecha_inicio = request.GET.get(
            'fecha_inicio', None)
        fecha_fin = request.GET.get(
            'fecha_fin', None)
        if fecha_fin and fecha_inicio:
            # Obtenemos data segun el rango de fechas
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
            labels = []
            dataset = []
            titulo = '$ Recaudado entre {} - {}'.format(
                str(fecha_inicio.date().strftime('%d/%m/%Y')), str(fecha_fin.date().strftime('%d/%m/%Y')))
            for fecha in daterange(fecha_inicio, fecha_fin):
                labels.append("{}/{}".format(fecha.day, fecha.month))
                dataset.append(Orden.objects.filter(
                    estado__in=[Orden.Status.PAID, Orden.Status.DES], fecha_pagado__date=fecha).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0)
        else:
            # Obtenemos lo de la presente semana y lo del dia actual
            fecha_inicio = fecha_fin = timezone.now().astimezone().date()
            current_week = datetime.date.today().isocalendar()[1]
            domingo = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=1).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0
            lunes = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=2).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0
            martes = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=3).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0
            miercoles = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=4).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0
            jueves = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=5).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0
            viernes = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=6).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0
            sabado = Orden.objects.filter(
                estado=Orden.Status.PAID, fecha_pagado__week=current_week, fecha_pagado__week_day=7).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0
            titulo = '$ Recaudado esta semana'
            labels = ['Lunes', 'Martes', 'Miércoles',
                      'Jueves', 'Viernes', 'Sábado', 'Domingo']
            dataset = [lunes, martes, miercoles,
                       jueves, viernes, sabado, domingo]
        dinero_rango = Orden.objects.filter(estado__in=[Orden.Status.PAID, Orden.Status.DES],
                                            fecha_pagado__date__gte=fecha_inicio, fecha_pagado__date__lte=fecha_fin).aggregate(total_dinero=Sum('valor_total'))['total_dinero'] or 0
        print(Producto.objects.annotate(num_ventas=Count(
            'detalles')).order_by('-num_ventas')[:5])
        print(Producto.objects.annotate(dinero_ventas=Count(
            'detalles__valor_total')).order_by('-dinero_ventas')[:5])
        return JsonResponse({
            'data': {
                'dinero_rango': "${:.2f}".format(dinero_rango),
                'chart_title': titulo,
                'data_chart': {
                    'labels': labels,
                    'datasets': [{
                        'label': '$ Recaudado',
                        'data': dataset,
                        'backgroundColor': ["rgba(0, 153, 51, 0.2)"],
                        'borderColor': ["rgba(0, 153, 51, 1)"],
                        'borderWidth': 1,
                    }]
                }
            },
            'status': 200
        })
    else:
        return JsonResponse({
            'data': 'No es un método válido.',
            'status': 400
        })


def dashboard_productos_mas_vendidor(request):
    if request.GET:
        return JsonResponse({
            'data': {
                'mas_ventas': "",
                "mas_dinero": ""
            }
        })
    else:
        return JsonResponse({
            'data': 'No es un método válido.',
            'status': 400
        })
