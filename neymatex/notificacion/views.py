from neymatex.utils import calculate_pages_to_render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from neymatex.models import *
from seguridad.views import EmpleadoPermissionRequieredMixin
from firebase_admin import messaging

from .forms import NotificacionForm


# Create your views here.
class ListarNotificaciones(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, ListView):
    paginate_by = 20
    max_pages_render = 10
    model = Notificacion
    context_object_name = 'notificaciones'
    template_name = "lista_notificacion.html"
    permission_required = 'neymatex.view_notificacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Notificaciones"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context


class CrearNotificacion(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, CreateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'notificacion_nueva.html'
    title = "Enviar Notificacion"
    success_url = reverse_lazy('neymatex:notificacion:listar')
    permission_required = 'neymatex.add_notificacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            notificacion = form.save()
            for usuario in User.objects.filter(groups__in=notificacion.grupo_usuarios.all()):
                notificacion.usuarios.add(usuario)
            # TODO: Implementar funcion para el envio de notificaciones push
            messages.success(request, "Notificación enviada con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response({"form": form, "title": self.title})


@ login_required()
def notificacion_reenviar(request, pk):
    notificacion = Notificacion.objects.get(id=pk)
    if request.POST:
        # TODO: Implementar funcion para el envio de notificaciones push
        messages.success(request, "Notificación reenviada con éxito.")
        return redirect('neymatex:notificacion:listar')
    return render(request, "ajax/notificacion_reenviar.html", {"notificacion": notificacion})


def enviar_push_notifications(tokens, title, body, image, data={}):
    # 500 token per call, need to create diferrent batches
    max_notification = 500
    tokens_count = len(tokens)
    enviados = 0
    if tokens_count > max_notification:
        counter = 0
        last = 0
        while tokens_count > 0:
            last = counter
            if tokens_count >= max_notification:
                counter += max_notification
            else:
                counter += tokens_count
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                    image=image
                ),
                data=data,
                tokens=tokens[last:counter],
            )
            tokens_count -= max_notification
            response = messaging.send_multicast(message)
            enviados += response.success_count
    else:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
                image=image
            ),
            data=data,
            tokens=tokens,
        )
        response = messaging.send_multicast(message)
        enviados += response.success_count
    return enviados
