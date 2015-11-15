from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .forms import ReceiptForm
from productos.models import Receipt


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
                return redirect('productos.views.recibos')
        else:
            form = ReceiptForm()
        return render(request, 'crear_recibo.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")
