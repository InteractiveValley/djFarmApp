# -*- coding: utf-8 -*- 
import os
import base64
import json
import urllib2
import urllib
import os
import openpay
import requests
from collections import OrderedDict

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from carrito.models import Sale, APPROVED, REJECTED, DELIVERED, PAID, NO_PAID, DetailSale, ImageSale, TYPE_RECEIPT, \
    TYPE_OBSOLETE, Send, DetailSend, TYPE_INACTIVADO, TYPE_WITHOUT_FOLIO, TYPE_RECIPE_NORMAL, TYPE_RECIPE_WITH_ANTIBIOTICO
from productos.models import Product
from usuarios.models import ConektaUser, CardConekta
from usuarios.enviarEmail import EmailSendSale
from django.views.decorators.csrf import csrf_exempt
from farmApp.secret import PUSH_APP_ID, PUSH_SECRET_API_KEY, APP_GCM_API_KEY
from farmApp.secret import APP_OPENPAY_API_KEY, APP_OPENPAY_MERCHANT_ID, APP_OPENPAY_VERIFY_SSL_CERTS, \
    APP_OPENPAY_PRODUCTION
from carrito.models import Receipt
from carrito.forms import ReceiptForm, SendForm, DetailSendForm
from gcm import GCM
from apns import APNs, Payload

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
            sales = paginator.page(1)
        except EmptyPage:
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
    if pedido.status != APPROVED:
        # pedido.status = APPROVED
        pedido.vendor = request.user
        user_conekta = ConektaUser.objects.get(user=pedido.user)

        device_session_id = request.GET.get('device_session')

        openpay.api_key = APP_OPENPAY_API_KEY
        openpay.verify_ssl_certs = APP_OPENPAY_VERIFY_SSL_CERTS
        openpay.merchant_id = APP_OPENPAY_MERCHANT_ID
        openpay.production = APP_OPENPAY_PRODUCTION
        customer = openpay.Customer.retrieve(user_conekta.conekta_user)

        card_conekta = pedido.card_conekta
        amount = "{0:.2f}".format(pedido.total)
        detalles = pedido.detail_sales.all()
        lista = []
        charge = None
        alertas = []
        try:
            if len(pedido.charge_conekta) == 0:
                charge = customer.charges.create(
                    source_id=card_conekta.card,
                    method="card",
                    currency="MXN",
                    amount=amount,
                    description="Pedido de FarmaApp",
                    order_id="pedido-" + str(pedido.id) + "-farmaapp",
                    device_session_id=device_session_id
                )
            else:
                charge = customer.charges.retrieve(pedido.charge_conekta)
        except Exception, e:
            print e
            alertas.append(
                "Ocurrio un error al realizar la transacción, detalle: {0}".format(str(e))
            )

        if charge is None:
            pedido.status = NO_PAID
            pedido.save()
        elif charge.status == "completed":
            pedido.charge_conekta = charge.id
            pedido.status = PAID
            pedido.vendor = request.user
            pedido.save()
            pedido.discount_inventory
            try:
                enviar_mensaje = EmailSendSale(pedido, detalles, pedido.user)
                enviar_mensaje.enviarMensaje()
            except Exception, e:
                print e
                alertas.append("Ocurrio un error al enviar el correo electronico")
            str_pedido = str(pedido.id).zfill(6)
            str_total = '{:20,.2f}'.format(pedido.total)
            message = "Tu orden #{0} con un monto de ${1} se ha cobrado y esta en camino a ser entregada.".format(str_pedido, str_total)
            try:
                create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message, amount)
            except Exception, e:
                alertas.append("Ocurrio un error al enviar la push notification")

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

    return render(request, template, {"pedido": pedido, 'detalles': detalles, 'alertas': alertas})


def detalle_cancelar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    if pedido.status != REJECTED:
        pedido.status = REJECTED
        pedido.vendor = request.user
        pedido.save()
        detalles = DetailSale.objects.filter(sale=pedido)
        message = "Tu orden #" + str(pedido.id).zfill(6) + " ha sido cancelada."
        create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message, 1)

    if request.is_ajax():
        template = "item_pedido.html"
    else:
        template = "detalle_pedido.html"

    return render(request, template, {"pedido": pedido, 'detalles': detalles})


