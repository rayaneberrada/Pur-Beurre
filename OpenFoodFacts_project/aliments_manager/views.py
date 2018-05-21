from .functionnalities import Functionnalities
from django.shortcuts import render, redirect
from .forms import ContactForm, RegistrationForm, ConnectionForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from aliments_manager.models import Favorites, User


# Create your views here.
def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    form = ContactForm(request.POST or None)
    if form.is_valid(): 
        succes = True 
    return render(request, 'aliments_manager/index.html', locals())

def results(request, page=1):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid(): 
           succes = True 
           sujet = form.cleaned_data['sujet']
        products = Functionnalities.getSearch(sujet)
        aliments = []
        for product in products:
            if 'nutrition_grades' in product and 'image_url' in product:
                    aliment = {"name":product['product_name'], "url":product['image_url'],\
                             "grade":product['nutrition_grades'], "code":str(product['codes_tags'][1])}
                    aliments.append(aliment)
        aliments = sorted(aliments, key=itemgetter('grade'))
        paginator = Paginator(aliments, 6)
        context = {"aliments":aliments, "firstAliment":aliments[0]["url"]}
    return render(request, 'aliments_manager/results.html', context)

def registration(request):
    form = RegistrationForm(request.POST or None)
    context = {"form":form}
    if form.is_valid():
        user = form.cleaned_data['nameUser']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user_exist = User.objects.filter(username=user)
        if user_exist:
            error = True
            error_msg = "Désolé mais ce compte existe déjà"
            context = {"error_msg": error_msg, "form": form, "error":error}
            return render(request, 'aliments_manager/registration.html', context)
        else:
            succes = True 
            newUser = User.objects.create_user(user, email, password)
            newUser.save()
            context = {"succes":succes, "form":form}
    return render(request, 'aliments_manager/registration.html', context)

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
                error = True
                context = {"error":error, "form":form}
                return render(request, 'aliments_manager/connection.html', context)
    else:
        form = ConnectionForm(request.POST or None)
        context = {"form":form}
    return render(request, 'aliments_manager/connection.html', context)

def disconnection(request):
    logout(request)
    return redirect(reverse(connection))

def account(request):
    user = str(request.user)
    if user == "AnonymousUser":
        return redirect('connection')
    else:
        return render(request, 'aliments_manager/account.html')

@csrf_exempt
def add_favorite(request):
    if request.method == 'POST':
        username = request.user.username
        img = request.POST['img']
        text = request.POST['text']
        grade = request.POST['grade']
        code = request.POST['code']
        if username == "":
            return JsonResponse({"msg":" Vous devez vous connecter pour enregistrer un aliment en favoris"})

        user = User.objects.get(username=username)
        in_db = Favorites.objects.filter(user=user).filter(code=code)
        print(in_db)
        if in_db:
            print("existe déjà")
            return JsonResponse({"msg":" Cet aliment est déjà dans vos favoris"})
        else:
            print("ajout")
            Favorites.objects.create(user=user, url=img, name=text, nutriscore=grade[-5], code=code)
            return JsonResponse({"msg":" l'aliment a bien été ajouté"})
