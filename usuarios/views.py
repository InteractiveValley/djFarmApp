from django.shortcuts import render
from usuarios.models import ConektaUser

# Create your views here.
def home(request):
    return render(request, 'homepage.html')


def userConekta(request):
    import conekta
    conekta.api_key = "key_wHTbNqNviFswU6kY8Grr7w"
    user = request.user
    customer = conekta.Customer.create({
      "name": user.get_full_name(),
      "email": user.email,
      "phone": user.cell,
      "cards": request.POST["conektaTokenId"]
    })
    ConektaUser.objects.create(user=user, conekta_user=customer.id)
    return render(request, 'creado.html')