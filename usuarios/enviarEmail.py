#! /usr/bin/python
# -*- coding: UTF-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
import string
import random
from farmApp.secret import APP_EMAIL_HOST, APP_EMAIL_HOST_PASSWORD, APP_EMAIL_HOST_USER, \
    APP_EMAIL_PORT, APP_EMAIL_USE_TLS, APP_EMAIL_HOST_EMAIL


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Función para generar valores aleatorios
    Puede recibir:
        size = longitud de la cadena
            Defecto 6
        chars = caracteres a utilizar para buscar la cadena
            Defecto letras mayusculas y numeros
    """

    return ''.join(random.choice(chars) for _ in range(size))


class EmailUserCreated():
    user = None
    html = ""

    def __init__(self, user, sPassword):
        self.user = user
        t = loader.get_template('usuarioCreado.html')
        c = Context({'user': user, 'sPassword': sPassword})
        self.html = t.render(c)

    def enviarMensaje(self):
        subject = 'Registro de usuario en FarmaApp.mx'
        text_content = 'Registro de usuario'
        from_email = APP_EMAIL_HOST_EMAIL
        to = self.user.email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(self.html, "text/html")
        respuesta = msg.send()
        return respuesta


class EmailSolicitudRecoverPassword():
    user = None
    password = ""
    html = ""

    def __init__(self, user):
        self.user = user
        t = loader.get_template('recuperarContrasena.html')
        c = Context({'user': user, 'sPassword': self.password})
        self.html = t.render(c)

    def enviarMensaje(self):
        subject = 'Solicitud para reestablecer contraseña de FarmaApp.mx'
        text_content = 'Restablecer contraseña de usuario'
        from_email = APP_EMAIL_HOST_EMAIL
        to = self.user.email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(self.html, "text/html")
        respuesta = msg.send()
        return respuesta


class EmailRecoverPassword():
    user = None
    password = ""
    html = ""

    def __init__(self, user, password = ''):
        self.user = user
        if len(password) == 0:
            self.password = id_generator(8)
        else:
            self.password = password

        t = loader.get_template('recuperarContrasena.html')
        c = Context({'user': user, 'sPassword': self.password})
        self.html = t.render(c)

    def enviarMensaje(self):
        subject = 'Restablecio contraseña de FarmaApp.mx'
        text_content = 'Se reestableciio la contraseña de FarmaApp.mx'
        from_email = APP_EMAIL_HOST_EMAIL
        to = self.user.email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(self.html, "text/html")
        respuesta = msg.send()
        return respuesta


class EmailSendSale():
    user = None
    pedido = None
    detalle = None
    html = ""

    def __init__(self, pedido, detalles, user):
        self.user = user
        self.pedido = pedido
        self.detalles = detalles
        t = loader.get_template('sendSale.html')
        c = Context({'pedido': self.pedido, 'detalles': self.detalles, 'user': self.user})
        self.html = t.render(c)

    def enviarMensaje(self):
        subject = 'Compra realizada en FarmaApp.mx'
        text_content = 'Se envia detalle de la compra de FarmaApp.mx'
        from_email = APP_EMAIL_HOST_EMAIL
        to = self.user.email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(self.html, "text/html")
        respuesta = msg.send()
        return respuesta


class EmailContacto():
    name = ""
    email = ""
    phone = ""
    subject = ""
    message = ""
    html = ""

    def __init__(self, name, email, phone, subject, message):
        self.name = name
        self.email = email
        self.phone = phone
        self.subject = subject
        self.message = message
        t = loader.get_template('contacto.html')
        c = Context({'name': name, 'email': email, 'phone': phone, 'subject': subject, 'message': message})
        self.html = t.render(c)

    def enviarMensaje(self):
        subject = 'Contacto desde la app FarmaApp'
        text_content = 'Envio de mensaje desde app'
        from_email = APP_EMAIL_HOST_EMAIL
        # to = 'info@farmaapp.mx'
        to = 'richpolis@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(self.html, "text/html")
        respuesta = msg.send()
        return respuesta
