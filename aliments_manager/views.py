from .functionnalities import Functionnalities
from django.shortcuts import render, redirect
from .forms import ContactForm, RegistrationForm, ConnectionForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from aliments_manager.models import Favorites, User


# Create your views here.
def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    search = ContactForm(request.POST or None)
    context = {"search":search}
    if search.is_valid():
        aliment_searched = search.cleaned_data['sujet']
        page_id = 1
        return redirect('results', aliment_searched, page_id )
    else:
        return render(request, 'aliments_manager/index.html', context)

def results(request, aliment_searched, page_id):
    searchForm = ContactForm(request.POST or None)
    if searchForm.is_valid():
        aliment = searchForm.cleaned_data['sujet']
        page_id = 1
        return redirect('results', aliment, page_id )

    aliments = []
    empty = False
    if 'session_name' in request.session:
        previous_session = request.session['session_name']
    else:
        previous_session = ""

    if previous_session == aliment_searched:
            aliments = request.session['aliment_session']
            first_image = request.session['first_image']
            print("j'utilise une session")
    else:
        products = Functionnalities.getSearch(aliment_searched)
        first_image = ""
        print("j'utilise une requête")
        for product in products:
            if 'nutrition_grades' in product and 'image_url' in product and 'codes_tags' in product:
                if len(str(product['codes_tags'][1])) == 13 and product['nutrition_grades'] in ["a", "b", "c"] :
                    aliment = {"name":product['product_name'], "url_image":product['image_url'],\
                             "grade":product['nutrition_grades'], "code":str(product['codes_tags'][1]),\
                             "nutrient_levels":product['nutrient_levels'], "nutriments":product['nutriments'],\
                             "url":product["url"]}
                    print("'"+str(product['codes_tags'][1])+"'")
                    aliments.append(aliment)
                elif len(str(product['codes_tags'][1])) == 13 and product['nutrition_grades'] in ["d","e"] and first_image == "":
                    first_image = {"name":product['product_name'], "url_image":product['image_url']}
                    request.session['first_image'] = first_image
        aliments = sorted(aliments, key=itemgetter('grade'))

    request.session['aliment_session'] = aliments
    request.session['session_name'] = aliment_searched

    paginator = Paginator(aliments, 6)
    try:
        display = paginator.page(page_id)
    except EmptyPage:
        display = paginator.page(paginator.num_pages)

    if not aliments:
        empty = True 
    context = {"aliments":display, "firstAliment":first_image, "aliment_searched":aliment_searched, "search":searchForm, 'empty':empty}
    return render(request, 'aliments_manager/results.html', context)

def registration(request):
    form = RegistrationForm(request.POST or None)
    search = ContactForm(request.POST or None)
    context = {"form":form, "search":search}
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
            newUser = User.objects.create_user(user, email, password)
            newUser.save()
            return redirect('connection')
    if search.is_valid():
        aliment = search.cleaned_data['sujet']
        page_id = 1
        return redirect('results', aliment, page_id )
    return render(request, 'aliments_manager/registration.html', context)

def connection(request):
    search = ContactForm(request.POST or None)
    if search.is_valid():
        aliment = search.cleaned_data['sujet']
        page_id = 1
        return redirect('results', aliment, page_id )
    if request.method == 'POST':
        form = ConnectionForm(request.POST or None)
        search = ContactForm(request.POST or None)
        if form.is_valid():
            user = form.cleaned_data['nameUser']
            password = form.cleaned_data['password']
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error = True
                context = {"error":error, "form":form, "search":search}
                return render(request, 'aliments_manager/connection.html', context)
    else:
        form = ConnectionForm(request.POST or None)
        context = {"form":form, "search":search}
    return render(request, 'aliments_manager/connection.html', context)

def disconnection(request):
    logout(request)
    return redirect(reverse(home))

def account(request):
    search = ContactForm(request.POST or None)
    context = {"search":search}
    if search.is_valid():
        aliment = search.cleaned_data['sujet']
        page_id = 1
        return redirect('results', aliment, page_id )
    user = str(request.user)
    if user == "AnonymousUser":
        return redirect('connection')
    else:
        return render(request, 'aliments_manager/account.html')

def show_favorites(request, page_id):
    username = request.user.username
    if username == "":
        #afficher un message indiquant à l'utilisateur qu'il a besoin d'être connecté
        return redirect('connection')
    else:
        user = User.objects.get(username=username)
        aliments = Favorites.objects.filter(user=user)
        paginator = Paginator(aliments, 6)
        try:
            display = paginator.page(page_id)
        except EmptyPage:
            display = paginator.page_id(paginator.num_pages)
        search = ContactForm(request.POST or None)
        context = {"aliments":display, "search":search}
        if search.is_valid():
            aliment = search.cleaned_data['sujet']
            page_id = 1
            return redirect('results', aliment, page_id )
        return render(request, 'aliments_manager/favorites.html', context)

@csrf_exempt
def add_favorite(request):
    if request.method == 'POST':
        username = request.user.username
        img = request.POST['img']
        text = request.POST['text']
        grade = request.POST['grade']
        code = request.POST['code']
        url = request.POST['url']
        if username == "":
            return JsonResponse({"msg":" Vous devez vous connecter pour enregistrer un aliment en favoris"})
        else:
            user = User.objects.get(username=username)
            print(code)
            in_db = Favorites.objects.filter(user=user).filter(code=code[:13])
            print(in_db)
        if in_db and username:
            print("existe déjà")
            return JsonResponse({"msg":" Cet aliment est déjà dans vos favoris"})
        else:
            print("ajout")
            Favorites.objects.create(user=user, image=img, name=text, nutriscore=grade[-5], code=code, url=url)
            return JsonResponse({"msg":" l'aliment a bien été ajouté"})

def show_aliment(request, code):
    search = ContactForm(request.POST or None)
    context = {"search":search}
    if search.is_valid():
        aliment = search.cleaned_data['sujet']
        page_id = 1
        return redirect('results', aliment, page_id )

    aliment_selected = Functionnalities.getAliment(code[:13])
    nutrients = aliment_selected['nutrient_levels']
    nutriments = aliment_selected['nutriments']
    nutriments['saturated'] = nutriments.pop('saturated-fat_value')
    aliment_selected['nutrient_levels']['saturated'] = aliment_selected['nutrient_levels'].pop('saturated-fat')
    aliment_selected['url'] = "https://fr.openfoodfacts.org/produit/"+code
    for level in nutrients:
        if nutrients[level] == "low":
            aliment_selected[level] = 'faible'
        elif nutrients[level] == "moderate":
            aliment_selected[level] = 'modérée'
        elif nutrients[level] == "high":
            aliment_selected[level] = 'élevée'

    print(aliment_selected)
    context = {"aliment_selected":aliment_selected, "nutrients":nutrients, "nutriments":nutriments, "search":search}
    return render(request, 'aliments_manager/aliment.html', context)
