from django.http import HttpResponseRedirect
from django.shortcuts import render
from usuarios.models import ConektaUser
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def home(request):
    return render(request, 'homepage.html')


@api_view(['POST'])
def user_conekta_create(request):
    import conekta
    conekta.api_key = "key_wHTbNqNviFswU6kY8Grr7w"
    user = request.user
    customer = conekta.Customer.create({
        "name": user.get_full_name(),
        "email": user.email,
        "phone": user.cell,
        "cards": request.POST.get('conektaTokenId', None)
    })
    user_conektas = ConektaUser.objects.filter(user=user.id)
    if len(user_conektas) == 0:
        ConektaUser.objects.create(user=user, conekta_user=customer.id)
    else:
        user_conekta = user_conektas[0]
        user_conekta.conekta_user = customer.id
        user_conekta.save()
    return Response({"message": "Usuario creado"})


def login_frontend(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/pedidos/")
            else:
                # Return a 'disabled account' error message
                return HttpResponseRedirect("/login/")
        else:
            # Return an 'invalid login' error message.
            return HttpResponseRedirect("/login/")
    else:
        return render(request, 'login_frontend.html')

