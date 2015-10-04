from django.shortcuts import render
from carrito.models import Sale

# Create your views here.
def pedidos(request):
    pedidos = Sale.objects.all()
    return render(request, 'pedidos.html', {'pedidos': pedidos})