from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from carrito.models import Sale, APPROVED, REJECTED, DELIVERED, PAID, NO_PAID, DetailSale
from usuarios.models import ConektaUser
from usuarios.enviarEmail import EmailSendSale


def pedidos(request):
    if request.user.is_authenticated():
        sale_list = Sale.objects.order_by('-status').all()
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
    import conekta
    conekta.api_key = "key_wHTbNqNviFswU6kY8Grr7w"
    customer_conekta = conekta.Customer.find(user_conekta.conekta_user)
    card = customer_conekta.default_card
    charge = conekta.Charge.create({
        "currency": "MXN",
        "amount": int(pedido.total * 100),
        "description": "Pedido FarmaApp",
        "card": card,
        "details": {
            "email": pedido.user.email,
            "line_items": []
        }
    })
    if charge.status == "paid":
        pedido.charge_conekta = charge.id
        pedido.status = PAID
    else:
        pedido.status = NO_PAID
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
    return render(request, 'detalle_pedido.html', {"pedido": pedido, 'detalles': detalles})


def send_sale_for_email(request, sale_id):
    pedido = Sale.objects.get(pk=sale_id)
    user = pedido.user
    pedido.save()
    detalles = DetailSale.objects.filter(sale=pedido.id)
    enviar_mensaje = EmailSendSale(pedido, detalles, user)
    enviar_mensaje.enviarMensaje()
    return HttpResponse("Email enviado")
