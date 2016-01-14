# -*- encoding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import Product


def inventario(request):
    if request.user.is_authenticated():
        filtro = request.GET.get('filter', 'todos')

        en_warning = Product.objects.filter(inventory__lte=5).count()
        sin_inventario = Product.objects.filter(inventory__exact=0).count()
        en_warning = en_warning - sin_inventario

        if filtro == 'todos':
            product_list = Product.objects.order_by('-inventory', 'name').all()
        elif filtro == 'sininventario':
            product_list = Product.objects.filter(inventory__exact=0).order_by('name')
        else:
            product_list = Product.objects.filter(inventory__lte=5).order_by('-inventory', 'name')

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

        return render(request, 'inventario.html', {"productos": productos, 'sin_inventario': sin_inventario,
                                                   'en_warning': en_warning, 'filter': filtro})
    else:
        return HttpResponseRedirect("/login/")
