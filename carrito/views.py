# -*- encoding: utf-8 -*-

import base64
import json
import urllib2
# import conekta
import openpay

from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from carrito.models import Sale, APPROVED, REJECTED, DELIVERED, PAID, NO_PAID, DetailSale, ImageSale
from usuarios.models import ConektaUser, CardConekta
from usuarios.enviarEmail import EmailSendSale
from django.views.decorators.csrf import csrf_exempt
from farmApp.secret import PUSH_APP_ID, PUSH_SECRET_API_KEY, APP_GCM_API_KEY
from farmApp.secret import APP_OPENPAY_API_KEY, APP_OPENPAY_MERCHANT_ID, APP_OPENPAY_VERIFY_SSL_CERTS, \
    APP_OPENPAY_PRODUCTION
from carrito.models import Receipt
from carrito.forms import ReceiptForm
from gcm import GCM


def pedidos(request):
    if request.user.is_authenticated():
        filtro = request.GET.get('filter', 'todos')

        if filtro == 'todos':
            sale_list = Sale.objects.order_by('-created').all()
        elif filtro == 'enviar':
            sale_list = Sale.objects.filter(status=APPROVED).order_by('-created')
        elif filtro == 'pagado':
            sale_list = Sale.objects.filter(status=PAID).order_by('-created')
        elif filtro == 'rechazado':
            sale_list = Sale.objects.filter(status=REJECTED).order_by('-created')

        paginator = Paginator(sale_list, 10)
        page = request.GET.get('page')

        try:
            sales = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            sales = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            sales = paginator.page(paginator.num_pages)

        return render(request, 'pedidos.html', {"pedidos": sales, "filter": filtro})
    else:
        return HttpResponseRedirect("/login/")


def detalle_pedido(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    detalles = DetailSale.objects.filter(sale=pedido.id)
    return render(request, 'detalle_pedido.html', {"pedido": pedido, 'detalles': detalles})


def pedido_ver_recetas(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    images = pedido.images.all()
    return render(request, 'ver_receta.html', {"pedido": pedido, 'images': images})


def detalle_aprobar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    pedido.status = APPROVED
    pedido.vendor = request.user
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
    message = "Tu orden #" + str(pedido.id).zfill(6) + " esta en camino"
    create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message)
    if request.is_ajax():
        template = "item_pedido.html"
    else:
        template = "detalle_pedido.html"

    return render(request, template, {"pedido": pedido, 'detalles': detalles})


def detalle_cancelar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    pedido.status = REJECTED
    pedido.vendor = request.user
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
    message = "Tu orden #" + str(pedido.id).zfill(6) + " ha sido cancelada."
    create_notification_carrito(pedido, pedido.user, "FarmaApp", message)
    if request.is_ajax():
        template = "item_pedido.html"
    else:
        template = "detalle_pedido.html"

    return render(request, template, {"pedido": pedido, 'detalles': detalles})


def detalle_rechazar_receta(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    pedido.status = REJECTED
    pedido.vendor = request.user
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
    message = "La receta de tu pedido #" + str(pedido.id).zfill(
        6) + " ha sido rechazada. Si lo deseas puedes volver a generar la orden."
    create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message)
    if request.is_ajax():
        template = "item_pedido.html"
    else:
        template = "detalle_pedido.html"

    return render(request, template, {"pedido": pedido, 'detalles': detalles})


def detalle_entregar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    pedido.status = DELIVERED
    pedido.vendor = request.user
    user_conekta = ConektaUser.objects.get(user=pedido.user)

    device_session_id = request.GET.get('device_session_id')

    # conekta.api_key = "key_wHTbNqNviFswU6kY8Grr7w"
    openpay.api_key = APP_OPENPAY_API_KEY
    openpay.verify_ssl_certs = APP_OPENPAY_VERIFY_SSL_CERTS
    openpay.merchant_id = APP_OPENPAY_MERCHANT_ID
    openpay.production = APP_OPENPAY_PRODUCTION  # By default this works in sandbox mode, production = True

    customer = openpay.Customer.retrieve(user_conekta.conekta_user)

    # import pdb; pdb.set_trace();
    card_conekta = pedido.card_conekta
    amount = pedido.total()
    detalles = pedido.detail_sales.all()
    lista = []
    """
    for detalle in detalles:
        dato = {
            "name": detalle.product.name,
            "description": detalle.product.description,
            "unit_price": detalle.price,
            "quantity": detalle.quantity,
            "sku": str(detalle.product.id),
            "type": "medicine"
        }
        lista.append(dato)
    """
    """
    charge = customer.charges.create({
        "description": "Pedido FarmaApp",
        "amount": amount,
        "currency": "MXN",
        "reference_id": "pedido-farmaapp-" + str(pedido.id),
        "card": card_conekta.card,
        "details": {
            "name": pedido.user.get_full_name(),
            "phone": pedido.user.cell,
            "email": pedido.user.email,
            "line_items": lista
        }
    })
    """
    charge = None
    if len(pedido.charge_conekta) == 0:
        charge = customer.charges.create(source_id=card_conekta.card, method="card", amount=amount,
                                         description="Pedido de FarmaApp", order_id="pedido-farmaapp-" + str(pedido.id),
                                         device_session_id=device_session_id)
    else:
        charge = customer.charges.retrieve(pedido.charge_conekta)

    #  import pdb; pdb.set_trace()

    if charge is None:
        pedido.status = NO_PAID
        pedido.save()
    elif charge.status == "completed":
        pedido.charge_conekta = charge.id
        pedido.status = PAID
        pedido.vendor = request.user
        pedido.save()
        pedido.discount_inventory()
        enviar_mensaje = EmailSendSale(pedido, detalles, pedido.user)
        enviar_mensaje.enviarMensaje()
        #  import pdb; pdb.set_trace()
        str_pedido = str(pedido.id).zfill(6)
        str_total = '{:20,.2f}'.format(pedido.total())
        message = "Tu orden #{0} con un monto de ${1} ha sido entregada.".format(str_pedido, str_total)
        create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message)
        # import pdb; pdb.set_trace()
    elif charge.status == "in_progress":
        pedido.charge_conekta = charge.id
        pedido.status = NO_PAID
        pedido.vendor = request.user
        pedido.save()
    elif charge.status == "failed":
        pedido.status = NO_PAID
        pedido.save()

    if request.is_ajax():
        template = "item_pedido.html"
    else:
        template = "detalle_pedido.html"

    return render(request, template, {"pedido": pedido, 'detalles': detalles})


