from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from carrito.models import Sale, APPROVED, REJECTED, DELIVERED, PAID, NO_PAID, DetailSale
from usuarios.models import ConektaUser
from usuarios.enviarEmail import EmailSendSale
import conekta

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
    return render(request, 'detalle_pedido.html', {"pedido": pedido, 'detalles': detalles})


def detalle_rechazar(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    pedido.status = REJECTED
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
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
        enviar_mensaje = EmailSendSale(pedido, detalles, pedido.user)
        enviar_mensaje.enviarMensaje()
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


