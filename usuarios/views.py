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
from farmApp.secret import PUSH_APP_ID, PUSH_SECRET_API_KEY
from farmApp.secret import APP_PATH_TERMINOS_PDF
from farmApp.secret import APP_OPENPAY_API_KEY, APP_OPENPAY_MERCHANT_ID, APP_OPENPAY_VERIFY_SSL_CERTS, \
    APP_OPENPAY_PRODUCTION


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

        card_conekta = CardConekta(card=card.id, name=card.holder_name, brand=card.brand, last4=card.card_number[:4],
                                   exp_year=card.expiration_year, active=True, exp_month=card.expiration_month,
                                   type=card.type, bank_name=card.bank_name, allows_payouts=card.allows_payouts,
                                   allows_charges=card.allows_charges)
        card_conekta.user = user
        card_conekta.save()
        message = "Usuario actualizado"
        error = False
        # import pdb; pdb.set_trace()
        # except conekta.ConektaError as e:
        # el cliente no pudo ser actualizado
        # message = e.message_to_purchaser
        # error = True
        # card_conekta = None
    else:
        # try:
        #  customer = conekta.Customer.create({
        # import pdb; pdb.set_trace()
        customer = openpay.Customer.create(name=user.first_name, last_name=user.last_name, email=user.email,
                                           phone_number=user.cell)
        ConektaUser.objects.create(user=user, conekta_user=customer.id)
        message = "Usuario creado"

        # card = customer.createCard({"token_id": data['conektaTokenId']})
        card = customer.cards.create(token_id=data['token_id'], device_session_id=data['device_session_id'])

        card_conekta = CardConekta(card=card.id, name=card.holder_name, brand=card.brand, last4=card.card_number[:4],
                                   exp_year=card.expiration_year, active=True, exp_month=card.expiration_month,
                                   type=card.type, bank_name=card.bank_name, allows_payouts=card.allows_payouts,
                                   allows_charges=card.allows_charges)
        card_conekta.user = user
        card_conekta.save()
        # import pdb; pdb.set_trace()
        # except conekta.ConektaError as e:
        # el cliente no pudo ser creado
    #    message = e.message_to_purchaser
        error = True
    #    card_conekta = None
    if card_conekta is not None:
        data = dict(id=card_conekta.id, card=card_conekta.card, brand=card_conekta.brand, last4=card_conekta.last4,
                    active=card_conekta.active, exp_year=card_conekta.exp_year, exp_month=card_conekta.exp_month,
                    allows_payouts=card_conekta.allows_payouts, allows_charges=card_conekta.allows_charges,
                    bank_name=card_conekta.bank_name, type=card_conekta.type)
    else:
        data = {}
    return Response({"message": message, "card": data, "error": error})


def login_frontend(request):
    if request.method == "POST":
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
    data = json.loads(request.body)
    email = data['email']
    user = CustomUser.objects.get(email=email)
    if user is not None:
        enviar_mensaje = EmailRecoverPassword(user)
        enviar_mensaje.enviarMensaje()
        data = {'status': 'ok', 'message': 'Email enviado'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("Email enviado")


@csrf_exempt
def contacto(request):
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


@csrf_exempt
def upload_images_inapam(request):
    if request.method == 'POST':
        if request.is_ajax() is False:
            active = request.POST['active']
            iduser = request.POST['usuario']
            image = request.FILES['inapam']
            user = CustomUser.objects.get(pk=iduser)
            #  import pdb; pdb.set_trace()
            inapam = Inapam(active=active, user=user, inapam=image)
            inapam.save()
            data = {'status': 'ok', 'message': 'Carga exitosa'}
        else:
            data = {'status': 'bat', 'message': 'No esta permitido este metodo por post normal'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def calificaciones(request):
    if request.user.is_authenticated():
        ahora = datetime.datetime.now()
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

        paginator = Paginator(rating_list, 10)
        page = request.GET.get('page')

        try:
            ratings = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ratings = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            ratings = paginator.page(paginator.num_pages)

        return render(request, 'ratings.html', {"ratings": ratings, 'buenos': buenos, 'malos': malos, 'filter': filtro})
    else:
        return HttpResponseRedirect("/login/")


def reminders(request):
    now = datetime.datetime.now()
    weekDay = now.weekday()
    hour = request.GET.get('hour', now.hour)
    minute = request.GET.get('minute', now.minute)
    if weekDay == 0:
        reminders = Reminder.objects.filter(monday=True, time=datetime.time(hour, minute))
    elif weekDay == 1:
        reminders = Reminder.objects.filter(tuesday=True, time=datetime.time(hour, minute))
    elif weekDay == 2:
        reminders = Reminder.objects.filter(wednesday=True, time=datetime.time(hour, minute))
    elif weekDay == 3:
        reminders = Reminder.objects.filter(thursday=True, time=datetime.time(hour, minute))
    elif weekDay == 4:
        reminders = Reminder.objects.filter(friday=True, time=datetime.time(hour, minute))
    elif weekDay == 5:
        reminders = Reminder.objects.filter(saturday=True, time=datetime.time(hour, minute))
    elif weekDay == 6:
        reminders = Reminder.objects.filter(sunday=True, time=datetime.time(hour, minute))
    else:
        reminders = None

    for reminder in reminders:
        create_notification_reminder(reminder)

    return JsonResponse({'response': 'ok'});


def create_notification_reminder(reminder):
    tokens = [reminder.user.token_phone.all()[0].token]

    post_data = {
        "tokens": tokens,
        "production": "true",
        "notification": {
            "title": "Recordatorio de FarmaApp",
            "alert": reminder.message,
            "ios": {
                "payLoad": {
                    "notificationId": reminder.id
                }
            },
            "android": {
                "payLoad": {
                    "notificationId": reminder.id
                }
            }
        }
    }
    app_id = PUSH_APP_ID
    private_key = PUSH_SECRET_API_KEY
    url = "https://push.ionic.io/api/v1/push"
    req = urllib2.Request(url, data=json.dumps(post_data))
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Ionic-Application-Id", app_id)
    b64 = base64.encodestring('%s:' % private_key).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % b64)
    resp = urllib2.urlopen(req)
    return resp