def detalle_rechazar_receta(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    if pedido.status != REJECTED:
        pedido.status = REJECTED
        pedido.vendor = request.user
        pedido.save()
        detalles = DetailSale.objects.filter(sale=pedido)
        message = "La receta de tu pedido #" + str(pedido.id).zfill(6) + " ha sido rechazada. " + \
                  "Si lo deseas puedes volver a generar la orden."
        create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message, 1)

    if request.is_ajax():
        template = "item_pedido.html"
    else:
        template = "detalle_pedido.html"

    return render(request, template, {"pedido": pedido, 'detalles': detalles})


def detalle_entregar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    if pedido.status != DELIVERED:
        pedido.status = PAID
        pedido.vendor = request.user
        pedido.save()

        amount = "{0:.2f}".format(pedido.total)
        str_pedido = str(pedido.id).zfill(6)
        str_total = '{:20,.2f}'.format(pedido.total)
        message = "Tu orden #{0} con un monto de ${1} ha sido entregada.".format(str_pedido, str_total)
        try:
            create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message, amount)
        except Exception, e:
            alertas.append("Ocurrio un error al enviar la push notification")

    if request.is_ajax():
        template = "item_pedido.html"
    else:
        template = "detalle_pedido.html"

    return render(request, template, {"pedido": pedido, 'detalles': detalles, 'alertas': alertas})


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
            pedido.discount_inventory
            detalles = pedido.detail_sales.all()
            enviar_mensaje = EmailSendSale(pedido, detalles, pedido.user)
            enviar_mensaje.enviarMensaje()
            str_pedido = str(pedido.id).zfill(6)
            str_total = '{:20,.2f}'.format(pedido.total)
            message = "Tu orden #{0} con un monto de ${1} ha sido entregada.".format(str_pedido, str_total)
            create_notification_ionic_push_carrito(pedido, pedido.user, "FarmaApp", message, 1)

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
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        if request.is_ajax() is False:
            sale_id = request.POST['venta']
            image = request.FILES['receta']
            sale = Sale.objects.get(pk=sale_id)
            image_sale = ImageSale(sale=sale, image_recipe=image)
            image_sale.save()
            data = {'status': 'ok', 'message': 'Carga exitosa'}
        else:
            data = {'status': 'bat', 'message': 'No esta permitido este metodo por post normal'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def upload_images_base64_ventas(request):
    if request.method == 'POST':
        if request.is_ajax() is False:

            from django.core.files.base import ContentFile

            datos = json.loads(request.body)
            sale_id = int(datos['venta'])
            receta = datos['receta']
            imgdata = base64.b64decode(receta)

            sale = Sale.objects.get(pk=sale_id)
            image_sale = ImageSale(sale=sale)
            image_sale.image_recipe = ContentFile(
                imgdata, "imageToSave" + str(sale_id) + ".png"
            )
            image_sale.save()

            # os.remove("imageToSave" + str(sale_id) + ".png")
            data = {'status': 'ok', 'message': 'Carga exitosa'}
        else:
            data = {
                'status': 'bat',
                'message': 'No esta permitido este metodo por post normal'
            }
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def create_notification_carrito(sale, user, title, message):
    gcm = GCM(APP_GCM_API_KEY)
    registration_ids = [user.token_phone.all()[0].token]

    notification = {
        "title": title,
        "message": message,
        "payload": {
            "saleId": sale.id,
            "status_string": sale.show_status()
        }
    }

    response = gcm.json_request(registration_ids=registration_ids,
                                data=notification,
                                collapse_key='notificacion_carrito',
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
                Notifications.objects.create(token_phone=token_phone, title=title, message=message)

    # Repace reg_id with canonical_id in your database
    if 'canonical' in response:
        for reg_id, canonical_id in response['canonical'].items():
            print("Replacing reg_id: {0} with canonical_id: {1} in db".format(reg_id, canonical_id))
            token_phone = user.token_phone.all()[0]
            token_phone.token = canonical_id
            token_phone.save()

    return response


def noti_ios(token, message, customPayload):
    print "Entro a la push de ios"
    apns = APNs(
        use_sandbox=False,
        cert_file='./certiAyuda.pem',
        key_file='./push-pro-key-out.pem'
    )
    print token
    payload = Payload(
        alert=message,
        sound="default",
        badge=1,
        custom=customPayload
    )
    print payload
    apns.gateway_server.send_notification(token, payload)


def push_ios(token, message, valuePayload, typePayload):
    params = OrderedDict([
        ('token_device', token),
        ('message', message),
        ('type', typePayload),
        ('value', valuePayload)
    ])
    r_push = requests.get(
        "http://push-farmapp.159.203.202.11.nip.io",
        params=urllib.urlencode(params)
    )
    print r_push.json


def create_notification_ionic_push_carrito(sale, user, title, message, typePush=0):
    if len(user.token_phone.all()[0].token) == 64:
        return push_ios(
            user.token_phone.all()[0].token,
            message,
            sale.id,
            typePush
        )
    else:
        return create_notification_carrito(sale, user, title, message)

    tokens = [user.token_phone.all()[0].token]
    post_data = {
        "tokens": tokens,
        "profile": PUSH_APP_ID,
        "notification": {
            "title": title,
            "message": message,
            "android": {
                "payload": {
                    "saleId": sale.id,
                    "status_string": sale.show_status()
                },
                "collapse_key": "FarmaApp_carrito"
            },
            "ios": {
                "payload": {
                    "saleId": sale.id,
                    "status_string": sale.show_status()
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
    b64 = base64.encodestring('%s' % private_key).replace('\n', '')
    req.add_header("Authorization", "Bearer %s" % b64)
    resp = urllib2.urlopen(req)
    return resp


def recibos(request):
    if request.user.is_authenticated():
        filter = request.GET.get('filter', 'todos')

        product_id = request.GET.get('product', '')

        if len(product_id) > 0:
            request.session['product_id'] = product_id

        if 'product_id' in request.session:
            product_id = int(request.session['product_id'])
            if product_id > 0:
                product = Product.objects.get(pk=product_id)
            else:
                product = None
        else:
            product = None

        if filter == 'todos':
            if not product is None:
                receipt_list = Receipt.objects.filter(product=product, type_receipt=TYPE_RECEIPT).order_by('-created')
            else:
                receipt_list = Receipt.objects.filter(type_receipt=TYPE_RECEIPT).order_by('-created')
        elif filter == 'por_caducar':
            if not product is None:
                receipt_list = Receipt.objects.filter(product=product, type_receipt=TYPE_RECEIPT).order_by(
                    '-date_expiration')
            else:
                receipt_list = Receipt.objects.filter(type_receipt=TYPE_RECEIPT).order_by('-date_expiration')
        elif filter == 'caduco':
            if not product is None:
                receipt_list = Receipt.objects.filter(product=product, type_receipt=TYPE_OBSOLETE).order_by('-created')
            else:
                receipt_list = Receipt.objects.filter(type_receipt=TYPE_OBSOLETE).order_by('-created')
        elif filter == 'inactivo':
            if not product is None:
                receipt_list = Receipt.objects.filter(product=product, type_receipt=TYPE_INACTIVADO).order_by('-created')
            else:
                receipt_list = Receipt.objects.filter(type_receipt=TYPE_INACTIVADO).order_by('-created')

        """paginator = Paginator(receipt_list, 10)
        page = request.GET.get('page')
        try:
            receipts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            receipts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            receipts = paginator.page(paginator.num_pages)"""
        if not product is None:
            return render(request, 'recibos.html',
                          dict(receipts=receipt_list, product=product, filter=filter, TYPE_RECEIPT=TYPE_RECEIPT,
                               TYPE_INACTIVADO=TYPE_INACTIVADO))
        else:
            return render(request, 'recibos.html',
                          dict(receipts=receipt_list, product={'id': 0}, filter=filter, TYPE_RECEIPT=TYPE_RECEIPT,
                               TYPE_INACTIVADO=TYPE_INACTIVADO))
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
            product_id = request.GET.get('product', '')
            if int(product_id) > 0:
                product = Product.objects.get(pk=int(product_id))
                form = ReceiptForm(initial={'product': product})
            else:
                form = ReceiptForm()
        return render(request, 'crear_recibo.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")


def recibo_inactivado(request, receipt_id):
    if request.user.is_authenticated():
        recibo = Receipt.objects.get(pk = receipt_id)
        recibo.type_receipt = TYPE_INACTIVADO
        recibo.status = False
        recibo.save()
        data = {'status': 'ok', 'message': 'Se ha realizado la actualizacion solicitada'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect("/login/")


def recibo_activado(request, receipt_id):
    if request.user.is_authenticated():
        recibo = Receipt.objects.get(pk = receipt_id)
        recibo.type_receipt = TYPE_RECEIPT
        recibo.status = False
        recibo.save()
        data = {'status': 'ok', 'message': 'Se ha realizado la actualizacion solicitada'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect("/login/")


def envios(request):
    if request.user.is_authenticated():
        send_list = Send.objects.order_by('-created').filter(status=False)

        return render(request, 'envios.html', {"sends": send_list})

    else:
        return HttpResponseRedirect("/login/")


def post_envios(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = SendForm(request.POST)
            if form.is_valid():
                envio = form.save(commit=False)
                envio.vendor = request.user
                venta = envio.sale
                envio.save()
                venta.with_shipping = True
                venta.save()
                return redirect('carrito.views.envios')
        else:
            form = SendForm()
        return render(request, 'crear_envio.html', {'dataForm': form})
    else:
        return HttpResponseRedirect("/login/")


def detalle_envio(request, send_id=None):
    if request.user.is_authenticated():
        if not send_id is None:
            request.session['send_id'] = send_id
        send_id = int(request.session['send_id'])
        send = Send.objects.get(pk=send_id)
        sale = send.sale
        detalles = sale.detail_sales.all()
        return render(request, 'detalles_envio.html', {"send": send, "detalles": detalles})
    else:
        return HttpResponseRedirect("/login/")


def post_detalle_envio(request, detail_sale_id=None):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = DetailSendForm(request.POST)
            # import pdb; pdb.set_trace()
            if form.is_valid():
                envio = form.save(commit=False)
                recibo = envio.receipt
                detalle_venta = envio.detail_sale
                max_quantity = detalle_venta.quantity - detalle_venta.quantity_shipping

                if envio.quantity > max_quantity:
                    envio.quanity = max_quantity

                if recibo.quantity >= envio.quantity:
                    recibo.quantity -= envio.quantity
                    envio.date_expiration = recibo.date_expiration
                    recibo.save()
                elif envio.quantity > recibo.quantity:
                    envio.quantity = recibo.quantity
                    envio.date_expiration = recibo.date_expiration
                    recibo.save()
                envio.save()

                envios = detalle_venta.detail_sends.all()
                cantidad_envio = 0

                for envio in envios:
                    cantidad_envio += envio.quantity

                # Descontar del inventario de producto
                product = Product.objects.get(pk=detalle_venta.product_id)
                product.inventory -= cantidad_envio
                product.save()
                if detalle_venta.quantity == cantidad_envio:
                    detalle_venta.quantity_shipping = cantidad_envio
                    detalle_venta.with_shipping = True
                else:
                    detalle_venta.quantity_shipping = cantidad_envio
                    detalle_venta.with_shipping = False

                detalle_venta.save()
                return redirect('carrito.views.detalle_envio', send_id=int(request.session['send_id']))
            else:
                send_id = int(request.session['send_id'])
                send = Send.objects.get(pk=send_id)
                detail_sale = DetailSale.objects.get(pk=detail_sale_id)
                data = [{
                    'send': send,
                    'detail_sale': detail_sale,
                    'product': detail_sale.product
                }]
                form = DetailSendForm(detalle_envio=data)
        else:

            if not detail_sale_id is None:
                request.session['detail_sale_id'] = detail_sale_id

            send_id = int(request.session['send_id'])
            detail_sale_id = int(request.session['detail_sale_id'])

            send = Send.objects.get(pk=send_id)
            detail_sale = DetailSale.objects.get(pk=detail_sale_id)

            data = [{
                'send': send,
                'detail_sale': detail_sale,
                'product': detail_sale.product
            }]
            form = DetailSendForm(detalle_envio=data)
        return render(request, 'crear_detalle_envio.html', {'form': form, 'send': send, 'detail_sale': detail_sale})
    else:
        return HttpResponseRedirect("/login/")


def delete_detalle_envio(request, detail_send_id=None):
    if request.user.is_authenticated():
        detail_send = DetailSend.objects.get(pk=detail_send_id)
        detail_sale = detail_send.detail_sale
        product = Product.objects.get(pk=detail_sale.product_id)
        receipt = detail_send.receipt
        receipt.quantity += detail_send.quantity
        product.inventory += detail_send.quantity
        product.save()
        receipt.save()
        detail_sale.with_shipping = False
        detail_sale.quantity_shipping -= detail_send.quantity
        detail_sale.save()
        detail_send.delete()
        return redirect('carrito.views.detalle_envio', send_id=int(request.session['send_id']))
    else:
        return HttpResponseRedirect("/login/")

def recipe_normal(request, image_sale_id):
    receta = ImageSale.objects.get(pk=image_sale_id)
    receta.type_recipe = TYPE_RECIPE_NORMAL
    receta.save()
    data = {'status': 'ok', 'message': 'Se ha foliado receta como tipo normal'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def recipe_with_antibiotico(request, image_sale_id):
    receta = ImageSale.objects.get(pk=image_sale_id)
    receta.type_recipe = TYPE_RECIPE_WITH_ANTIBIOTICO
    receta.save()
    data = {'status': 'ok', 'message': 'Se ha foliado receta como tipo con antibiotico'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def recetas(request):
    if request.user.is_authenticated():
        filter = request.GET.get('filter', 'todos')

        sale_id = request.GET.get('sale', '')

        if len(sale_id) > 0:
            request.session['sale_id'] = sale_id

        if 'sale_id' in request.session:
            sale_id = int(request.session['sale_id'])
            if sale_id > 0:
                sale = Sale.objects.get(pk=sale_id)
            else:
                sale = None
        else:
            sale = None

        if filter == 'todos':
            if not sale is None:
                recipe_list = ImageSale.objects.filter(type_recipe=TYPE_WITHOUT_FOLIO, sale=sale).order_by('-sale')
            else:
                recipe_list = ImageSale.objects.filter(type_recipe=TYPE_WITHOUT_FOLIO).order_by('-sale')
        elif filter == 'es_antibiotico':
            if not sale is None:
                recipe_list = ImageSale.objects.filter(type_recipe=TYPE_RECIPE_WITH_ANTIBIOTICO, sale=sale).order_by('-sale')
            else:
                recipe_list = ImageSale.objects.filter(type_recipe=TYPE_RECIPE_WITH_ANTIBIOTICO).order_by('-sale')
        elif filter == 'normal':
            if not sale is None:
                recipe_list = ImageSale.objects.filter(type_recipe=TYPE_RECIPE_NORMAL, sale=sale).order_by('-sale')
            else:
                recipe_list = ImageSale.objects.filter(type_recipe=TYPE_RECIPE_NORMAL).order_by('-sale')

        """paginator = Paginator(receipt_list, 10)
        page = request.GET.get('page')
        try:
            receipts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            receipts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            receipts = paginator.page(paginator.num_pages)"""
        if not sale is None:
            return render(request, 'recetas.html', {"recetas": recipe_list, 'sale': sale, 'filter': filter})
        else:
            return render(request, 'recetas.html', {"recetas": recipe_list, 'sale': {'id': 0}, 'filter': filter})
    else:
        return HttpResponseRedirect("/login/")
