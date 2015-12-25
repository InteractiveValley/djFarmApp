import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from usuarios.models import ConektaUser, CustomUser, Inapam
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from usuarios.enviarEmail import EmailUserCreated, EmailSolicitudRecoverPassword, \
    EmailRecoverPassword, EmailContacto
from django.views.decorators.csrf import csrf_exempt
import conekta


# Create your views here.
def home(request):
    return render(request, 'homepage.html')


@api_view(['POST'])
def user_conekta_create(request):
    conekta.api_key = "key_wHTbNqNviFswU6kY8Grr7w"
    user_conekta = None
    user = request.user
    try:
        user_conekta = ConektaUser.objects.get(user=user)
    except user_conekta.DoesNotExist:
        user_conekta = None

    data = json.loads(request.body)
    # import pdb; pdb.set_trace()
    if user_conekta is not None:
        customer = conekta.Customer.find(user_conekta.conekta_user)
        card = customer.update({
            "cards": [data['conektaTokenId']]
        })
        message = "Usuario actualizado"
    else:
        customer = conekta.Customer.create({
            "name": user.get_full_name(),
            "email": user.email,
            "phone": user.cell,
            "cards": [data['conektaTokenId'], ]
        })
        ConektaUser.objects.create(user=user, conekta_user=customer.id)
        message = "Usuario creado"

    return Response({"message": message})


def login_frontend(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/pedidos/")
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
