# -*- encoding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category


def inventario(request):
    if request.user.is_authenticated():
        filtro = request.GET.get('filter', 'todos')

        category_id = request.GET.get('category','')

        if len(category_id) > 0:
            request.session['category_id'] = category_id
        
        if 'category_id' in request.session:
            category_id = int(request.session['category_id'])
            if category_id > 0:
                category = Category.objects.get(pk=category_id)
            else:
                category = None
        else:
            category = None

        en_warning = Product.objects.filter(inventory__lte=5).count()
        sin_inventario = Product.objects.filter(inventory__exact=0).count()
        en_warning = en_warning - sin_inventario

        if filtro == 'todos':
            if not category is None:
                product_list = Product.objects.filter(category=category).order_by('-inventory', 'name')
            else:
                product_list = Product.objects.order_by('-inventory', 'name').all()
        elif filtro == 'sininventario':
            if not category is None:
                product_list = Product.objects.filter(inventory__exact=0,category=category).order_by('name')
            else:
                product_list = Product.objects.filter(inventory__exact=0).order_by('name')
        else:
            if not category is None:
                product_list = Product.objects.filter(inventory__lte=5,category=category).order_by('-inventory', 'name')
            else:
                product_list = Product.objects.filter(inventory__lte=5).order_by('-inventory', 'name')

        """paginator = Paginator(product_list, 10)
        page = request.GET.get('page')
        try:
            productos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            productos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            productos = paginator.page(paginator.num_pages)"""
        if not category is None:
            return render(request, 'inventario.html', {"productos": product_list, 'sin_inventario': sin_inventario,
                                                   'en_warning': en_warning, 'filter': filtro,'category': category })
        else:
            return render(request, 'inventario.html', {"productos": product_list, 'sin_inventario': sin_inventario,
                                                   'en_warning': en_warning, 'filter': filtro,'category': {'id': 0 }})
    else:
        return HttpResponseRedirect("/login/")


def categorias(request):
    if request.user.is_authenticated():
        category_list = Category.objects.all().order_by('position')

        paginator = Paginator(category_list, 100)

        page = request.GET.get('page')

        try:
            registros = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            registros = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            registros = paginator.page(paginator.num_pages)

        return render(request, 'categorias.html', {"registros": registros})
    else:
        return HttpResponseRedirect("/login/")


@csrf_exempt
def categorias_up(request, category_id):
    if request.method == 'POST':
        if request.is_ajax() is True:
            category_up = Category.objects.get(pk=category_id)
            category_down = Category.objects.get(position=category_up.position - 1)
            category_up.position -= 1
            category_down.position += 1
            category_up.save()
            category_down.save()

            category_list = Category.objects.all().order_by('position')
            paginator = Paginator(category_list, 100)
            page = request.GET.get('page', 1)

            try:
                registros = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                registros = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                registros = paginator.page(paginator.num_pages)

            return render(request, 'list_categorias.html', {"registros": registros, "cont_registros": len(registros)})
        else:
            data = {'status': 'bat', 'message': 'No esta autorizado otro metodo'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def categorias_down(request, category_id):
    if request.method == 'POST':
        if request.is_ajax() is True:
            category_down = Category.objects.get(pk=category_id)
            category_up = Category.objects.get(position=category_down.position + 1)
            category_down.position += 1
            category_up.position -= 1
            category_up.save()
            category_down.save()
            category_list = Category.objects.all().order_by('position')
            paginator = Paginator(category_list, 100)
            page = request.GET.get('page', 1)

            try:
                registros = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                registros = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                registros = paginator.page(paginator.num_pages)

            return render(request, 'list_categorias.html', {"registros": registros, "cont_registros": len(registros)})
        else:
            data = {'status': 'bat', 'message': 'No esta autorizado otro metodo'}
    else:
        data = {'status': 'bat', 'message': 'No esta permitido este metodo'}
    return HttpResponse(json.dumps(data), content_type='application/json')

