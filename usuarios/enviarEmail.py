#! /usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template import loader, Context
import string
import random


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
        msg = MIMEMultipart('alternative')
        part2 = MIMEText(self.html, 'html', _charset='UTF-8')
        msg['Subject'] = 'Registro de usuario en FarmaApp.mx'
        msg['From'] = 'noreply@farmaapp.mx'
        msg['To'] = self.user.email

        msg.attach(part2)

        server = smtplib.SMTP('smtp.webfaction.com')
        server.starttls()
        server.login("noreply@farmaapp.mx", "D3m3s1s1")

        respuesta = server.sendmail('noreply@farmaapp.mx', self.user.email, msg.as_string())
        server.quit()
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
        msg = MIMEMultipart('alternative')
        part2 = MIMEText(self.html, 'html', _charset='UTF-8')
        msg['Subject'] = 'Solicitud para reestablecer contraseña de FarmaApp.mx'
        msg['From'] = 'noreply@farmaapp.mx'
        msg['To'] = self.user.email

        msg.attach(part2)

        server = smtplib.SMTP('smtp.webfaction.com')
        server.starttls()
        server.login("noreply@farmaapp.mx", "D3m3s1s1")

        respuesta = server.sendmail('noreply@farmaapp.mx', self.user.email, msg.as_string())
        server.quit()
        return respuesta


class EmailRecoverPassword():
    user = None
    password = ""
    html = ""

    def __init__(self, user):
        self.user = user
        self.password = id_generator(8)
        t = loader.get_template('recuperarContrasena.html')
        c = Context({'user': user, 'sPassword': self.password})
        user.set_password(self.password)
        user.save()
        self.html = t.render(c)

    def enviarMensaje(self):
        msg = MIMEMultipart('alternative')
        part2 = MIMEText(self.html, 'html', _charset='UTF-8')
        msg['Subject'] = 'Restablecio contraseña de FarmaApp.mx'
        msg['From'] = 'noreply@farmaapp.mx'
        msg['To'] = self.user.email

        msg.attach(part2)

        server = smtplib.SMTP('smtp.webfaction.com')
        server.starttls()
        server.login("noreply@farmaapp.mx", "D3m3s1s1")

        respuesta = server.sendmail('noreply@farmaapp.mx', self.user.email, msg.as_string())
        server.quit()
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
        msg = MIMEMultipart('alternative')
        part2 = MIMEText(self.html, 'html', _charset='UTF-8')
        msg['Subject'] = 'Compra realizada en FarmaApp.mx'
        msg['From'] = 'noreply@farmaapp.mx'
        msg['To'] = self.user.email

        msg.attach(part2)

        server = smtplib.SMTP('smtp.webfaction.com')
        server.starttls()
        server.login("noreply@farmaapp.mx", "D3m3s1s1")

        respuesta = server.sendmail('noreply@farmaapp.mx', self.user.email, msg.as_string())
        server.quit()
        return respuesta


class EmailContacto():
    name = ""
    email = ""
    phone = ""
    subject = ""
    message = ""
    html = ""

    def __init__(self, name,email,phone,subject,message):
        self.name = name
        self.email = email
        self.phone = phone
        self.subject = subject
        self.message = message
        t = loader.get_template('contacto.html')
        c = Context({'name': name, 'email': email, 'phone': phone, 'subject': subject, 'message': message})
        self.html = t.render(c)

    def enviarMensaje(self):
        msg = MIMEMultipart('alternative')
        part2 = MIMEText(self.html, 'html', _charset='UTF-8')
        msg['Subject'] = 'Compra realizada en FarmaApp.mx'
        msg['From'] = 'noreply@farmaapp.mx'
        msg['To'] = self.email

        msg.attach(part2)

        server = smtplib.SMTP('smtp.webfaction.com')
        server.starttls()
        server.login("noreply@farmaapp.mx", "D3m3s1s1")

        respuesta = server.sendmail(self.email, 'noreply@farmaapp.mx', msg.as_string())
        server.quit()
        return respuesta