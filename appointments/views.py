from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives, mail_admins, \
    mail_managers  # импортируем класс для создание объекта письма с html
from datetime import datetime

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст


from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        mail_managers(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )
        return redirect('make_appointment')

        # получаем наш html
        html_content = render_to_string(
        'appointments_created.html',
        {
        'appointment': appointment,
        }
        )

        msg = EmailMultiAlternatives(
        subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        body=appointment.message,  # это то же, что и message
        from_email='nick.muravscky2013@yandex.ru',
        to=['nmuravskij681@gmail.com'],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()
