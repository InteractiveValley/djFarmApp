from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import Product


def inventario(request):
    if request.user.is_authenticated():
        product_list = Product.objects.order_by('-inventory').all()
        paginator = Paginator(product_list, 10)
        page = request.GET.get('page')
        try:
            productos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            productos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            productos = paginator.page(paginator.num_pages)

        return render(request, 'inventario.html', {"productos": productos})
    else:
        return HttpResponseRedirect("/login/")