def revisar_pago(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)

    user_conekta = ConektaUser.objects.get(user=pedido.user)

     # conekta.api_key = "key_wHTbNqNviFswU6kY8Grr7w"
    openpay.api_key = APP_OPENPAY_API_KEY
    openpay.verify_ssl_certs = APP_OPENPAY_VERIFY_SSL_CERTS
    openpay.merchant_id = APP_OPENPAY_MERCHANT_ID
    openpay.production = APP_OPENPAY_PRODUCTION  # By default this works in sandbox mode, production = True

    customer = openpay.Customer.retrieve(user_conekta.conekta_user)

    if len(pedido.charge_conekta) > 0:
        charge = customer.charges.retrieve(pedido.charge_conekta)
        # import pdb; pdb.set_trace()
        if charge.status == "completed":
            pedido.status = PAID
            pedido.vendor = request.user
            pedido.save()
            pedido.discount_inventory()
            detalles = pedido.detail_sales.all()
            enviar_mensaje = EmailSendSale(pedido, detalles, pedido.user)
            enviar_mensaje.enviarMensaje()
            str_pedido = str(pedido.id).zfill(6)
            str_total = '{:20,.2f}'.format(pedido.total())
            message = "Tu orden #{0} con un monto de ${1} ha sido entregada.".format(str_pedido, str_total)
            create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message)

    if request.is_ajax():
        template = "item_pedido.html"
    else:
        template = "detalle_pedido.html"

    return render(request, template, {"pedido": pedido, 'detalles': detalles})


def send_sale_for_email(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    user = pedido.user
    detalles = DetailSale.objects.filter(sale=pedido.id)
    # import pdb; pdb.set_trace()
    enviar_mensaje = EmailSendSale(pedido, detalles, user)
    enviar_mensaje.enviarMensaje()
    return HttpResponse("Email enviado")


@csrf_exempt
def upload_images_ventas(request):
    if request.method == 'POST':
        if request.is_ajax() is False:
            sale_id = request.POST['venta']
            image = request.FILES['receta']
            #  import pdb; pdb.set_trace()
            sale = Sale.objects.get(pk=sale_id)
            image_sale = ImageSale(sale=sale, image_recipe=image)
            image_sale.save()
            data = {'status': 'ok', 'message': 'Carga exitosa'}
        else:
            data = {'status': 'bat', 'message': 'No esta permitido este metodo por post normal'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def create_notification_carrito(sale, user, title, message):
    gcm = GCM(APP_GCM_API_KEY)

    registration_ids = [user.token_phone.all()[0].token]

    notification = {
        "title": title,
        "message": message,
        "saleId": sale.id
    }

    response = gcm.json_request(registration_ids=registration_ids,
                                data=notification,
                                collapse_key='notificacion_carrito',
                                priority='normal',
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
                Notifications.objects.create(token_phone=token_phone, title=title, message=message)

    # Repace reg_id with canonical_id in your database
    if 'canonical' in response:
        for reg_id, canonical_id in response['canonical'].items():
            print("Replacing reg_id: {0} with canonical_id: {1} in db".format(reg_id, canonical_id))
            token_phone = user.token_phone.all()[0]
            token_phone.token = canonical_id
            token_phone.save()


def create_notification_ionic_push_carrito(sale, user, title, message):
    tokens = [user.token_phone.all()[0].token]
    post_data = {
        "tokens": tokens,
        "notification": {
            "title": title,
            "alert": message,
            "android": {
                "payload": {
                    "saleId": sale.id
                }
            },
            "ios": {
                "payload": {
                    "saleId": sale.id
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


def recibos(request):
    if request.user.is_authenticated():
        receipt_list = Receipt.objects.order_by('-created').all()
        paginator = Paginator(receipt_list, 10)
        page = request.GET.get('page')
        try:
            receipts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            receipts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            receipts = paginator.page(paginator.num_pages)

        return render(request, 'recibos.html', {"receipts": receipts})
    else:
        return HttpResponseRedirect("/login/")


def post_recibos(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = ReceiptForm(request.POST)
            if form.is_valid():
                recibo = form.save(commit=False)
                recibo.user = request.user
                recibo.save()
                return redirect('carrito.views.recibos')
        else:
            form = ReceiptForm()
        return render(request, 'crear_recibo.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")
