# -*- encoding: utf-8 -*-
import base64
import json
import urllib2
import datetime
# import conekta
import openpay
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from usuarios.models import ConektaUser, CustomUser, Inapam, Rating, CardConekta, Reminder
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from usuarios.enviarEmail import EmailUserCreated, EmailSolicitudRecoverPassword, \
    EmailRecoverPassword, EmailContacto
from django.views.decorators.csrf import csrf_exempt
from farmApp.secret import APP_PATH_TERMINOS_PDF, APP_GCM_API_KEY, PUSH_APP_ID, PUSH_SECRET_API_KEY
from farmApp.secret import APP_OPENPAY_API_KEY, APP_OPENPAY_MERCHANT_ID, APP_OPENPAY_VERIFY_SSL_CERTS, \
    APP_OPENPAY_PRODUCTION
from django.utils import timezone
from gcm import GCM

# Create your views here.
def home(request):
    return render(request, 'homepage.html')


def terminos(request):
    with open(APP_PATH_TERMINOS_PDF, 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=terminos.pdf'
        return response
    pdf.closed


@api_view(['POST'])
def user_conekta_create(request):
    openpay.api_key = APP_OPENPAY_API_KEY
    openpay.verify_ssl_certs = APP_OPENPAY_VERIFY_SSL_CERTS
    openpay.merchant_id = APP_OPENPAY_MERCHANT_ID
    openpay.production = APP_OPENPAY_PRODUCTION  # By default this works in sandbox mode, production = True

    #  conekta.api_key = "key_wHTbNqNviFswU6kY8Grr7w"

    user_conekta = None
    user = request.user
    try:
        user_conekta = ConektaUser.objects.get(user=user)
    except ConektaUser.DoesNotExist:
        user_conekta = None

    data = json.loads(request.body)
    # import pdb; pdb.set_trace()
    if user_conekta is not None:
        # try:
        # customer = conekta.Customer.find(user_conekta.conekta_user)
        customer = openpay.Customer.retrieve(user_conekta.conekta_user)

        # card = customer.createCard({"token_id": data['conektaTokenId']})
        card = customer.cards.create(token_id=data['token_id'], device_session_id=data['device_session_id'])

        if "id" in card:
            card_conekta = CardConekta(card=card.id, name=card.holder_name, brand=card.brand, last4=card.card_number[:4],
                                   exp_year=card.expiration_year, active=True, exp_month=card.expiration_month,
                                   type=card.type, bank_name=card.bank_name, allows_payouts=card.allows_payouts,
                                   allows_charges=card.allows_charges)
            card_conekta.user = user
            card_conekta.save()
            message = 'Usuario actualizado'
            error = False
        else:
            error = True
            message = card.description
            card_conekta = None
    else:
        customer = openpay.Customer.create(name=user.first_name, last_name=user.last_name, email=user.email,
                                           phone_number=user.cell)
        if "id" in customer:
            ConektaUser.objects.create(user=user, conekta_user=customer.id)
            message = 'Usuario creado'
            card = customer.cards.create(token_id=data['token_id'], device_session_id=data['device_session_id'])
            if "id" in card:
                card_conekta = CardConekta(card=card.id, name=card.holder_name, brand=card.brand, last4=card.card_number[:4],
                                           exp_year=card.expiration_year, active=True, exp_month=card.expiration_month,
                                           type=card.type, bank_name=card.bank_name, allows_payouts=card.allows_payouts,
                                           allows_charges=card.allows_charges)
                card_conekta.user = user
                card_conekta.save()
                error = False
            else:
                error = True
                message = card.description
                card_conekta = None
        else:
            error = True
            message = customer.description
            card_conekta = None

    if card_conekta is not None:
        data = dict(id=card_conekta.id, card=card_conekta.card, brand=card_conekta.brand, last4=card_conekta.last4,
                    active=card_conekta.active, exp_year=card_conekta.exp_year, exp_month=card_conekta.exp_month,
                    allows_payouts=card_conekta.allows_payouts, allows_charges=card_conekta.allows_charges,
                    bank_name=card_conekta.bank_name, type=card_conekta.type)
    else:
        data = {}
    return Response({"message": message, "card": data, "error": error})


def login_frontend(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/backend/pedidos/")
            else:
                # Return a 'disabled account' error message
                return HttpResponseRedirect("/login/")
        else:
            # Return an 'invalid login' error message.
            return HttpResponseRedirect("/login/")
    else:
        return render(request, 'login_frontend.html')


@csrf_exempt
def user_created(request):
    data = json.loads(request.body)
    email = data['email']
    password = data['pass']
    user = CustomUser.objects.get(email=email)
    if user is not None:
        enviar_mensaje = EmailUserCreated(user, password)
        enviar_mensaje.enviarMensaje()
    return HttpResponse("Email enviado")


@csrf_exempt
def solicitud_recover_password(request):
    #  import pdb; pdb.set_trace()
    data = json.loads(request.body)
    email = data['email']
    user = CustomUser.objects.get(email=email)
    if user is not None:
        enviar_mensaje = EmailSolicitudRecoverPassword(user)
        enviar_mensaje.enviarMensaje()
        data = {'status': 'ok', 'message': 'Email enviado'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("Email enviado")


@csrf_exempt
def recover_password(request):
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        username = request.POST['username']
        password = request.POST['password']
        repeat = request.POST['repeat']
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            user = None

        if user is None:
            data = {'status': 'bat', 'message': 'El usuario no existe'}
        elif password != repeat:
            data = {'status': 'bat', 'message': 'Las contraseñas no son iguales'}
        else:
            user.set_password(password)
            user.save()
            enviar_mensaje = EmailRecoverPassword(user, password)
            enviar_mensaje.enviarMensaje()
            data = {'status': 'ok', 'message': 'Se ha reestablecido la contraseña'}
        return render(request, 'recovery.html', {"username": username , "data": data})
    else:
        email = request.GET.get('email')
        data = {'status': '', 'message': ''}
        return render(request, 'recovery.html', {"username": email , "data": data})


@csrf_exempt
def contacto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        email = data['email']
        phone = data['phone']
        subject = data['subject']
        message = data['message']
        enviar_mensaje = EmailContacto(name, email, phone, subject, message)
        enviar_mensaje.enviarMensaje()
        data = {'status': 'ok', 'message': 'Email enviado'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        data = {'status': 'bat', 'message': 'Esta pagina no es accesible desde esta forma'}
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def upload_images_inapam(request):
    if request.method == 'POST':
        if request.is_ajax() is False:
            active = request.POST['active']
            iduser = request.POST['usuario']
            image = request.FILES['inapam']
            user = CustomUser.objects.get(pk=iduser)
            #  import pdb; pdb.set_trace()
            inapam = Inapam(active=active, user=user, image=image)
            inapam.save()
            data = {'status': 'ok', 'message': 'Carga exitosa'}
        else:
            data = {'status': 'bat', 'message': 'No esta permitido este metodo por post normal'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def calificaciones(request):
    if request.user.is_authenticated():
        ahora =  timezone.localtime(timezone.now())
        filtro = request.GET.get('filter', 'todos')
        #  print filtro
        year = request.GET.get('year', ahora.year)
        month = request.GET.get('month', ahora.month)

        #  buenos = Rating.objects.filter(created__year=year).filter(created__month=month).filter(rating__gte=4).count()
        #  malos = Rating.objects.filter(created__year=year).filter(created__month=month).filter(rating__lte=3).count()

        buenos = Rating.objects.filter(rating__gte=4).count()
        malos = Rating.objects.filter(rating__lte=3).count()

        #  import pdb; pdb.set_trace()

        if filtro == 'todos':
            rating_list = Rating.objects.filter(rating__gte=1).order_by('-created')
        elif filtro == 'malos':
            rating_list = Rating.objects.filter(rating__lte=3).order_by('-created')
        else:
            rating_list = Rating.objects.filter(rating__gte=4).order_by('-created')

        """paginator = Paginator(rating_list, 10)
        page = request.GET.get('page')

        try:
            ratings = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ratings = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            ratings = paginator.page(paginator.num_pages)"""

        return render(request, 'ratings.html', {'ratings': rating_list, 'buenos': buenos, 'malos': malos, 'filter': filtro})
    else:
        return HttpResponseRedirect('/login/')


def reminders(request):
    now = timezone.localtime(timezone.now())
    weekday = now.weekday()
    hour = request.GET.get('hour', now.hour)
    minute = request.GET.get('minute', now.minute)
    if weekday == 0:
        reminders = Reminder.objects.filter(monday=True, time=datetime.time(hour, minute))
    elif weekday == 1:
        reminders = Reminder.objects.filter(tuesday=True, time=datetime.time(hour, minute))
    elif weekday == 2:
        reminders = Reminder.objects.filter(wednesday=True, time=datetime.time(hour, minute))
    elif weekday == 3:
        reminders = Reminder.objects.filter(thursday=True, time=datetime.time(hour, minute))
    elif weekday == 4:
        reminders = Reminder.objects.filter(friday=True, time=datetime.time(hour, minute))
    elif weekday == 5:
        reminders = Reminder.objects.filter(saturday=True, time=datetime.time(hour, minute))
    elif weekday == 6:
        reminders = Reminder.objects.filter(sunday=True, time=datetime.time(hour, minute))
    else:
        reminders = None

    for reminder in reminders:
        create_notification_ionic_push_reminder(reminder)

    return JsonResponse({'response': 'ok'})


def create_notification_reminder(reminder):
    gcm = GCM(APP_GCM_API_KEY)
    user = reminder.user
    registration_ids = [user.token_phone.all()[0].token]

    notification = {
        'title': reminder.title,
        'message': reminder.message,
        'payload': {
        	'reminderId': reminder.id
        }
    }

    response = gcm.json_request(registration_ids=registration_ids,
                                data=notification,
                                collapse_key='notificacion_reminder',
                                priority='high',
                                delay_while_idle=False)

    # Successfully handled registration_ids
    if response and 'success' in response:
        for reg_id, success_id in response['success'].items():
            print('Successfully sent notification for reg_id {0}'.format(reg_id))

    # Handling errors
    if 'errors' in response:
        for error, reg_ids in response['errors'].items():
            # Check for errors and act accordingly
            if error in ['NotRegistered', 'InvalidRegistration']:
                # Remove reg_ids from database
                token_phone = user.token_phone.all()[0]
                token_phone.delete()
            elif error in ['Unavailable', 'InternalServerError']:
                from usuarios.models import Notifications
                token_phone = user.token_phone.all()[0]
                Notifications.objects.create(token_phone=token_phone, title=reminder.title, message=reminder.message)

    # Repace reg_id with canonical_id in your database
    if 'canonical' in response:
        for reg_id, canonical_id in response['canonical'].items():
            print("Replacing reg_id: {0} with canonical_id: {1} in db".format(reg_id, canonical_id))
            token_phone = user.token_phone.all()[0]
            token_phone.token = canonical_id
            token_phone.save()

    return response



def create_notification_ionic_push_reminder(reminder):
    return create_notification_reminder(reminder)
    
    user = reminder.user
    tokens = [user.token_phone.all()[0].token]
    post_data = {
        "tokens": tokens,
        "profile": PUSH_APP_ID,
        "notification": {
            "title": reminder.title,
            "alert": reminder.message,
            "android": {
                "payload": {
                    "reminderId": reminder.id
                },
                "collapse_key": "FarmaApp_reminder"
            },
            "ios": {
                "payload": {
                    "reminderId": reminder.id
                }
            }
        }
    }
    app_id = PUSH_APP_ID
    private_key = PUSH_SECRET_API_KEY
    url = "https://api.ionic.io/push/notifications"
    req = urllib2.Request(url, data=json.dumps(post_data))
    req.add_header("Content-Type", "application/json")
    #  req.add_header("X-Ionic-Application-Id", app_id)
    b64 = base64.encodestring('%s:' % private_key).replace('\n', '')
    req.add_header("Authorization", "Bearer %s" % b64)
    resp = urllib2.urlopen(req)
    return resp


def inapams(request):
    if request.user.is_authenticated():

        filtro = request.GET.get('filter', 'todos')

        activos = Inapam.objects.filter(user__inapam=True).count()
        inactivos = Inapam.objects.filter(user__inapam=False).count()

        #  import pdb; pdb.set_trace()

        if filtro == 'todos':
            inapams_list = Inapam.objects.all().order_by('-created')
        elif filtro == 'activos':
            inapams_list = Inapam.objects.filter(user__inapam=True).order_by('-created')
        else:
            inapams_list = Inapam.objects.filter(user__inapam=False).order_by('-created')

        """paginator = Paginator(inapams_list, 10)
        page = request.GET.get('page')

        try:
            registros = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            registros = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            registros = paginator.page(paginator.num_pages)"""
        return render(request, 'inapams.html', {'registros': inapams_list, 'activos': activos, 'inactivos': inactivos, 'filter': filtro})
    else:
        return HttpResponseRedirect("/login/")

@csrf_exempt
def inapams_approve(request, inapam_id):
    if request.method == 'POST':
        if request.is_ajax() is True:
            inapam = Inapam.objects.get(pk=inapam_id)
            user = inapam.user
            user.inapam = True
            inapam.active = True
            inapam.vendor = request.user
            user.save()
            inapam.save()
            create_notification_ionic_push_inapam(inapam, "Inapam", "Tu registro fue autorizado")
            return render(request, 'item_inapam.html', {"registro": inapam})
        else:
            data = {'status': 'bat', 'message': 'No esta autorizado otro metodo'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def inapams_update(request, inapam_id):
    if request.method == 'POST':
        if request.is_ajax() is True:
            inapam = Inapam.objects.get(pk=inapam_id)
            user = inapam.user
            user.inapam = False
            inapam.active = False
            inapam.vendor = request.user
            user.save()
            inapam.save()
            create_notification_ionic_push_inapam(inapam, "Inapam", "Tu credencial necesita ser actualizada, favor de subir nuevamente la imagen")
            return render(request, 'item_inapam.html', {"registro": inapam})
        else:
            data = {'status': 'bat', 'message': 'No esta autorizado otro metodo'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def inapams_reject(request, inapam_id):
    if request.method == 'POST':
        if request.is_ajax() is True:
            inapam = Inapam.objects.get(pk=inapam_id)
            user = inapam.user
            user.inapam = False
            inapam.active = False
            inapam.vendor = request.user
            user.save()
            inapam.save()
            create_notification_ionic_push_inapam(inapam, "Inapam", "Tu registro no fue autorizado")
            inapam.remove()
            data = {'status': 'ok', 'message': 'El registro se ha eliminado'}
        else:
            data = {'status': 'bat', 'message': 'No esta autorizado otro metodo'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def create_notification_inapam(inapam, title, message):
    gcm = GCM(APP_GCM_API_KEY)
    user = inapam.user
    registration_ids = [user.token_phone.all()[0].token]

    notification = {
        'title': title,
        'message': message,
        'payload': {
        	'inapam': True
        }
    }

    response = gcm.json_request(registration_ids=registration_ids,
                                data=notification,
                                collapse_key='notificacion_inapam',
                                priority='high',
                                delay_while_idle=False)

    # Successfully handled registration_ids
    if response and 'success' in response:
        for reg_id, success_id in response['success'].items():
            print('Successfully sent notification for reg_id {0}'.format(reg_id))

    # Handling errors
    if 'errors' in response:
        for error, reg_ids in response['errors'].items():
            # Check for errors and act accordingly
            if error in ['NotRegistered', 'InvalidRegistration']:
                # Remove reg_ids from database
                token_phone = user.token_phone.all()[0]
                token_phone.delete()
            elif error in ['Unavailable', 'InternalServerError']:
                from usuarios.models import Notifications
                token_phone = user.token_phone.all()[0]
                Notifications.objects.create(token_phone=token_phone, title=reminder.title, message=reminder.message)

    # Repace reg_id with canonical_id in your database
    if 'canonical' in response:
        for reg_id, canonical_id in response['canonical'].items():
            print("Replacing reg_id: {0} with canonical_id: {1} in db".format(reg_id, canonical_id))
            token_phone = user.token_phone.all()[0]
            token_phone.token = canonical_id
            token_phone.save()

    return response


def create_notification_ionic_push_inapam(register, title, message):
    return create_notification_inapam(register, title, message)
    user = register.user
    tokens = [user.token_phone.all()[0].token]
    post_data = {
        "tokens": tokens,
        "profile": PUSH_APP_ID,
        "notification": {
            "title": title,
            "alert": message,
            "android": {
                "payload": {
                    "inapam": True
                },
                "collapse_key": "FarmaApp_inapam"
            },
            "ios": {
                "payload": {
                    "inapam": True
                }
            }
        }
    }
    app_id = PUSH_APP_ID
    private_key = PUSH_SECRET_API_KEY
    url = "https://api.ionic.io/push/notifications"
    req = urllib2.Request(url, data=json.dumps(post_data))
    req.add_header("Content-Type", "application/json")
    #  req.add_header("X-Ionic-Application-Id", app_id)
    b64 = base64.encodestring('%s:' % private_key).replace('\n', '')
    req.add_header("Authorization", "Bearer %s" % b64)
    resp = urllib2.urlopen(req)
    return resp