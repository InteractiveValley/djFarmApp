import base64
import json
import urllib2

from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from carrito.models import Sale, APPROVED, REJECTED, DELIVERED, PAID, NO_PAID, DetailSale, ImageSale
from usuarios.models import ConektaUser
from usuarios.enviarEmail import EmailSendSale
from django.views.decorators.csrf import csrf_exempt
import conekta
from farmApp.secret import PUSH_APP_ID, PUSH_SECRET_API_KEY


def pedidos(request):
    if request.user.is_authenticated():
        sale_list = Sale.objects.order_by('-created').all()
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

        return render(request, 'pedidos.html', {"pedidos": sales})
    else:
        return HttpResponseRedirect("/login/")


def detalle_pedido(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    detalles = DetailSale.objects.filter(sale=pedido.id)
    return render(request, 'detalle_pedido.html', {"pedido": pedido, 'detalles': detalles})


def detalle_aprobar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    pedido.status = APPROVED
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
    message = "Tu orden #" + str(pedido.id).zfill(6) + " esta en camino"
    create_notification(pedido.user,"FarmaApp", message)
    return render(request, 'detalle_pedido.html', {"pedido": pedido, 'detalles': detalles})


def detalle_rechazar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    pedido.status = REJECTED
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
    message = "Tu orden #" + str(pedido.id).zfill(6) + " no ha podido ser procesado, favor de capturar de nuevo."
    create_notification(pedido.user,"FarmaApp", message)
    return render(request, 'detalle_pedido.html', {"pedido": pedido, 'detalles': detalles})


def detalle_entregar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    pedido.status = DELIVERED
    user_conekta = ConektaUser.objects.get(user=pedido.user)
    conekta.api_key = "key_wHTbNqNviFswU6kY8Grr7w"
    customer_conekta = conekta.Customer.find(user_conekta.conekta_user)
    card = customer_conekta.cards[0]
    amount = str(int(float(pedido.total() * 100)))
    detalles = pedido.detail_sales.all()
    lista = []
    for detalle in detalles:
        dato = {
          "name": detalle.product.name,
          "description": detalle.product.description,
          "unit_price": str(int(float(detalle.price * 100))),
          "quantity": detalle.quantity,
          "sku": str(detalle.product.id),
          "type": "medicine"
         };
        lista.append(dato)
    charge = conekta.Charge.create({
            "description": "Pedido FarmaApp",
            "amount": amount,
            "currency": "MXN",
            "reference_id": "pedido-farmaapp-" + str(pedido.id),
            "card": card.id,
            "details": {
                "name": pedido.user.get_full_name(),
                "phone": pedido.user.cell,
                "email": pedido.user.email,
                "line_items": lista
            }
    })
    #  import pdb; pdb.set_trace()
    if charge.status == "paid":
        pedido.charge_conekta = charge.id
        pedido.status = PAID
        pedido.save()
        pedido.discount_inventory()
        //enviar_mensaje = EmailSendSale(pedido, detalles, pedido.user)
        //enviar_mensaje.enviarMensaje()
        str_pedido = str(pedido.id).zfill(6)
        str_total = '{:20,.2f}'.format(pedido.total())
        message = "Tu orden #{0} con un monto de ${1} ha sido entregada.".format(str_pedido, str_total)
        create_notification(pedido.user,"FarmaApp", message)
    else:
        pedido.status = NO_PAID
        pedido.save()
    return render(request, 'detalle_pedido.html', {"pedido": pedido, 'detalles': detalles})



def send_sale_for_email(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    user = pedido.user
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
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


def create_notification(user, title, message):
    tokens = [user.token_phone.all()[0].token]
    post_data = {
        "tokens": tokens,
        "production": "true",
        "notification": {
            "title": title,
            "alert": message
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