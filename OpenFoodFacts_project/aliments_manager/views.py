from .functionnalities import Functionnalities
from django.shortcuts import render, redirect
from .forms import ContactForm, RegistrationForm, ConnectionForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    form = ContactForm(request.POST or None)
    if form.is_valid(): 
        succes = True 
    return render(request, 'aliments_manager/index.html', locals())

def results(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid(): 
           succes = True 
           sujet = form.cleaned_data['sujet']
        products = Functionnalities.getSearch(sujet)
        aliments = []
        firstAliment = False
        for product in products:
            if 'nutrition_grades' in product and 'image_url' in product:
                if firstAliment != False:
                    aliment = {"name":product['product_name'], "url":product['image_url'], "grade":product['nutrition_grades']}
                    aliments.append(aliment)
                else:
                    firstAliment  = product['image_url']
        context = {"aliments":aliments, "firstAliment":firstAliment}
    return render(request, 'aliments_manager/results.html', context)

def registration(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid(): 
        succes = True
        user = form.cleaned_data['nameUser']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        newUser = User.objects.create_user(user, email, password)
        newUser.save()
    return render(request, 'aliments_manager/registration.html', locals())

def connection(request):
    if request.method == 'POST':
        form = ConnectionForm(request.POST or None)
        if form.is_valid():
            user = form.cleaned_data['nameUser']
            password = form.cleaned_data['password']
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = ConnectionForm(request.POST or None)
    return render(request, 'aliments_manager/connection.html', locals())

def disconnection(request):
    logout(request)
    return redirect(reverse(connection))

def account(request):
    user = str(request.user)
    if user == "AnonymousUser":
        return redirect('connection')
    else:
        return render(request, 'aliments_manager/account.html')

